var App = angular.module('testAccess', []);

App.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.headers
               .common['X-Requested-With'] = 'XMLHttpRequest';
}]);

App.controller('groupsAccess', function($scope, $http){
    var init = function(){
        $scope.filters = {
            specialization: '',
            course: '',
            access: '',
            name: ''
        }

        $http.get('').then(function(response){
            response.data.specs.unshift({name: 'Все', code: ''});
            response.data.courses.unshift({id: '', name: 'Все'});
            $scope.data = response.data;

            //Устанавливаем первоначальное значение фильтров
            $scope.filters.specialization = $scope.data.specs[0].code;
            $scope.filters.course = $scope.data.courses[0].id;
        })

    }

    $scope.setSpec = function(specID){
        $scope.filters.specialization = specID;
        //$scope.filteredGroups = filterGroups('specialization', specID);
    }

    $scope.setCourse = function(courseID){
        $scope.filters.course = courseID;
        //$scope.filteredGroups = filterGroups('course', courseID);
    }

    $scope.setAccess = function(access){
        $scope.filters.access = access;
    }

    $scope.closeAllAccess = function(){
        $http.delete('')
                .then(function(resp){
                    angular.forEach($scope.data.groups, function(group){
                        group.access = false;
                    })
                })
    }

    $scope.changeAccess = function(group){
        if(group.access){
            $.post('',{group: group.id, append: true})
                .success(function(response){
                    console.log(response)
                })
        }else{
            $.post('',{group: group.id, append: false})
                .success(function(response){
                    console.log(response)
                })
        }

    }

    init();
})