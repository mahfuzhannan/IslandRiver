/**
 * Created by mafz on 28/01/2017.
 */
angular.module('underscore', [])
    .factory('_', ['$window', function($window) {
        // place lodash include before angular
        return $window._;
    }]);