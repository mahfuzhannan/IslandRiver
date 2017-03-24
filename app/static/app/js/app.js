/**
 * Created by mafz on 19/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('app', [
        'shop',
        'basket',
        'user',
        'ngRoute',
        'ngNotify'
    ])
        .config(['$routeProvider', '$httpProvider', function (routeProvider, $httpProvider) {
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        }]);
})(window.angular);
