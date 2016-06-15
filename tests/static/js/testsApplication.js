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

App.controller('testCtrl', function($scope, $http, $routeParams, $interval, $timeout){
    var init = function(){
        $scope.currentOption = false;
        $http.get('/tests/' + $routeParams.id + '/')
            .then(function(response){
                console.log(response.data)
                $scope.test = response.data.test;
            })
    }

    var setTimer =function(){
        closeTimer();
        $scope.time = "00:00";

        var option = $scope.currentOption;
        if(option.time || $scope.test.time_completion){
            var time = option.time ? option.time : $scope.test.time_completion;
            var minutes = time - 1;
            var seconds = 60;
            $scope.timer = $interval(function(){
                seconds -= 1
                if (seconds < 0){
                    minutes -= 1;
                    seconds = 60;
                }

                $scope.time = minutes + " : " + seconds
            }, 1000)

            $scope.timerTimeout = $timeout(function(){
                $interval.cancel($scope.timer);
                $scope.checkTest();
            }, time * 60 * 1000)

        }
    }

    var closeTimer = function(){
        if($scope.timer){
            $interval.cancel($scope.timer);
            $timeout.cancel($scope.timerTimeout);
        }
    }

    $scope.startTest = function(option){
        function shuffle(a) {
            var j, x, i;
            for (i = a.length; i; i -= 1) {
                j = Math.floor(Math.random() * i);
                x = a[i - 1];
                a[i - 1] = a[j];
                a[j] = x;
            }
        }
        $scope.currentOption = option;
        shuffle($scope.currentOption.questions);
        angular.forEach($scope.currentOption.questions, function(question){
            shuffle(question.answers);
        })
        $scope.currentIndexQuestion = 0;
        $scope.currentQuestion = option.questions[$scope.currentIndexQuestion];
        closeTimer();
        setTimer();
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

    $scope.showHelp = function(){
        var help = $scope.currentOption.questions[$scope.currentIndexQuestion].help;
        if(help.length > 0 && $scope.test.helps){
            swal('Подсказка', help , 'info')
        }else{
            swal('Подсказка', 'В данном тесте или вопросе не предусмотрены', 'error')
        }
    }

    $scope.checkTest = function(){
        closeTimer();
        var userPoint = 0;
        var maxPoint = 0;
        //Проверка ответов и формирование балла
        angular.forEach($scope.currentOption.questions, function(question){
            var correctValue = true;
            maxPoint += question.point;

            angular.forEach(question.answers, function(answer){
                answer.error = false;
                answer.success = false;

                if (answer.selected && !answer.correct){
                    answer.error = true;
                    correctValue = false;
                }else if (!answer.selected && answer.correct){
                    correctValue = false;
                }else if (answer.selected && answer.correct){
                    answer.success = true;
                }
            })

            if(correctValue){
                userPoint += question.point;
            }
        })

        //Выведение процента
        var percent = userPoint * 100/ maxPoint;
        $scope.testData = {
            point: userPoint,
            maxPoint: maxPoint,
            percent: Math.round(percent)
        }
        //получаем оценку
        if (percent >= 0 && percent < $scope.test.two_mark){
            $scope.mark = 2;
            $scope.color = "error";
        }else if (percent >= $scope.test.two_mark && percent < $scope.test.three_mark){
            $scope.mark = 3;
            $scope.color = "warning";
        }else if (percent >= $scope.test.three_mark && percent < $scope.test.four_mark){
            $scope.mark = 4;
            $scope.color = "info";
        }else{
            $scope.mark = 5;
            $scope.color = "success";
        };

        $http.post('/tests/' + $scope.test.id + '/', {
            option: $scope.currentOption.id,
            questions: $scope.currentOption.questions,
            mark: $scope.mark,
            percent: percent
        }).then(function(response){
            console.log(response)
        })

    }

    $scope.optionsBack = function(){
        $scope.mark = false;
        angular.forEach($scope.currentOption.questions, function(question){
            angular.forEach(question.answers, function(answer){
                answer.selected = false;
            })
        })

        $scope.currentOption = false;
        $scope.currentIndexQuestion = false;
        $scope.currentQuestion = false;
        closeTimer();
    }

    $scope.restart = function(){
        $scope.mark = false;
        function shuffle(a) {
            var j, x, i;
            for (i = a.length; i; i -= 1) {
                j = Math.floor(Math.random() * i);
                x = a[i - 1];
                a[i - 1] = a[j];
                a[j] = x;
            }
        }
        shuffle($scope.currentOption.questions);
        angular.forEach($scope.currentOption.questions, function(question){
            shuffle(question.answers);
            angular.forEach(question.answers, function(answer){
                answer.selected = false;
            })
        })

        $scope.currentIndexQuestion = 0;
        $scope.currentQuestion = $scope.currentOption.questions[$scope.currentIndexQuestion];
        setTimer();
    }

    init()
})
