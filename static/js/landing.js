(function(){
    var app = angular.module('landing', []);

    app.directive('landingPage', function(){
        return {
            restrict: 'E',
            templateUrl: '/static/html/landing_page.html',
            controller: function($scope){
                $scope.desc = 'Tasks MG - is the modern web tasks management service for create/manage tasks and build own team';
                $scope.about = 'My name is Bogdan Piven. I am a 24 years old, and I am fond of sports and web - developing.'
                $scope.features = [
                    'Manage your tasks',
                    'Set deadline for tasks',
                    'Build your team via Facebook',
                    'Assign/re-assign tasks to your teammates'
                ];
            }
        }
    });
})();
