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
        if ($scope.countries === undefined){
            $http.get('/api/countries/').then(function(res){
                $scope.countries = res.data;
            })
        };

        if ($routeParams.id){
            $http.get('/api/tests/'+ $routeParams.id+'/').then(function(res){
                $scope.current_test = res.data;
            })
        }

    };

    $scope.getQuestions = function(){
        $http.get('/api/tests/' + $scope.current_test.id + '/questions/').then(function(res){
            $scope.questions = res.data;
        })
    };

    $scope.restart = function(){
        $scope.mark = 0;
        angular.forEach($scope.questions, function(question){
            angular.forEach(question.answers, function(answer){
                answer.error = false;
                answer.success = false;
                answer.selection = false;
            })
        })
    };

    $scope.check_test = function(){
        var point = 0;
        var max_point = 0;
        angular.forEach($scope.questions, function(question){
                var correct_value = true;
                max_point += question.point;

                angular.forEach(question.answers, function(answer){
                    answer.error = false;
                    answer.success = false;

                    if (answer.selection && !answer.correct){
                        answer.error = true;
                        correct_value = false;
                    }else if ((answer.selection === undefined || !answer.selection) && answer.correct){
                        correct_value = false;
                    }else if(answer.selection && answer.correct){
                        answer.success = true;
                    }
                });

                if (correct_value){
                    point += question.point;
                }
        });

        //Получение процента
        var percent = point * 100/ max_point;
        console.log(percent,max_point, point)
        $scope.mark = 5;
        //получаем оценку
        if (percent >= 0 && percent < $scope.current_test.two_mark){
            $scope.mark = 2;
        }else if (percent >= $scope.current_test.two_mark && percent < $scope.current_test.three_mark){
            $scope.mark = 3;
        }else if (percent >= $scope.current_test.three_mark && percent < $scope.current_test.four_mark){
            $scope.mark = 4;
        };

        scroll(0,0)
    };

    $scope.init();

})
