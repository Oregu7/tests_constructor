var TemplateDIR = '/tests/page/';
var App = angular.module('testsApp', ['ngRoute'])
    .config(function($routeProvider){
        $routeProvider
            .when('/', {
                templateUrl: TemplateDIR + 'tests/',
                controller: 'testsCtrl'
            })

            .when('/:id', {
                templateUrl: TemplateDIR + 'test/',
                controller: 'testCtrl'
            })

            .otherwise({
                redirectTo: '/'
            })
    })

    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        //$httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

App.controller('testsCtrl', function($scope, $http){
    var init = function(){
        $scope.filters = {
            name: '',
            category: ''
        }

        $http.get('')
            .then(function(response){
                $scope.data = response.data;
            })
    }


    $scope.setCategory = function(category){
        $scope.filters.category= category;
    }

    init()
})

App.controller('testCtrl', function($scope, $http, $routeParams){
    var init = function(){
        $scope.currentOption = false;

        $http.get('/tests/' + $routeParams.id + '/')
            .then(function(response){
                console.log(response.data)
                $scope.test = response.data.test;
            })
    }

    $scope.startTest = function(option){
        $scope.currentOption = option;
        $scope.currentIndexQuestion = 0;
        $scope.currentQuestion = option.questions[$scope.currentIndexQuestion];
    }

    $scope.next = function(){
        var nextIndex = $scope.currentIndexQuestion + 1;
        if(nextIndex > $scope.currentOption.questions.length - 1){
            $scope.currentIndexQuestion = 0;
            $scope.currentQuestion = $scope.currentOption.questions[$scope.currentIndexQuestion];
        }else{
            $scope.currentIndexQuestion = nextIndex;
            $scope.currentQuestion = $scope.currentOption.questions[$scope.currentIndexQuestion];
        }


    }

    $scope.back = function(){
        var prevIndex = $scope.currentIndexQuestion - 1;
        if (prevIndex < 0){
            $scope.currentIndexQuestion = $scope.currentOption.questions.length - 1;
            $scope.currentQuestion = $scope.currentOption.questions[$scope.currentIndexQuestion];
        }else{
            $scope.currentIndexQuestion = prevIndex;
            $scope.currentQuestion = $scope.currentOption.questions[$scope.currentIndexQuestion];
        }


    }

    init()
})
