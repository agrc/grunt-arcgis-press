'use strict';

var grunt = require('grunt');
var mixin = require('../tasks/lib/mixin_options');

exports.arcgis_press = {
    deep_merge_options: function (test) {
        var expected_dev = grunt.file.readJSON('test/data/expected_options_dev.json');
        var expected_stage = grunt.file.readJSON('test/data/expected_options_stage.json');
        var options = grunt.file.readJSON('test/data/options.json');

        test.deepEqual(mixin(options, 'dev'), expected_dev);
        test.deepEqual(mixin(options, 'stage'), expected_stage);

        test.done();
    },
    no_common: function (test) {
        var expected = grunt.file.readJSON('test/data/expected_options_no_common.json');
        var options = grunt.file.readJSON('test/data/options_no_common.json');

        test.deepEqual(mixin(options, 'dev'), expected);

        test.done();
    }
};