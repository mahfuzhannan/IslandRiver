/**
 * Created by mafz on 27/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('app.basket', [
        'app.data',
        'underscore'
    ])
        .controller('basketController', ['basketService', '$scope', function (basket, $scope) {

        }])
        .service('basketService', ['dataService', function (data) {
            this.add = function (item) {
                data.post('/basket/add', {item: item});
            };

            this.remove = function (item) {
                data.post('/basket/remove', {item:item});
            };

            this.checkout = function () {
                data.post('basket/checkout')
            };
        }]);
})(window.angular);