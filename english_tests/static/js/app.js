var TemplatesDIR = '/english_tests/'
var App = angular.module('testProject',['ngRoute'])
    .config(function($routeProvider){
        $routeProvider
            .when("/",{
                templateUrl:TemplatesDIR + 'eng_tests.html'
            })

            .when("/test/:id",{
                templateUrl:TemplatesDIR + 'eng_test.html',
                controller: 'main'
            })

            .when('/test/:id/questions',{
                templateUrl:TemplatesDIR + 'eng_questions.html',
                controller: 'main'
            })

            .otherwise({
                redirectTo:"/"
            })
    })

App.controller('main', function($scope, $http, $routeParams){
    $scope.init = function(){
        if ($scope.tests === undefined){
            $http.get('/api/tests/English/').then(function(res){
                $scope.tests = res.data;
            })
        };

        if ($routeParams.id){
            $scope.current_test = $scope.tests[$routeParams.id];
        }

    }

    $scope.getQuestions = function(){
        $http.get('/api/tests/' + $scope.current_test.id + '/questions/').then(function(res){
            $scope.questions = res.data;
        })
    }

    $scope.init();

})
