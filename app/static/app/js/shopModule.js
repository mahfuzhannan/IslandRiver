/**
 * Created by mafz on 19/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('shop', [])
        .controller('shopController', ['shopService', '$scope', 'ngNotify', '$window', function (shop, $scope, ngNotify, $window) {
            $scope.products = null;
            $scope.catalogSlug = '';
            $scope.categories = [];
            $scope.categorySlug = '';
            $scope.price = '';
            $scope.loading = true;

            $scope.init = function () {
                var pathArr = $window.location.pathname.split('/');
                console.log(pathArr);
                if(pathArr[2] == 'men') {
                    $scope.catalogSlug = 'men';
                } else {
                    $scope.catalogSlug = 'women';
                }
                $scope.loading = true;
                getCategories();
                getProducts();
            };

            $scope.loadWomen = function () {
                $scope.loading = true;
                getCatalogs();
                $scope.catalogSlug = 'women';
                getProducts();
            };

            function getProducts() {
                $scope.loading = true;
                shop.getProducts($scope.catalogSlug, $scope.categorySlug, $scope.price).success(function (response) {
                    $scope.products = response;
                    $scope.loading = false;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                    $scope.loading = false;
                });
            }

            function getCategories() {
                shop.getCategories($scope.catalogSlug).success(function (response) {
                    console.log(response);
                    $scope.categories = response;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                });
            }

            $scope.setCategory = function (categorySlug) {
                $scope.categorySlug = categorySlug;
                getProducts();
            };

            $scope.addItem = function (productId) {
                shop.addToBasket(productId).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 2000});
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 2000});
                });
            };

            $scope.getFilter = function () {
                var str = 'All';
                if($scope.catalogSlug && $scope.categorySlug) {
                    str = $scope.catalogSlug + ' > ' + $scope.categorySlug;
                } else if($scope.catalogSlug) {
                    str = $scope.catalogSlug + ' > All';
                }
                return str;
            };

            $scope.areProductsEmpty = function () {
                return _.size($scope.products);
            }

        }])
        .service('shopService', ['$http', function ($http) {
            this.getProducts = function (catalogSlug, categorySlug, price) {
                return $http.get('/api/products/?format=json&category__catalog__slug=' + catalogSlug +
                    '&category__slug=' + categorySlug + '&price=' + price);
            };

            this.getCatalogs = function () {
                return $http.get('/api/catalogs/?format=json');
            };

            this.getCategories = function (catalogSlug) {
                return $http.get('/api/categories/?format=json&catalog__slug=' + catalogSlug);
            };

            this.addToBasket = function (productId) {
                return $http.put('/baskets/', {add:{product_id:productId}});
            };
        }]);
})(window.angular);