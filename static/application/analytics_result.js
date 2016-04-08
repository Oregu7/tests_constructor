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

    init();
})
