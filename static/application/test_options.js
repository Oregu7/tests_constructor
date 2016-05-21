var App = angular.module('testOptions', []);

App.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.headers
               .common['X-Requested-With'] = 'XMLHttpRequest';

  //$httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

App.controller('OptionsCtr', function($scope, $http){
    var init = function(){
        $scope.currentOption = false;
        $scope.allQuestion =  true;

        $scope.filters = {
            inOption: '',
            text: '',
            point:''
        }

        $http.get('')
            .then(function(response){
                $scope.data = response.data;
            })
    }

    $scope.addOption = function(){
        var option = {number: $scope.data.options.length + 1, action:'addOption'}
        $http.post('', option)
            .then(function(response){
                option.id = response.data.id;
                option.questions = [];
                $scope.data.options.push(option);
            })
    }

    $scope.deleteOption = function(){
        var option = $scope.data.options[$scope.currentOption];
        var data = {option: option.id, action: 'deleteOption'}
        $http.post('', data)
            .then(function(response){
                $scope.data.options.splice($scope.currentOption, 1);
                $scope.currentOption = false;
            })
    }

    $scope.setInOption = function(value){
        $scope.filters.inOption = value;
    }

    var searchQuestion = function(search_item, questions){
        var response = {result: false, index: ''};
        angular.forEach(questions, function(question, index){
            if(question.id == search_item.id){
                response = {result: true, index: index};
            }
        })

        return response
    }

    $scope.setOption = function(index){
        $scope.currentOption = index;
        $scope.allQuestion = true;

        var option = $scope.data.options[index];
        //Проверяем какие вопросы входят в данный вариант
        angular.forEach($scope.data.questions, function(question){
            question.inOption = searchQuestion(question, option.questions).result;
        })
    }

    $scope.changeQuestion = function(question){
        var option = $scope.data.options[$scope.currentOption];
        var data = {
            option: option.id,
            question: question.id
        }

        if(question.inOption){
            option.questions.push(question);
            data.action = "addQuestion";

            $http.post('', data)
                .then(function(response){
                    console.log(response.data)
                })
        }else{
            data.action = "deleteQuestion";

            $http.post('', data)
                .then(function(response){
                    console.log(response.data)
                })

            var result = searchQuestion(question, option.questions);
            option.questions.splice(result.index, 1);
        }

    }

    $scope.clearQuestions = function(){
        var option = $scope.data.options[$scope.currentOption];
        $http.post('', {option: option.id, action: 'deleteAllQuestions'})
            .then(function(response){
                $scope.data.options[$scope.currentOption].questions = [];
                angular.forEach($scope.data.questions, function(question){
                    question.inOption = false;
                })
            })

    }

    $scope.changeSelectAll = function(){
        var option = $scope.data.options[$scope.currentOption];
        option.questions = [];

        if($scope.allQuestion){
            $http.post('', {option: option.id, questions: $scope.data.questions, action: 'addAllQuestions'})
                .then(function(response){
                    console.log(response)
                })

            angular.forEach($scope.data.questions, function(question){
                question.inOption = true;
                option.questions.push(question);
            })

            $scope.allQuestion = false
        }else{
            $scope.clearQuestions();
            $scope.allQuestion = true;
        }

    }

    init();
})
