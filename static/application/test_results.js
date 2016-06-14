var TemplateDIR = '/profile/page/'
App = angular.module('testResults', ['ngRoute'])
    .config(function($routeProvider){
        $routeProvider
            .when('/',{
                templateUrl : TemplateDIR + 'probationers',
                controller: 'TestedsCtr'
            })
            .when('/:id', {
                templateUrl: TemplateDIR + 'probationer',
                controller: 'TestedCtr'
            })

            .otherwise({
                redirectTo: '/'
            })
    })

    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])


App.factory('loaderFactory', function(){
    return {
        active: true
    }
})

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

App.filter('dateFilter', function(){
    return function(dateF, dateL, items){
        var response = [];
        for (i=0; i<items.length; i++){
            var item_date = moment(items[i].date).format("YYYY-MM-DD");

            if(dateF && !dateL){
                var df = moment(dateF).format("YYYY-MM-DD");
                if (item_date >= df){
                    response.push(items[i])
                }
            }else if (!dateF && dateL){
                var ds = moment(dateL).format("YYYY-MM-DD");
                if (item_date <= ds){
                    response.push(items[i])
                }
            }else if (dateF && dateL){
                var df = moment(dateF).format("YYYY-MM-DD");
                var ds = moment(dateL).format("YYYY-MM-DD");
                if (item_date >= df && item_date <= ds){
                    response.push(items[i])
                }
            }else{
                response.push(items[i])
            }
        }

        return response
    }
})


App.controller('LoaderCtr', function($scope, loaderFactory){
    $scope.loader = loaderFactory;
})

App.controller('TestedsCtr', function($scope, $http, $rootScope, loaderFactory, $filter){
    var init = function(){
        loaderFactory.active = true;
        $scope.filters = {
            sortField: false,
            reverse: false,
            specialization: '',
            course: '',
            group: '',
            option: '',
            mark: '',
            lastName:'',
            testeds: '',
            date: {
                first: '',
                last: ''
            }
        }

        $scope.pagination = {
            countItemsAll: [2, 3, 5, 10, 20, 30, 50, 100],
            countItems: 10,
            countPages: 1,
            currentPage: 1,
            pages: []
        };

        $http.get('')
            .then(function(response){
                $scope.data = response.data;
                loaderFactory.active = false;
                filterAll(1);
            })

        $rootScope.$on('$viewContentLoaded',function(){
            //$('.dropdown').dropdown();
            $('.accordion').accordion();
        });
    }

    //фильтрация
    var filterAll = function(page){
        var filteredData = $filter('filter')($scope.data.testeds,
            {
                user : {
                    last_name: $scope.filters.lastName,
                    study_group : {
                        id : $scope.filters.group, course : $scope.filters.course,
                        specialization : {
                            code: $scope.filters.specialization
                        }
                    }
                },
                option : {id : $scope.filters.option},
                mark : $scope.filters.mark
            }
        );

        filteredData = $filter('dateFilter')($scope.filters.date.first, $scope.filters.date.last, filteredData);
        filteredData = $filter('orderBy')(filteredData, $scope.filters.sortField, $scope.filters.reverse);
        //количество найденных данных
        $scope.FilteredDataAll = filteredData;
        //пагинация

        $scope.pagination.countPages = Math.ceil(filteredData.length / $scope.pagination.countItems);
        if($scope.pagination.countPages){
                $scope.pagination.pages.splice(0, $scope.pagination.pages.length);
                $scope.pagination.currentPage = page;

                if($scope.pagination.countPages > 10){
                    if(($scope.pagination.countPages - $scope.pagination.currentPage) <= 9){
                        $scope.pagination.pages.push(1);
                        $scope.pagination.pages.push("..");
                        for(i=$scope.pagination.countPages - 9; i<= $scope.pagination.countPages; i++){
                            $scope.pagination.pages.push(i)
                        }
                    }else if($scope.pagination.currentPage > 10){
                        var tenth = Math.floor($scope.pagination.currentPage/10) * 10;
                        $scope.pagination.pages.push(1);
                        $scope.pagination.pages.push("..");
                        for(i=tenth; i<= tenth + 9; i++){
                            $scope.pagination.pages.push(i)
                        }
                        $scope.pagination.pages.push("...")
                        $scope.pagination.pages.push($scope.pagination.countPages)
                    }else{
                        for(i=1; i<= 10; i++){
                            $scope.pagination.pages.push(i)
                        }
                        $scope.pagination.pages.push("..")
                        $scope.pagination.pages.push($scope.pagination.countPages)
                    }

                }else{
                    for(i=1; i<= $scope.pagination.countPages; i++){
                        $scope.pagination.pages.push(i)
                    }
                }

                //filters in controller
                $scope.filteredData = $filter('paginationFilter')(page ,$scope.pagination,filteredData);
        }else{
            $scope.filteredData = [];
        }

    }

    $scope.dateRangeFilter = function(dateF, dateL){
        return function(item){
            var item_date = moment(item.date).format("YYYY-MM-DD");
            if(dateF && !dateL){
                var df = moment(dateF).format("YYYY-MM-DD");
                if (item_date >= df){
                    return true;
                }else{
                    return false;
                }
            }else if (!dateF && dateL){
                var ds = moment(dateL).format("YYYY-MM-DD");
                if (item_date <= ds){
                    return true
                }else{
                    return false
                }
            }else if (dateF && dateL){
                var df = moment(dateF).format("YYYY-MM-DD");
                var ds = moment(dateL).format("YYYY-MM-DD");
                if (item_date >= df && item_date <= ds){
                    return true
                }else{
                    return false;
                }
            }else{
                return true
            }
        }
    }

    $scope.sendTesteds = function(){
        var testeds = $scope.FilteredDataAll.map(function(tested){
            return tested.id
        })

        if(testeds.length){
          $("input[name=testeds]").val(testeds.join());
          $('#testedsForm').attr('action', "/profile/print/results/" + $scope.data.test + "/").submit()
        }else{
            swal('Ошибка!', 'Количество найденных данных равно 0', 'error');
        }


    }

    $scope.printResultTested = function(tested){
        $('#printResultTested').attr('action', '/profile/tested/' + tested + '/').submit()
    }

    $scope.sortByField = function(fieldName){
        if(fieldName == $scope.filters.sortField){
            $scope.filters.reverse = !$scope.filters.reverse;
        }else{
            $scope.filters.sortField = fieldName;
            $scope.revers = false;
        }

        filterAll(1);
    }

    $scope.changeCountItems = function(){
        filterAll(1);
    }

    $scope.changeFilters = function(){
        filterAll(1);
    }

    $scope.setPage = function(page){
        if(page != '..' && page != '...'){
           $scope.pagination.currentPage = page;
           filterAll(page);
        }
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

App.controller('TestedCtr', function($scope, $http, $routeParams, loaderFactory){
    var init = function(){
        loaderFactory.active = true;
        $http.get('/profile/tested/' + $routeParams.id + '/')
            .then(function(response){
                $scope.tested = response.data.tested;
                loaderFactory.active = false;
            })
    }

    $scope.printResult = function(){
        $('#printResult').attr('action', '/profile/tested/' + $routeParams.id + '/').submit()
    }

    init()
})