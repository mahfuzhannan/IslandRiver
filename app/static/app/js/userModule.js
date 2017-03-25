(function (angular){
     'use strict';
         angular.module('user', [])
             .controller('userController', ['userService', '$scope', 'ngNotify', '$window', function (user, $scope, ngNotify, $window) {
                 $scope.email = null;
                 $scope.address = null;

                 $scope.removeUser = function(email) {
                     console.log(email);
                     if($scope.email==email){
                         user.removeUser().success(function (response) {
                             ngNotify.set(response.message, {type: 'success', duration: 4000}, function () {
                                 // redirect to login
                                 $window.location.href = response.next;
                             });
                         }).error(function (response) {
                             ngNotify.set(response, {type: 'error', duration: 4000}, function () {
                                 // redirect to login
                                 $window.location.href = response.next;
                             });
                         });
                     } else {
                         ngNotify.set('emails did not match', {type: 'error', duration: 5000});
                     }
                 }
             }])
             .service('userService', ['$http', function ($http) {
                 this.removeUser = function() {
                    return $http.delete('/account/');
                 };
             }]);
})(window.angular);
