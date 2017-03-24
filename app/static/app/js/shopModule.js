/**
 * Created by mafz on 19/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('shop', [])
        .controller('shopController', ['shopService', '$scope', 'ngNotify', '$window', function (shop, $scope, ngNotify, $window) {
            $scope.products = null;
            $scope.catalogSlug = '';
            $scope.catalogs = null;
            $scope.categories = [];
            $scope.categorySlug = '';
            $scope.price = '';
            $scope.loading = true;

            $scope.init = function () {
                var pathArr = $window.location.pathname.split('/');
                console.log(pathArr);
                if(pathArr[2] == 'men') {
                    $scope.catalogSlug = 'men';
                } else if(pathArr[2] == 'women'){
                    $scope.catalogSlug = 'women';
                } else {
                    shop.getCatalogs().success(function (response) {
                        $scope.catalogs = response;
                    }).error(function () {
                        ngNotify.set(response.error, {type: 'error', duration: 4000});
                    })
                }
                $scope.loading = true;
                getCategories();
                getProducts();
            };

            function getProducts() {
                $scope.loading = true;
                shop.getProducts($scope.catalogSlug, $scope.categorySlug, $scope.price).success(function (response) {
                    $scope.products = response;
                    $scope.loading = false;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                    $scope.loading = false;
                });
            }

            function getCategories() {
                shop.getCategories($scope.catalogSlug).success(function (response) {
                    $scope.categories = response;
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                });
            }

            $scope.setCategory = function (categorySlug) {
                $scope.categorySlug = categorySlug;
                getProducts();
            };

            $scope.addProduct = function (productId, quantity) {
                shop.addToBasket(productId, quantity).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000});
                }).error(function (response) {
                    ngNotify.set(response.error, {type: 'error', duration: 4000});
                });
            };

            $scope.getFilter = function () {
                var str = 'all products';
                if($scope.catalogs) {
                    str = $scope.categorySlug;
                } else if($scope.catalogSlug && $scope.categorySlug) {
                    str = $scope.catalogSlug + ' > ' + $scope.categorySlug;
                } else if($scope.catalogSlug) {
                    str = $scope.catalogSlug + ' > all products';
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

            this.addToBasket = function (productId, quantity) {
                return $http.put('/baskets/', {add:{product_id:productId, quantity:quantity||1}});
            };
        }]);
})(window.angular);