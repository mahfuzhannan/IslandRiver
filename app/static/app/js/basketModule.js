/**
 * Created by mafz on 27/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('basket', [
        'underscore'
    ])
        .controller('basketController', ['basketService', '$scope', function (basket, $scope) {

        }])
        .service('basketService', ['$http', function ($http) {
            this.add = function (item) {
                $http.post('/basket/add', {item: item});
            };

            this.remove = function (item) {
                $http.post('/basket/remove', {item:item});
            };

            this.checkout = function () {
                $http.post('basket/checkout')
            };
        }]);
})(window.angular);