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
        $http.get('')
            .then(function(response){
                $scope.data = response.data;
            })
    }

    init();

    $scope.addOption = function(){
        var option = {number: $scope.data.options.length + 1, action:'addOption'}
        $http.post('', option)
            .then(function(response){
                option.id = response.data.id;
                option.questions = [];
                $scope.data.options.push(option);
            })
    }

    $scope.setOption = function(index){
        $scope.currentOption = index;
    }
})
