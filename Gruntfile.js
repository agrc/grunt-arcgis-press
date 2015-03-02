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

    var secrets;
    try {
        secrets = grunt.file.readJSON('secrets.json');
    } catch (e) {
        secrets = {
            devHost: 'localhost',
            stageHost: 'blah',
            username: 'username',
            password: 'password',
            mxdBasePath: 'path'
        };
    }

    // Project configuration.
    grunt.initConfig({
        arcgis_press: {
            options: {
                // Any service props defined here are applied to all services.
                mapServerBasePath: secrets.mxdBasePath,
                gpServerBasePath: '',
                commonServiceProperties: {
                    minInstancesPerNode: 1,
                    maxInstancesPerNode: 3
                },
                server: {
                    username: secrets.username,
                    password: secrets.password
                },
                services: {
                    // Each service is a property of this object which will
                    // allow for overriding service-level options from within
                    // different targets.
                    // Prop names need to be unique.
                    mainMapService: {
                        type: 'MapServer',
                        serviceName: '1',
                        resource: 'This.mxd',
                        folder: 'Pressed',
                        minInstancesPerNode: 2,
                        capabilities: 'Map,Query',
                        properties: {
                            maxRecordCount: '1500'
                        }
                    },
                    mainMapService2: {
                        type: 'MapServer',
                        serviceName: '2',
                        resource: 'Other.mxd',
                        // this prop would override the general one above
                        minInstancesPerNode: 2,
                        capabilities: 'Map,Query',
                        properties: {
                            maxRecordCount: '1500'
                        }
                    }
                    // toolbox: {
                    //     type: 'GPServer',
                    //     basePathToResource: 'scripts/...',
                    //     properties: {
                    //         maximumRecords: '1500'
                    //     }
                    // },
                    // soe: {
                    //     type: 'SOE',
                    //     path: 'soe/xyq.soe',
                    //     name: 'mySoe'
                    // }
                }
            },
            dev: {
                options: {
                    server: {
                        host: secrets.devHost
                    },
                    commonServiceProperties: {
                        minInstancesPerNode: 0
                    },
                    services: {
                        mainMapService: {
                            serviceName: 'This'
                        }
                    }
                }
            },
            stage: {
                options: {
                    server: {
                        host: secrets.stageHost
                    }
                }
            }
        },
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
        nodeunit: {
            tests: ['test/*_test.js']
        },
        watch: {
            files: [
                'tasks/**/*.*',
                'test/**/*.*',
                'Gruntfile.js'
            ],
            tasks: ['jshint', 'test']
        }
    });

    // Actually load this plugin's task(s).
    grunt.loadTasks('tasks');

    //grunt.registerTask('test', ['arcgis_press:dev', 'nodeunit']);
    grunt.registerTask('test', ['nodeunit']);

    grunt.registerTask('default', grunt.config('watch.tasks').concat('watch'));

    grunt.registerTask('travis', ['jshint', 'test']);
};