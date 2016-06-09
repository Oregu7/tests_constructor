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

App.controller('TestedsCtr', function($scope, $http, $rootScope){
    var init = function(){
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

        $http.get('')
            .then(function(response){
                //response.data.specializations.unshift({name: 'Все', code: ''});
                response.data.courses.unshift({id: '', name: 'Все'});
                $scope.data = response.data;
                $scope.loader = false;
            })

        $rootScope.$on('$viewContentLoaded',function(){
            //$('.dropdown').dropdown();
            $('.accordion').accordion();
        });
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
        var testeds = $scope.filteredTesteds.map(function(tested){
            return tested.id
        })

        $("input[name=testeds]").val(testeds.join());
        $('#testedsForm').attr('action', "/profile/print/results/" + $scope.data.test + "/").submit()

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
    }

    init()
})

App.controller('TestedCtr', function($scope, $http, $routeParams){
    var init = function(){
        $http.get('/profile/tested/' + $routeParams.id + '/')
            .then(function(response){
                $scope.tested = response.data.tested
            })
    }

    $scope.printResult = function(){
        $('#printResult').attr('action', '/profile/tested/' + $routeParams.id + '/').submit()
    }

    init()
})