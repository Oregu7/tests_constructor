App = angular.module('profileApp', [])
    .config(['$httpProvider', function ($httpProvider) {
            $httpProvider.defaults.headers
                           .common['X-Requested-With'] = 'XMLHttpRequest';

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }])

App.controller('ProfileCntr', function($scope, $http){
    var init = function(){
        $scope.filters = {
            title: '',
            category: '',
            name: ''
        };

        $scope.pagination = {
            countItems: 2,
            countPages: 1,
            currentPage: 1,
            pages: []
        };

        $http.get('')
            .then(function(response){
                $scope.data = response.data;
                $scope.pagination.countPages = Math.ceil($scope.data.tests.length / $scope.pagination.countItems);
                for(i=1; i<= $scope.pagination.countPages; i++){
                    $scope.pagination.pages.push(i)
                }
            })

        $scope.$watch('filteredData', function() {
            if ($scope.filteredData) {
                console.log($scope.filteredData);
            }
        });

    }

    $scope.setCategory = function(category){
        $scope.pagination.currentPage = 1;
        $scope.filters.category = category;
    }

    $scope.setPage = function(page){
        $scope.pagination.currentPage = page;
    }

    $scope.paginationFilter = function(page){
        return function(item, index){
            previousPage = page-1;
            previousLastIndex = $scope.pagination.countItems * previousPage;
            currentLastIndex = ($scope.pagination.countItems * page) - 1;
            if (index >= previousLastIndex && index <= currentLastIndex){
                return true
            }else{
                return false
            }
        }
    }

    init()
})
