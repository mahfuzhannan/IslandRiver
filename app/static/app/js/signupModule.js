/**
 * Created by mafz on 24/10/2016.
 */
(function(angular) {
    'use strict';
    angular.module('app.signup', [
        'app.data',
        'underscore'
    ])
        .controller('signupController', ['signupService', '$scope', '$window', '_', function (signup, $scope, $window, _) {
            $scope.firstname = "";
            $scope.lastname = "";
            $scope.email = "";
            $scope.pass = "";
            $scope.passconfirm = "";
            $scope.agree;

            $scope.error = "";

            $scope.signup = function() {
                if(validate()) {
                    var form = {
                        firstname: $scope.firstname ,
                        lastname: $scope.lastname ,
                        email: $scope.email,
                        pass: $scope.pass ,
                        passconfirm: $scope.passconfirm ,
                        agree: $scope.agree
                    };
                    signup.signup(form).then(function(response) {
                        if(response.error) {
                            $scope.error = response.error;
                        } else {
                            // redirect to page after login
                            $window.location.href = '/account';
                        }
                    });
                }
            };

            function validate() {
                $scope.error = "";

                console.log("agree: " + $scope.agree);

                if(!_.size($scope.firstname)) {
                    $scope.error = "First name is required";
                    return false;
                }
                if(!_.size($scope.lastname)) {
                    $scope.error = "Last name is required";
                    return false;
                }
                if(!_.size($scope.email)) {
                    $scope.error = "Email is required";
                    return false;
                }
                if(_.size($scope.pass) < 6) {
                    $scope.error = "Password must be at least 6 characters";
                    return false;
                }
                if($scope.pass != $scope.passconfirm) {
                    $scope.error = "Passwords are not the same, passwords must match";
                    return false;
                }
                if(!$scope.agree) {
                    $scope.error = "Please read and accept the Terms and Conditions and our Privacy Policy";
                    return false;
                }

                return true;
            }

        }])
        .service('signupService', ['dataService', function (data) {
            this.signup = function(form) {
                // put url to signup here
                return data.post('/auth/signup', {form: form});
            };
        }]);
})(window.angular);