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

    grunt.registerMultiTask('arcgis_press',
        'A grunt task for covering your ArcGIS service publishing needs. Hot off the press!',
        function() {
            var done = this.async();

            var config = mixin(grunt.config('arcgis_press'), this.target);

            var shellOptions = {
                cwd: __dirname + '/scripts',
                pythonOptions: ['-m'],
                scriptPath: 'press'
            };

            var promises = [];

            var publishService = function (service) {
                shellOptions.args = [JSON.stringify(service), JSON.stringify(config.server)];
                return new Promise(function (resolve, reject) {
                    PythonShell.run('', shellOptions, function(err, results) {
                        if (err) {
                            grunt.verbose.error(err.stack);
                            grunt.log.error(err.message);
                            reject();
                        }

                        if (results) {
                            for (var i = 0; i < results.length; i++) {
                                grunt.log.writelns(chalk.blue(results[i]));
                            }
                        }

                        resolve();
                    });
                });
            };

            for (var prop in config.services) {
                if (config.services.hasOwnProperty(prop)) {
                    promises.push(publishService(config.services[prop]));
                }
            }

            Promise.all(promises).then(function () {
                done();
            }, function () {
                done(false);
            });
        });
};