var App = angular.module('appAuth', []);

App.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.headers
               .common['X-Requested-With'] = 'XMLHttpRequest';

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

App.controller('AuthController', function($scope, $http, $q){
    var init = function(){
        $scope.loader = false;
        var group = 'I3KO2UD2ZK2';
        $scope.auth = {
            login:'',
            password: '',
            error: false
        }

        $scope.registration = {
            login:'',
            password: '',
            firstName:'',
            lastName:'',
            errors:{
                login:'',
                password: '',
                firstName:'',
                lastName:''
            },
            errorMessage: false
        }
    }

    $scope.searchGroup = function(){
        $scope.loader = true;
        $http.post('/auth/check/', {secret_key: $scope.secret_key, action:'group'})
            .then(function(response){
                $scope.check = response.data;
                $scope.loader = false;
            })
    }

    $scope.authUser = function(){
        data = {login: $scope.auth.login, password: $scope.auth.password}
        $http.post('/auth/login/', data)
            .then(function(response){
                response = response.data;
                if(response.auth){
                    window.location.assign('/profile/')
                }else{
                    $scope.auth.error = response.error;
                    $scope.auth.password = '';
                }
            })
    }

    var clearErrors = function(){
        $scope.registration.errorMessage = false;
        angular.forEach($scope.registration.errors, function(item, key){
            $scope.registration.errors[key] = '';
        })
    }

    var chechRegistration = function(){
        var deferred = $q.defer();
        var promise = deferred.promise;
        promise.then(function(){
               angular.forEach($scope.registration, function(item, key){
                if(key == 'login' || key == 'password' || key == 'firstName' || key == 'lastName'){
                    if(!$scope.registration[key].length){
                        $scope.registration.errors[key] = "Вы не указали данные";
                        $scope.registration.errorMessage = true;
                    }

                   if(key == 'login'){
                       var r=/[^A-Z-a-z-0-9]/g;
                       if($scope.registration[key].length < 3 || $scope.registration[key].length > 20){
                            $scope.registration.errors[key] = "Допустимая длинна от 3 до 20 символов";
                            $scope.registration.errorMessage = true;
                       }else if(r.test($scope.registration[key])){
                            $scope.registration.errors[key] = "Введены недопустимые символы. Разрешены латинские буквы и цифры";
                            $scope.registration.errorMessage = true;
                       }else{
                           var data = {login: $scope.registration[key], action:'username'}
                           $http.post('/auth/check/', data)
                               .then(function(response){
                                   response = response.data;
                                   if(response.username){
                                       $scope.registration.errors[key] = "Данный логин уже занят!";
                                       $scope.registration.errorMessage = true;
                                   }
                               })
                       }

                   }else if(key == 'password'){
                        var r=/[^A-Z-a-z-0-9]/g;
                        if($scope.registration[key].length < 6 || $scope.registration[key].length > 30){
                            $scope.registration.errors[key] = "Допустимая длинна от 6 до 30 символов";
                            $scope.registration.errorMessage = true;
                        }else if(r.test($scope.registration[key])){
                            $scope.registration.errors[key] = "Введены недопустимые символы. Разрешены латинские буквы и цифры";
                            $scope.registration.errorMessage = true;
                        }

                   }else if(key == 'firstName' || key == 'lastName'){
                       var r=/[^А-Я-а-я]/g;
                       if($scope.registration[key].length < 2 || $scope.registration[key].length > 30){
                           $scope.registration.errors[key] = "Допустимая длинна от 2 до 30 символов";
                           $scope.registration.errorMessage = true;
                       }else if(r.test($scope.registration[key])){
                           $scope.registration.errors[key] = "Введены недопустимые символы. Разрешена только кириллица";
                           $scope.registration.errorMessage = true;
                       }
                   }
                }
            })
        }).then(function(){
            if(!$scope.registration.errorMessage){
                data = {
                    login: $scope.registration.login,
                    password: $scope.registration.password,
                    firstName: $scope.registration.firstName,
                    lastName: $scope.registration.lastName,
                    group: $scope.check.group.id
                }

                $http.post('/auth/registration/', data)
                    .then(function(response){
                        if(response.data.registration){
                            window.location.assign('/profile/');
                        }
                    })
            }
        })

        deferred.resolve();
    }

    $scope.registrationUser = function(){
        clearErrors();
        chechRegistration();
    }

    init()
})
