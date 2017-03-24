(function (angular){
     'use strict';
         angular.module('user', [])
             .controller('userController', ['userService', '$scope', 'ngNotify', '$window', function (user, $scope, ngNotify, $window) {
                 $scope.user = null;

                 $scope.getUser = function () {
                     user.getUser().success(function (response) {
                         $scope.user = response;
                     }).error(function () {
                     //    do something
                     });
                 };

                 $scope.removeUser = function() {
                     user.removeUser().success(function (response) {
                         ngNotify.set(response.message, {type: 'success', duration: 10000}, function () {
                             // redirect to login
                             $window.location.href = response.next;
                         });
                         alert("Are you sure you want to delete your account?");
                     }).error(function (response) {
                         ngNotify.set(response.error, {type: 'error', duration: 10000}, function () {
                             // redirect to login
                             $window.location.href = response.next;
                         });
                         console.log("User cannot be deleted");
                     });
                 }
             }])

             .service('userService', ['$http', function ($http) {
                 this.getUser = function () {
                     return $http.get('/user');
                 };

                 this.removeUser = function(){
                    return $http.delete('/account/');
                    console.log("Deleted");
                 };
             }]);
})(window.angular);
