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

    .config(['$compileProvider',
    function ($compileProvider) {
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|file|blob):/);
    }]);

App.filter('dateRangeFilter', function(){

})

App.controller('TestedsCtr', function($scope, $http, $rootScope){
    var init = function(){
        $scope.filters = {
            specialization: '',
            course: '',
            group: '',
            option: '',
            mark: '',
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
            })

        $rootScope.$on('$viewContentLoaded',function(){
            //$('.dropdown').dropdown();
            $('.accordion').accordion();
        });
    }

    $scope.dateRangeFilter = function(dateF, dateL){
        return function(item){
            var item_date = moment(item.date).format("DD.MM.YYYY");
            if(dateF && !dateL){
                var df = moment(dateF).format("DD.MM.YYYY");
                if (item_date >= df){
                    return true;
                }else{
                    return false;
                }
            }else if (!dateF && dateL){
                var ds = moment(dateL).format("DD.MM.YYYY");
                if (item_date <= ds){
                    return true
                }else{
                    return false
                }
            }else if (dateF && dateL){
                var df = moment(dateF).format("DD.MM.YYYY");
                var ds = moment(dateL).format("DD.MM.YYYY");
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