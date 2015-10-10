'use strict';

describe('Team manage', function() {

    var $scope,
        scope,
        controller,
        $httpBackend,
        userId = 1,
        Teams,
        Teammates,
        team_mock = {"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1}, "objects": [{"created_at": "2015-10-09", "id": 1, "name": "My super team", "owner": {"date_joined": "2015-10-01T20:33:07.004000", "email": "", "first_name": "Богдан", "id": 1, "is_active": true, "is_staff": false, "is_superuser": false, "last_login": "2015-10-03T12:43:14.682000", "last_name": "Пивень", "password": "!ZaciAbc39bVqkxAj2K91IJxUGe0DC6KEPsVgfWCy", "resource_uri": "/api/v1/users/1/", "username": "БогданПивень"}, "resource_uri": "/api/v1/teams/1/", "teammates": [{"id": 1, "resource_uri": "/api/v1/teammates/1/", "user": {"date_joined": "2015-10-06T21:25:07.515174", "email": "", "first_name": "Ivan", "id": 2, "is_active": true, "is_staff": false, "is_superuser": false, "last_login": "2015-10-06T21:25:08.779000", "last_name": "Piddubniy", "password": "!E7DEJcuZqqketd4qrKnpFBLFtovDqQP8VIvtToqb", "resource_uri": "/api/v1/users/2/", "username": "IvanPiddubniy"}}]}]},
        teammates_mock = [{"id": 1, "resource_uri": "/api/v1/teammates/1/", "user": {"date_joined": "2015-10-06T21:25:07.515174", "email": "", "first_name": "Ivan", "id": 2, "is_active": true, "is_staff": false, "is_superuser": false, "last_login": "2015-10-06T21:25:08.779000", "last_name": "Piddubniy", "password": "!E7DEJcuZqqketd4qrKnpFBLFtovDqQP8VIvtToqb", "resource_uri": "/api/v1/users/2/", "username": "IvanPiddubniy"}}];

    beforeEach(module('team'));
    beforeEach(module('my.templates'));
    beforeEach(inject(function($compile, $rootScope, _$httpBackend_, _Teams_, _Teammates_) {
        $scope = $rootScope.$new();
        $httpBackend = _$httpBackend_;
        Teams = _Teams_;
        Teammates = _Teammates_;

        $httpBackend.expectGET('/tm_invite/').respond(200, [
            {
                'fields': {
                    'email': "",
                    'first_name': "Ivan",
                    'is_staff': false,
                    'is_superuser': false,
                    'last_login': "2015-10-03T12:43:14.682Z",
                    'last_name': "Piddubniy",
                    'password': "!ZaciAbc39bVqkxAj2K91IJxUGe0DC6KEPsVgfWCy",
                    'username': "Ivan Piddubniy"
                },
                'model': "auth.user",
                'pk': userId
            }
        ]);

        $httpBackend.expectGET('/current_user/').respond(200, [
            {
                'fields': {
                    'email': "",
                    'first_name': "Bogdan",
                    'is_staff': false,
                    'is_superuser': false,
                    'last_login': "2015-10-03T12:43:14.682Z",
                    'last_name': "Piven",
                    'password': "!ZaciAbc39bVqkxAj2K91IJxUGe0DC6KEPsVgfWCy",
                    'username': "Bogdan Piven"
                },
                'model': "auth.user",
                'pk': userId
            }
        ]);

        $httpBackend.expectGET('/api/v1/teams/?format=json&owner=1').respond(team_mock);

        var element = angular.element("<team-manage></team-manage>");
        $compile(element)($scope);
        $scope.$digest();
        controller = element.controller();
        scope = element.isolateScope() || element.scope();
    }));

    it('should fetch team obj with teammates', function(){
        $httpBackend.expectGET('/api/v1/teams/?format=json&owner=1').respond(team_mock);
        Teams.getAll(userId);
        $scope.$apply();
        $httpBackend.flush();
        expect($scope.team).not.toBe(null);
        expect($scope.teammates).not.toBe([]);
    });

    it('user should be able manage teammates', function(){
        $httpBackend.expectGET('/api/v1/teams/?format=json&owner=1').respond(team_mock);
        Teams.getAll(userId);
        $scope.$apply();
        $httpBackend.flush();
        expect($scope.teammates.length).not.toBe(0);
        $httpBackend.expectDELETE('/api/v1/teammates/1/?format=json').respond();
        Teammates.remove($scope.teammates[0]).then(function(response){
            $scope.teammates.splice($scope.teammates.indexOf($scope.teammates[0]), 1);
        });
        $scope.$apply();
        $httpBackend.flush();
        expect($scope.teammates.length).toBe(0);

    });

});

