var App = angular.module('testAccess', []);

App.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.headers
               .common['X-Requested-With'] = 'XMLHttpRequest';
}]);

App.controller('groupsAccess', function($scope, $http){
    var init = function(){
        $scope.filters = {
            spec: '',
            course: '',
            type: '',
            search: {}
        }

        $http.get('').then(function(response){
            response.data.specs.unshift({name: 'Все', code: 1});
            response.data.courses.unshift('Все');
            $scope.data = response.data;

            $scope.filteredGroups = $scope.data.groups;
            //Устанавливаем первоначальное значение фильтров
            $scope.filters.spec = $scope.data.specs[0].code;
            $scope.filters.course = $scope.data.courses[0];
            $scope.filters.type = 'all';
        })

    }

    var filterGroups = function(key, value){
        var result = []
        angular.forEach($scope.data.groups, function(group){
            if ((key == 'specialization' && value == 1) || (key == 'course' && value == 'Все')){
                result.push(group)
            }else if(group[key] == value){
                result.push(group)
            }

        })

        return result;
    }

    $scope.setSpec = function(specID){
        $scope.filters.spec = specID;
        $scope.filteredGroups = filterGroups('specialization', specID);
    }

    $scope.setCourse = function(courseID){
        $scope.filters.course = courseID;
        $scope.filteredGroups = filterGroups('course', courseID);
    }

    $scope.setType = function(type){
        $scope.filters.type = type;
    }

    init();
})