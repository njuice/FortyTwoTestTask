(function(){

    var app = angular.module('team', ["ngCookies", 'ngRoute', "ngResource", "ngFacebook", "cgNotify", "ui.bootstrap.modal"]);

    // Config $http for django backend
    app.config(function($httpProvider , $interpolateProvider, $resourceProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $resourceProvider.defaults.stripTrailingSlashes = false
    });

    app.config( function( $facebookProvider ) {
        $facebookProvider.setAppId('392682690927802');
    });

    app.run(function($rootScope){
       (function(d, s, id){
             var js, fjs = d.getElementsByTagName(s)[0];
             if (d.getElementById(id)) {return;}
             js = d.createElement(s); js.id = id;
             js.src = "//connect.facebook.net/en_US/sdk.js";
             fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    });

    app.factory('Teams', ['$http', function($http){

        var Teams = function(data){
            angular.extend(this, data)
        };

        Teams.getAll = function(userId) {
            return $http.get('/api/v1/teams/?format=json&owner=' + userId).then(function(response){
                return response;
            })
        };

        Teams.get = function(id) {
            return $http.get('/api/v1/teams/' + id + '/?format=json');
        };

        Teams.save = function(tm) {
            var url = '/api/v1/teams/?format=json';
            return $http.post(url, tm).error(function(data){
                console.log(data);
            });
        };

        Teams.remove = function(id) {
            return $http.delete('/api/v1/teams/' + id + '/?format=json');
        };
        return Teams;

    }]);

    app.factory('Teammates', ['$http', function($http){

        var Teammates = function(data){
            angular.extend(this, data)
        };

        Teammates.get = function(id) {
            return $http.get('/api/v1/teammates/' + id + '/?format=json');
        };

        Teammates.save = function(tm) {
            var url = '/api/v1/teammates/?format=json';
            return $http.post(url, tm).error(function(data){
                console.log(data);
            });
        };

        Teammates.remove = function(tm) {
            return $http.delete('/api/v1/teammates/' + tm.id + '/?format=json');
        };
        return Teammates;

    }]);

    app.service("teammatesList", function TeammatesList(){
        var teammates = this;
        teammates.list = [];
    });

    app.directive('inviteFriends', function (notify) {
        return {
            restrict: 'E',
            templateUrl: '/static/html/invite_friends.html',
            controller: function($log, $scope, $http, $facebook){
                this.list = [];

                var that = this;
                // Fetch our facebook friends that we can invite
                $http.get('/invitable/', {}).success(function(data){
                    that.list = data;
                });

                this.invite = function(friend){
                    $facebook.ui({method: 'apprequests',
                        message: 'Join us - http://fortytwotesttask-136.bogdan.at.getbarista.com',
                        to: friend.id
                    }).then(function(resp){
                        notify({message: friend.name + ' was successfully invited! Please wait while user joined Task MG, and add it into your team', templateUrl: '/static/html/angular-notify.html'});
                    });

                };

            },
            controllerAs: 'invitable_friends'
        };
    });

    // Modal window
    app.controller('ModalInstanceCtrl', function ($scope, $modalInstance, $http, $httpParamSerializer, items) {
        $scope.items = items;
        $scope.selected = {
            item: $scope.items[0]
        };

        $scope.ok = function () {
            $modalInstance.close($scope.selected.item);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };

        $scope.addToTeam = function(item){
            console.log(item);
            var req = {
                method: 'POST',
                url: '/tm_invite/',
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: $httpParamSerializer({'cmd': 'add', 'item': item})
            };

            $http(req).success(function(data){
                window.location.reload();
            });
            $modalInstance.close($scope.selected.item);

        };
    });

    app.directive('teamManage', function(){
        return {
            restrict: 'E',
            templateUrl: '/static/html/team_manage.html',
            controller: function($log, $scope, $http, $modal, Teams, Teammates){
                this.current_user = null;
                $scope.team = null;
                $scope.new_team = {};
                $scope.teammates = [];
                $scope.items_invitable = [];


                this.getInvitable = function(){
                    $http.get('/tm_invite/', {}).success(function(data){
                        var i = 0,
                            max = data.length;
                        for( ; i < max; i += 1){
                            var item = {};
                            item.id = data[i]['pk'];
                            item.name = data[i]['fields']['first_name'] + ' ' + data[i]['fields']['last_name'];
                            $scope.items_invitable.push(item)
                        }
                    });
                };

                this.getInvitable();

                var that = this;

                $scope.addNewTeam = function(){
                    $scope.new_team.owner = that.current_user;
                    $scope.new_team.teammates = [];
                    $scope.team = $scope.new_team;
                    Teams.save($scope.new_team);
                    $scope.new_team = {};
                };

                $scope.remove = function(tm){
                    Teammates.remove(tm).then(function(response){
                        $scope.teammates.splice($scope.teammates.indexOf(tm), 1);
                        that.getInvitable();
                    })
                };
                $http.get('/current_user/').success(function(data){
                    that.current_user = data[0]['fields'];
                    that.current_user.id = data[0]['pk'];

                    Teams.getAll(data[0]['pk']).then(function(response) {
                        $scope.team = response.data.objects[0];
                        if($scope.team) {
                            $scope.teammates = $scope.team['teammates'];
                        }
                    });
                });

                // Modal window settings


                $scope.animationsEnabled = true;

                $scope.open = function (size) {
                    var modalInstance = $modal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: 'myModalContent.html',
                        controller: 'ModalInstanceCtrl',
                        size: size,
                        resolve: {
                            items: function () {
                                return $scope.items_invitable;
                            }
                        }
                    });
                    modalInstance.result.then(function (selectedItem) {
                        $scope.selected = selectedItem;
                    }, function (item) {
                        $log.info('Modal dismissed at: ' + new Date(), item);
                    });
                };

                $scope.toggleAnimation = function () {
                    $scope.animationsEnabled = !$scope.animationsEnabled;
                };


            },
            controllerAs: 'team-manage'
        };
    })

})();