App = angular.module('profileApp', [])
    .config(['$httpProvider', function ($httpProvider) {
            $httpProvider.defaults.headers
                           .common['X-Requested-With'] = 'XMLHttpRequest';

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }])


App.filter('paginationFilter', function(){
        return function(page, pagination, items){
            var response = [];
            previousPage = page-1;
            previousLastIndex = pagination.countItems * previousPage;
            currentLastIndex = (pagination.countItems * page) - 1;
            for (i=0;i<items.length;i++){
                if (i >= previousLastIndex && i <= currentLastIndex){
                    response.push(items[i])
                }
            }

            return response;

        }
})

App.controller('ProfileCntr', function($scope, $http, $filter){
    var init = function(){
        $scope.loader = true;

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
                if ($scope.data.user.is_staff || $scope.data.user.is_superuser){
                    $scope.pagination.countItems = 1;
                    $scope.pagination.countPages = Math.ceil($scope.data.tests.length / $scope.pagination.countItems);
                }else{
                    $scope.pagination.countItems = 30;
                    $scope.pagination.countPages = Math.ceil($scope.data.tested_results.length / $scope.pagination.countItems);
                }

                for(i=1; i<= $scope.pagination.countPages; i++){
                    $scope.pagination.pages.push(i)
                }


                $scope.loader = false;
            })

        $scope.$watch('filteredData', function() {
            if ($scope.filteredData) {
                console.log($scope.filteredData);
                $scope.pagination.countPages = Math.ceil($scope.filteredData.length / $scope.pagination.countItems);
                if($scope.pagination.countPages){
                    $scope.pagination.pages.splice(0, $scope.pagination.pages.length);

                    for(i=1; i<= $scope.pagination.countPages; i++){
                        $scope.pagination.pages.push(i)
                    }

                    $scope.pagination.currentPage = 1;
                    //filters in controller
                    $filter('paginationFilter')(2,$scope.pagination,$scope.filteredData);
                    var data = $filter('filter')($scope.data.tests, {title : $scope.filters.title, category: { url: $scope.filters.category}});
                    console.log(data);
                    //end
                }
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

    $scope.downloadResult = function(id){
        $('#downloadResultForm').attr('action', '/profile/tested/'+id+'/').submit()
    }

    init()
})
