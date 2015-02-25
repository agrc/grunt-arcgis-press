'use strict';

module.exports = function (optionsObj, targetName) {
    var cloneDeep = require('lodash.clonedeep');
    var merge = require('lodash.merge');
    var defaults = require('lodash.defaults');

    var result = cloneDeep(optionsObj.options);

    merge(result, optionsObj[targetName].options);

    // apply commonServiceProperties
    if (result.commonServiceProperties) {
        for (var serv in result.services) {
            if (result.services.hasOwnProperty(serv)) {
                defaults(result.services[serv], result.commonServiceProperties);
            }
        }
        delete result.commonServiceProperties;
    }

    return result;
};
