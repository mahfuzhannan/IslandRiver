/**
 * Created by mafz on 27/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('basket', [
        'underscore'
    ])
        .controller('basketController', ['basketService', '$scope', 'ngNotify', '_', '$window', function (basket, $scope, ngNotify, _, $window) {
            $scope.basket = null;
            $scope.basketProducts = [];
            $scope.loading = true;

            $scope.getBasketProducts = function () {
                basket.getBasketProducts().success(function (response) {
                    $scope.basketProducts = response;
                    $scope.loading = false;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.loading = false;
                });
            };

            $scope.addProduct = function (basketProductId, productName) {
                console.log('thrthtr', basketProductId);
                console.log('sdfsdfsd', productName);
                $scope.loading = true;
                basket.addProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000});
                    $scope.getBasketProducts();
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.getBasketProducts();
                });
            };

            $scope.removeProduct = function (basketProductId, productName) {
                $scope.loading = true;
                basket.removeProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000});
                    $scope.getBasketProducts();
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.getBasketProducts();
                });
            };

            $scope.deleteProduct = function (basketProductId, productName) {
                $scope.loading = true;
                basket.deleteProduct(basketProductId, productName).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000});
                    $scope.getBasketProducts();
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.getBasketProducts();
                });
            };

            $scope.checkout = function () {
                basket.checkout().success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000}, function () {
                        $window.location.href = response.next;
                    });
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.getBasketProducts();
                });
            };

            $scope.isBasketEmpty = function () {
                return _.size($scope.basketProducts) ? false : true;
            };

            $scope.orderByProduct = function (basketProduct) {
                return basketProduct.product.name;
            };

            $scope.getTotalQuantity = function () {
                var totalQuantity = 0;
                _.forEach($scope.basketProducts, function (basketProduct) {
                    totalQuantity += parseInt(basketProduct.quantity);
                });
                return totalQuantity;
            };

            $scope.getTotal = function () {
                var total = 0;
                _.forEach($scope.basketProducts, function (basketProduct) {
                    total += basketProduct.quantity * basketProduct.product.price;
                });
                return total;
            };

            $scope.troll = function () {
                ngNotify.set('Nice try...', {type: 'info', duration: 4000});
            };
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

            this.checkout = function () {
                return $http.post('/checkout/')
            }
        }]);
})(window.angular);