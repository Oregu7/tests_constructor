var TemplatesDIR = '/analytics/'
var App = angular.module('testProject',['ngRoute', 'ui.materialize'])
    .config(function($routeProvider){
        $routeProvider
            .when("/",{
                templateUrl:TemplatesDIR + 'analytics_tests.html'
            })

            .when("/test/:id",{
                templateUrl:TemplatesDIR + 'analytics_test.html',
                controller: 'main'
            })

            .when('/test/:id/questions',{
                templateUrl:TemplatesDIR + 'analytics_questions.html',
                controller: 'main'
            })

            .otherwise({
                redirectTo:"/"
            })
    })

App.controller('main', function($scope, $http, $routeParams){
    $scope.init = function(){
        if ($scope.tests === undefined){
            $http.get('/api/tests/analytics/').then(function(res){
                $scope.tests = res.data;
            })
        };

        if ($routeParams.id){
            $http.get('/api/tests/'+ $routeParams.id+'/').then(function(res){
                $scope.current_test = res.data;
            })
        }

        $scope.select = {};

    };

    $scope.startTest = function(){
        $scope.courses = [1,2,3,4];

        $http.get('/api/rolies/').then(function(res){
            $('#modal1').openModal();
            $scope.rolies = res.data;
        });

        $http.get('/api/specializations/').then(function(res){
            $scope.specializations = res.data;
        })
    };

    $scope.next =function(){
        if(($scope.select.role && $scope.select.specialization && $scope.select.course)){
            if($scope.mark){
                $scope.mark = 0;
                angular.forEach($scope.questions, function(question){
                    question.current_answer = false;
                });
                console.log($scope.questions)
            }else{
                $http.get('/api/tests/' + $scope.current_test.id + '/questions/').then(function(res){
                $scope.questions = res.data;
                    angular.forEach($scope.questions, function(question){
                        question.current_answer = false;
                    });
                })
            }

        }

    }

    $scope.cancel = function(){
        $scope.select = {}
    }

    $scope.restart = function(){
        $scope.select = {};
        $('#modal1').openModal();
    };

    $scope.check_test = function(){
        var data = [];
        angular.forEach($scope.questions, function(question){
            data.push({id: question.id, current_answer:question.current_answer})
        });

        $.post('/analytics/save/',
            {
                data: JSON.stringify(data),
                tested: JSON.stringify($scope.select),
                test: $scope.current_test.id
            },
            function(response){
                console.log(response);
                console.log(data);
            }
        )

        $scope.mark = "Данные успешно сохранены";
        scroll(0,0);

    };

    $scope.init();

})
