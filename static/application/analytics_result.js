var App = angular.module('analytics_result',['ui.materialize'])
    .config([
        '$httpProvider',
        function($httpProvider){
            $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        }
    ])
    .run(['$http', function($http){
        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }]);

App.controller('main', function($scope, $http){
    var init = function(){
        $scope.select = {
            role: '',
            specialization: '',
            course: ''
        };
        $scope.date = {
            last: '',
            first: ''
        };
        $scope.test = $('#test_header').attr('data-testID');
        $scope.courses = [1,2,3,4];

        $http.get('/api/rolies/').then(function(res){
            $scope.rolies = res.data;
        });

        $http.get('/api/specializations/').then(function(res){
            $scope.specializations = res.data;
        })

        var currentTime = new Date();
        $scope.month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
        $scope.monthShort = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Нояб', 'Дек'];
        $scope.weekdaysFull = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
        $scope.weekdaysLetter = ['В', 'П', 'В', 'С', 'Ч', 'П', 'С'];
        $scope.today = 'Сегод';
        $scope.clear = 'Очист';
        $scope.close = 'Закр';

    }

    $scope.show_data = function(){
        $http.post('', {'tested': $scope.select, 'date': $scope.date})
            .then(function(resp){
                console.log(resp)
            })

        console.log($scope.select);
        console.log($scope.date);
    }


    $scope.create_url = function(data){
        var url = '/analytics/'+data+'/test/'+$scope.test;

        var check_empty = function(param){
            if(param == ""){
                return "all"
            }
            else{
                return param
            }

        }

        var add_url = function (url, param){
           return url + param;
        }

        var role = check_empty($scope.select.role);
        var spec = check_empty($scope.select.specialization);
        var course = check_empty($scope.select.course);
        var date_f = check_empty($scope.date.first);
        var date_l = check_empty($scope.date.last);

        url = add_url(url, '/role/' + role);
        url = add_url(url, '/spec/' + spec);
        url = add_url(url, '/course/' + course);
        url = add_url(url, '/date_f/' + date_f);
        url = add_url(url, '/date_l/' + date_l + '/');
        window.location.assign(url);
        console.log(url)

    }

    init();
})
