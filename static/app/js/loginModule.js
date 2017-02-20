/**
 * Created by mafz on 28/01/2017.
 */
(function(angular) {
    'use strict';
    angular.module('app.login', ['app.data'])
        .controller('loginController', ['loginService', '$scope', '$window', function (login, $scope, $window) {
            $scope.email = '';
            $scope.pass = '';

            $scope.error = "";

            $scope.login = function() {
                $scope.error = "";
                var form = {
                    email: $scope.email,
                    pass: $scope.pass
                };
                login.login(form).then(function(response) {
                    if(response.error) {
                        $scope.error = response.error;
                    } else {
                        // redirect to page after login
                        $window.location.href = '/account';
                    }
                });
            };
        }])

        .service('loginService', ['dataService', function (data) {
            this.login = function(form) {
                // put url to login here
                return data.put('/auth/login', {form: form});
            }
        }]);
})(window.angular);