/**
 * Created by mafz on 19/02/2017.
 */
(function (angular) {
    'use strict';
    angular.module('product', [])
        .controller('productController', ['productService', 'shopService', '$scope', 'ngNotify', '$location', '$window', function (product, shop, $scope, ngNotify, $location, $window) {
            $scope.reviews = null;
            $scope.rating = null;
            $scope.comments = null;

            $scope.init = function () {
                var pathArr = $window.location.pathname.split('/');
                if(pathArr[2] == 'men') {
                    $scope.catalogSlug = 'men';
                } else if(pathArr[2] == 'women'){
                    $scope.catalogSlug = 'women';
                } else {
                    shop.getCatalogs().success(function (response) {
                        $scope.catalogs = response;
                    }).error(function (response) {
                        ngNotify.set(response, {type: 'error', duration: 4000});
                    })
                }
                $scope.loading = true;
                getCategories();
                getProducts();
            };

            $scope.addProduct = function (productId, quantity) {
                shop.addToBasket(productId, quantity).success(function (response) {
                    ngNotify.set(response.message, {type: 'success', duration: 4000});
                }).error(function (response) {
                    ngNotify.set(response, {type: 'error', duration: 4000});
                });
            };

            $scope.setRating = function (rating) {
                $scope.rating = rating;
            };

            $scope.addReview = function (product_id) {
                if($scope.rating > 0) {
                    product.addReview(product_id, $scope.rating, $scope.comments).success(function (response) {
                        ngNotify.set(response.message, {type: 'success', duration: 4000}, function () {
                            $window.location.href = $location.absUrl()
                        });
                    }).error(function (response) {
                        ngNotify.set(response, {type: 'error', duration: 4000});
                    });
                } else {
                    ngNotify.set('Please select a rating.', {type: 'error', duration: 4000});
                }
            }

        }])
        .service('productService', ['$http', function ($http) {
            this.addReview = function (product_id, rating, comments) {
                return $http.post('/products/review/', {product_id: product_id, rating:rating, comments: comments});
            };
        }]);
})(window.angular);