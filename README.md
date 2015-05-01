[![Build Status](https://travis-ci.org/agrc/grunt-arcgis-press.svg?branch=master)](https://travis-ci.org/agrc/grunt-arcgis-press)

![press](https://cloud.githubusercontent.com/assets/325813/6882906/25168c48-d55c-11e4-851c-5fa3765fee68.png)
# grunt-arcgis-press

> A grunt task for covering your ArcGIS service publishing needs. Hot off the press!

## Getting Started
This plugin requires Grunt.

If you haven't used [Grunt](http://gruntjs.com/) before, be sure to check out the [Getting Started](http://gruntjs.com/getting-started) guide, as it explains how to create a [Gruntfile](http://gruntjs.com/sample-gruntfile) as well as install and use Grunt plugins. Once you're familiar with that process, you may install this plugin with this command:

```shell
npm install grunt-arcgis-press --save-dev
```

Once the plugin has been installed, it may be enabled inside your Gruntfile with this line of JavaScript:

```js
grunt.loadNpmTasks('grunt-arcgis-press');
```

## The "arcgis_press" task

### Overview
In your project's Gruntfile, add a property named `arcgis_press` to the data object passed into `grunt.initConfig()`.

```js
grunt.initConfig({
    arcgis_press: {
        options: {
            server: {
                username: 'an administrative username for accessing the /arcgis/admin page. Store this value in your secrets.json file.',
                password: 'the password for that user. Store this value in your secrets.json file.'
            },
            mapServerBasePath: 'the base path (parent folder) to your mxd\'s. This can be placed into your secrets.json file to allow for different project structures among developers.',
            commonServiceProperties: {
                // These properties can be any item from the service json. They will be mixed into all of services 
                minInstancesPerNode: 0,
                maxInstancesPerNode: 3
            },
            services: {
                service1: {
                    type: 'The type of the resource being published (MapServer|GpServer|Soe)',
                    serviceName: 'The service name when publishing to server',
                    resource: 'The file name with extension from within the serviceBasePath being published.',
                    folder: 'The folder on arcgis server within which you want the service published (omit for root folder)'
                        // all commonServiceProperties will be mixed in with these
                },
                service2: {
                    // you can have as many of these as you need for your project.
                }
            }
        },
        dev: {
            options: {
                // Target-specific overrides for test, stage, and production go here. These override the service level entries.
                server: {
                    host: secrets.devHost
                },
                commonServiceProperties: {
                    minInstancesPerNode: 0
                },
                services: {
                    // these names must match the earlier entries for the overrides to link
                    service1: {
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
        },
        prod: {
            options: {
                server: {
                    host: secrets.prodHost
                }
            }
        }
    },
});
```

## Python usage
grunt-arcgis-press uses a python module to perform the interactions with arcgis server. This python module makes it possible to use the modules api without using grunt. Theoretically, other build tool plugins could be created using the python module or you could invoke it directly. Also, it's invaluable for debugging. Below are the cli options and examples. 

### Stage
`press stage <ip> <username> <password> <json> <[temp_folder]>`  
`python -m press stage localhost user pass {\"type\":\"MapServer\",\"serviceName\":\"MainDevMapService\",\"resource\":\"C:\\Projects\\GitHub\\BEMS\\maps\\BEMS.local.mxd\",\"folder\":\"press\"}`

### Upload
`press upload <ip> <username> <password> <sd> <connection_file>`  
`python -m press upload localhost user pass c:\\Projects\\GitHub\\grunt-arcgis-press\\tasks\\scripts\\.temp\\draft.sd c:\\Projects\\GitHub\\grunt-arcgis-press\\tasks\\scripts\\.temp\\server_connection.ags`

### Edit
`press edit <ip> <username> <password> <json> <[temp_folder]>` 
`python -m press edit localhost user pass {\"type\":\"MapServer\",\"serviceName\":\"MainDevMapService\",\"resource\":\"C:\\Projects\\GitHub\\BEMS\\maps\\BEMS.local.mxd\",\"minInstancesPerNode\":2,\"capabilities\":\"Map,Query\",\"properties\":{\"maxRecordCount\":\"1500\"},\"maxInstancesPerNode\":3}`

### Publish
`press upload <ip> <username> <password> <json> <[temp_folder]>`  
`python -m press publish localhost user pass {\"type\":\"MapServer\",\"serviceName\":\"MainDevMapService\",\"resource\":\"C:\\Projects\\GitHub\\BEMS\\maps\\BEMS.local.mxd\",\"minInstancesPerNode\":2,\"capabilities\":\"Map,Query\",\"properties\":{\"maxRecordCount\":\"500\"},\"maxInstancesPerNode\":3}`

## Release History
**0.2.0** - Initial release. Available functionality limited to publishing `.mxd` documents as dynamic map services. 

## License
Copyright (c) 2015 AGRC. Licensed under the MIT license.
