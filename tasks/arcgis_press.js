/*
 * grunt-arcgis-press
 * https://github.com/agrc/grunt-arcgis-press
 *
 * Copyright (c) 2015 Steve Gourley & Scott Davis
 * Licensed under the MIT license.
 */

'use strict';

module.exports = function(grunt) {
    var PythonShell = require('python-shell');
    var chalk = require('chalk');
    var mixin = require('./lib/mixin_options');
    var Promise = require('promise');
    var path = require('path');

    grunt.registerMultiTask('arcgis_press',
        'A grunt task for covering your ArcGIS service publishing needs. Hot off the press!',
        function() {
            var done = this.async();

            // create temp folder if needed
            var tempFolder = path.join(process.cwd(), '.grunt', 'grunt-arcgis-press');
            if (!grunt.file.exists(tempFolder)) {
                grunt.file.mkdir(tempFolder);
            }

            // need to use our own mixin because grunt's doesn't do a deep mixin
            var config = mixin(grunt.config('arcgis_press'), this.target);

            var commonArgs = [
                config.server.host,
                config.server.username,
                config.server.password
            ];
            var shellOptions = {
                cwd: __dirname + '/scripts',
                pythonOptions: ['-m'],
                scriptPath: 'press'
            };

            var promises = [];

            var invokePython = function(command, args) {
                shellOptions.args = [command].concat(commonArgs, args);
                return new Promise(function(resolve, reject) {
                    PythonShell.run('', shellOptions, function(err, results) {
                        if (err) {
                            grunt.log.error(err.message);
                            grunt.verbose.error(err.stack);
                            reject();
                        }

                        resolve(results);
                    });
                });
            };

            var publishService = function(service) {

                var basePath = null;
                if(service.type.toUpperCase() === 'MAPSERVER'){
                    basePath = config.mapServerBasePath;
                }else if(service.type.toUpperCase() === 'GPSERVER'){
                    basePath = config.gpServerBasePath;
                }

                service.resource = path.join(basePath, service.resource);
                var args = [
                    JSON.stringify(service),
                    tempFolder
                ];
                var sn = service.serviceName;
                grunt.log.writelns(chalk.blue('Publishing: ' + sn));
                grunt.verbose.writelns(chalk.blue(sn + ': staging...'));
                return invokePython('stage', args)
                    .then(function(results) {
                        // the return value from the python script has an extra
                        // character that causes the next script to error so we
                        // need to trim it
                        results[0] = results[0].trim();
                        results[1] = results[1].trim();
                        grunt.verbose.writelns(chalk.blue(sn + ': uploading...'));
                        return invokePython('upload', results);
                    })
                    .then(function() {
                        grunt.verbose.writelns(chalk.blue(sn + ': updating service properties...'));
                        return invokePython('edit', args);
                    })
                    .then(function () {
                        var msg = sn + ' (' + service.type +
                            ') was successfully published to ' + config.server.host;
                        grunt.verbose.writelns(chalk.blue(msg));
                    });
            };

            // loop through services
            for (var prop in config.services) {
                if (config.services.hasOwnProperty(prop)) {
                    promises.push(publishService(config.services[prop]));
                }
            }

            Promise.all(promises).then(function() {
                done();
            }, function() {
                done(false);
            });
        });
};