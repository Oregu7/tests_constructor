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
                    $scope.pagination.countItems = 5;
                }else{
                    $scope.pagination.countItems = 20;
                }

                filterAll(1);
                $scope.loader = false;
            })
    }

    var filterAll = function(page){
        if(!$scope.data.user.is_staff && !$scope.data.user.is_superuser){
           var filteredData = $filter('filter')($scope.data.tested_results, {
              option : { test : {title : $scope.filters.title, category : {url : $scope.filters.category} } }
           })
        }else{
           var filteredData = $filter('filter')($scope.data.tests, {title : $scope.filters.title, category: { url: $scope.filters.category}});
        }
        $scope.pagination.countPages = Math.ceil(filteredData.length / $scope.pagination.countItems);
        if($scope.pagination.countPages){
                $scope.pagination.pages.splice(0, $scope.pagination.pages.length);

                for(i=1; i<= $scope.pagination.countPages; i++){
                    $scope.pagination.pages.push(i)
                }

                //filters in controller
                $scope.filteredData = $filter('paginationFilter')(page ,$scope.pagination,filteredData);
        }else{
            $scope.filteredData.splice(0,$scope.filteredData.length);
        }

    }

    $scope.setCategory = function(category){
        $scope.pagination.currentPage = 1;
        $scope.filters.category = category;
        filterAll(1);
    }

    $scope.setPage = function(page){
        $scope.pagination.currentPage = page;
        filterAll(page);
    }

    $scope.searchTitle = function(){
        $scope.pagination.currentPage = 1;
        filterAll(1);
    }

    $scope.downloadResult = function(id){
        $('#downloadResultForm').attr('action', '/profile/tested/'+id+'/').submit()
    }

    $scope.next = function(){
        var nextPage = $scope.pagination.currentPage + 1;
        if(nextPage <= $scope.pagination.countPages){
            $scope.pagination.currentPage = nextPage;
            filterAll(nextPage);
        }else{
            $scope.pagination.currentPage = 1;
            filterAll(1);
        }
    }

    $scope.back = function(){
        var previousPage = $scope.pagination.currentPage - 1;
        if (previousPage != 0){
            $scope.pagination.currentPage = previousPage;
            filterAll(previousPage);
        }else{
            $scope.pagination.currentPage = $scope.pagination.countPages;
            filterAll($scope.pagination.countPages);
        }
    }

    init()
})
