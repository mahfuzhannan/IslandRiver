/**
 * Created by mafz on 19/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('app.shop', [
        'app.data'
    ])
        .controller('shopController', ['shopService', '$scope', function (shop, $scope) {
            $scope.items = null;

            $scope.getItems = function () {
                shop.getItems().success(function (response) {
                    $scope.items = response;
                }).error(function () {
                //    do something
                });
            };

            $scope.addItem = function (item) {
                shop.addToBasket(item);
            };

        }])
        .service('shopService', ['$http', function ($http) {
            this.getItems = function () {
                return $http.get('/items');
            };

            this.addToBasket = function (item) {
                return $http.put('/baskets/', {item:item});
            };

            this.removeFromBasket = function (item) {
                return $http.delete('/baskets/', {params:{item:item}});
            };

            this.checkout = function () {
                return $http.get('/baskets/checkout');
            };
        }]);
})(window.angular);