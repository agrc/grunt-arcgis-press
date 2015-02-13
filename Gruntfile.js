/*
 * grunt-arcgis-press
 * https://github.com/agrc/grunt-arcgis-press
 *
 * Copyright (c) 2015 Steve Gourley & Scott Davis
 * Licensed under the MIT license.
 */

'use strict';

module.exports = function(grunt) {
    // load all npm grunt tasks
    require('load-grunt-tasks')(grunt);

    // Project configuration.
    grunt.initConfig({
        jshint: {
            all: [
                'Gruntfile.js',
                'tasks/*.js',
                '<%= nodeunit.tests %>'
            ],
            options: {
                jshintrc: '.jshintrc',
                reporter: require('jshint-stylish')
            }
        },

        // Configuration to be run (and then tested).
        arcgis_press: {
            default_options: {
                options: {}
            },
            custom_options: {
                options: {}
            }
        },

        // Unit tests.
        nodeunit: {
            tests: ['test/*_test.js']
        }

    });

    // Actually load this plugin's task(s).
    grunt.loadTasks('tasks');

    // grunt.registerTask('test', ['arcgis_press', 'nodeunit']);
    grunt.registerTask('test', []);

    grunt.registerTask('default', ['jshint', 'test']);

    grunt.registerTask('travis', ['jshint', 'test']);
};