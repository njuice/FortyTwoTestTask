'use strict';

describe('Tasks Management directive', function() {

    var $scope,
        scope,
        controller,
        $httpBackend,
        Tasks,
        userId = 1,
        tasks_mock = [{text: 'task1', owner:{id: 1, name: 'User'}, due_to: '2015-10-31', completed: false}];


    beforeEach(module('tasks'));
    beforeEach(module('my.templates'));
    beforeEach(inject(function($compile, $rootScope, _$httpBackend_, _Tasks_) {
        $scope = $rootScope.$new();
        $httpBackend = _$httpBackend_;
        Tasks = _Tasks_;
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
        $httpBackend.expectGET('/api/v1/items/?format=json&assigned_to=' + userId).respond(200, tasks_mock);
        var element = angular.element("<tasks-management></tasks-management>");
        $compile(element)($scope);
        $scope.$digest();
        controller = element.controller();
        scope = element.isolateScope() || element.scope();
    }));

    it('should display empty new task form', function(){
        expect(scope.new_task).toEqual({})
    });

    it('should fetch tasks items', function(){
        var tasks;
        $httpBackend.expectGET('/api/v1/items/?format=json&assigned_to=1').respond(tasks_mock);
        Tasks.getAll(userId).then(function(returnFromPromise){
            tasks = returnFromPromise.data;
        });
        $scope.$apply();
        $httpBackend.flush();
        expect(tasks).toEqual(tasks_mock);
    });

    it('user should be able to add new valid task', function () {
        var due_to = new Date();
        due_to.setDate(due_to.getFullYear() + 1);
        due_to = due_to.getFullYear() + '-' + (due_to.getMonth() < 10? '0' +
            due_to.getMonth() : due_to.getMonth()) + '-' + (due_to.getDate() < 10? '0' + due_to.getDate() : due_to.getDate());
        $scope.newTaskForm.date.$setViewValue(due_to);
        expect(scope.new_task.due_to.getDate()).toEqual(new Date(due_to).getDate());
        $scope.newTaskForm.task.$setViewValue('New task');
        expect(scope.new_task.text).toEqual('New task');

        expect($scope.newTaskForm.$valid).toBe(true);
        scope.task_item.add();
        expect($scope.tasks).toContain(jasmine.objectContaining({text:'New task'}));
    });

});



