/**
 * Created by mafz on 27/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('basket', [
        'underscore'
    ])
        .controller('basketController', ['basketService', '$scope', 'ngNotify', '_', function (basket, $scope, ngNotify, _) {
            $scope.basket = null;
            $scope.basketProducts = [];
            $scope.loading = true;

            $scope.getBasketProducts = function () {
                basket.getBasketProducts().success(function (response) {
                    $scope.basketProducts = response;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                }).then(function (response) {
                    $scope.loading = false;
                });
            };

            $scope.addProduct = function (basketProductId, productName) {
                $scope.loading = true;
                basket.addProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 2000});
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                }).then(function (response) {
                    $scope.getBasketProducts();
                });
            };

            $scope.removeProduct = function (basketProductId, productName) {
                $scope.loading = true;
                basket.removeProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 2000});
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                }).then(function (response) {
                    $scope.getBasketProducts();
                });
            };

            $scope.deleteProduct = function (basketProductId, productName) {
                $scope.loading = true;
                basket.deleteProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 2000});
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                }).then(function (response) {
                    $scope.getBasketProducts();
                });
            };

            $scope.isBasketEmpty = function () {
                console.log(_.size($scope.basketProducts));
                return _.size($scope.basketProducts) ? false : true;
            }
        }])
        .service('basketService', ['$http', function ($http) {
            this.getBasketProducts = function () {
                return $http.get('/baskets/products');
            };

            this.addProduct = function (basketProductId, productName) {
                return $http.put('/baskets/', {remove:{basket_product_id:basketProductId, product_name: productName}});
            };

            this.removeProduct = function (basketProductId, productName) {
                return $http.put('/baskets/', {add:{basket_product_id:basketProductId, product_name: productName}});
            };

            this.deleteProduct = function (basketProductId, productName) {
                return $http.delete('/baskets/', {params:{basket_product_id:basketProductId, product_name: productName}});
            };
        }]);
})(window.angular);