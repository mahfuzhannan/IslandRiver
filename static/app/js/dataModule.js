/**
 * Created by mafz on 21/10/2016.
 */
angular.module('app.data', [])
    .service('dataService', ['$http', function ($http) {
        this.get = function (url, params) {
            return this.http('GET', url, params)
        };

        this.post = function (url, data) {
            return this.http('POST', url, {}, data)
        };

        this.delete = function (url, params) {
            return this.http('DELETE', url, params);
        };

        this.put = function (url, data) {
            return this.http('PUT', url, {}, data);
        };

        this.patch = function (url, data) {
            return this.http('PATCH', url, {}, data);
        };

        this.http =  function (method, url, params, data) {
            return $http({method:method, url:url, params:params, data:data})
                .then(function successCallback(response) {
                    return response.data;
                }, function errorCallback(response) {
                    return response.data;
                });
        };
}]);