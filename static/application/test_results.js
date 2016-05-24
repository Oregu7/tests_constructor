var TemplateDIR = '/profile/page/'
App = angular.module('testResults', ['ngRoute'])
    .config(function($routeProvider){
        $routeProvider
            .when('/',{
                templateUrl : TemplateDIR + 'probationers',
                controller: 'TestedsCtr'
            })
            .when('/:id', {
                templateUrl: TemplateDIR + 'probationer',
                controller: 'TestedCtr'
            })

            .otherwise({
                redirectTo: '/'
            })
    })

    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);


App.controller('TestedsCtr', function($scope, $http){
    var init = function(){
        $scope.filters = {
            
        }

        $http.get('')
            .then(function(response){
                $scope.testeds = response.data.probationers;
            })
    }

    init()
})

App.controller('TestedCtr', function($scope, $http, $routeParams){

})