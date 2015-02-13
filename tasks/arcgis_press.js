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

    grunt.registerMultiTask('arcgis_press',
        'A grunt task for covering your ArcGIS service publishing needs. Hot off the press!', function() {

        var done = this.async();

        // Merge task-specific and/or target-specific options with these defaults.
        // var options = this.options({
        //     // punctuation: '.',
        //     // separator: ', '
        // });

        var shellOptions = {
            scriptPath: __dirname + '/scripts'
        };

        // instead of run we could also use the messaging functionality
        // see: https://github.com/extrabacon/python-shell#exchanging-data-between-node-and-python
        PythonShell.run('publish_mxd.py', shellOptions, function (err) {
            if (err) {
                grunt.log.error(err.stack);
                done(false);
            }

            grunt.log.writeln('service published successfully');
            done();
        });
    });

};