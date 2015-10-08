
(function(){
    var app = angular.module('tasks', ["ngCookies", "ngResource", "pusher-angular", "ui.sortable", "cgNotify", "ui.bootstrap.datepicker"]);

    // Config $http for django backend
    app.config(function($httpProvider , $interpolateProvider, $resourceProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $resourceProvider.defaults.stripTrailingSlashes = false
    });

    // Api factories
    app.factory('Tasks', ['$http', function($http){

        var Tasks = function(data){
            angular.extend(this, data)
        };

        Tasks.getAll = function(userId) {
            return $http.get('/api/v1/items/?format=json&assigned_to=' + userId).then(function(response){
                // Replace string with Date object
                angular.forEach(response.data.objects, function(value, key){
                    response.data.objects[key]['due_to'] = new Date(response.data.objects[key]['due_to']);
                });
                return response;
            })
        };

        Tasks.get = function(id) {
            return $http.get('/api/v1/items/' + id + '/?format=json');
        };

        Tasks.save = function(task) {
            var url = '/api/v1/items/?format=json';
            return $http.post(url, task).error(function(data){
                console.log(data);
            });
        };

        Tasks.remove = function(id) {
            return $http.delete('/api/v1/items/' + id + '/?format=json');
        };
        return Tasks;

    }]);

    // Main app directive
    app.directive('tasksManagement', function(){
        return {
            restrict: 'E',
            templateUrl: '/static/html/tasks_manager.html',
            controller: function($log, $scope, $filter, $http, $pusher, notify, Tasks){

                this.current_user = null;
                $scope.new_task = {};
                $scope.tasks = [];
                $scope.status = {};
                $scope.status.opened = false;

                $scope.minDate = new Date();

                /**
                 * Tasks ui.sortable drag & drop config
                 */
                $scope.draggable = {
                    stop: function(e, ui){
                        var tasks = [];
                        angular.extend(tasks, $scope.tasks);
                        var i = 0,
                            max = tasks.length;
                        for(; i < max; i += 1){
                            tasks[i]['priority'] = i + 1;
                            Tasks.save(tasks[i]);
                        }
                        $scope.tasks.length = 0;
                        angular.extend($scope.tasks, tasks);
                    }
                };

                 /**
                 *  Add new task
                 */
                this.add = function(){
                    $scope.new_task.priority  = $scope.tasks.length + 1;
                    $scope.new_task.owner  = that.current_user;
                    $scope.new_task.assigned_to  = [that.current_user];
                    $scope.new_task.due_to = new Date($scope.new_task.due_to);
                    var pushed = $scope.tasks.push($scope.new_task);
                    Tasks.save($scope.new_task).success(function(data){
                        pushed -= 1;
                        if($scope.tasks[pushed]) {
                            $scope.tasks[pushed]['id'] = data.id;
                        }
                    });
                    $scope.new_task = {};
                    $scope.newTaskForm.$setPristine(true)
                };

                /**
                 *  Remove current task
                 *  @param task
                 */
                this.remove = function(task){
                    if(task.id) {
                        $scope.tasks.splice($scope.tasks.indexOf(task), 1);
                        Tasks.remove(task.id);
                    }
                };

                /**
                 * Save item changes
                 * @param task
                 */
                this.edit = function(task){
                    Tasks.save(task);
                };

                /**
                 * Add new task form validation
                 * @param newTaskForm
                 */
                $scope.validateForm = function(newTaskForm){
                    notify.closeAll();
                    if( newTaskForm.$invalid &&
                        newTaskForm.task.$invalid &&
                        !newTaskForm.task.$pristine) {
                         notify({message: 'Task text is required!', templateUrl: '/static/html/angular-notify.html', classes: 'nt-error'});
                    }

                    if( newTaskForm.$invalid &&
                        newTaskForm.date.$invalid &&
                        !newTaskForm.date.$pristine){
                        notify({message: 'Date field can\'t be empty!', templateUrl: '/static/html/angular-notify.html', classes: 'nt-error'});
                    }
                };

                var that = this;

                $scope.datepicker_toggle = function($event) {
                    $scope.status.opened = true;
                };

                // Listen for tasks changes with pusher
                var client = new Pusher('e749c59b174735416abe');
                var pusher = $pusher(client);
                var tasks_channel = pusher.subscribe('tasks-channel');
                tasks_channel.bind('tasks-changed', function(data) {
                    if(data.task.due_to){
                        data.task.due_to = new Date(data.task.due_to);
                    }
                    var i = 0,
                        max = $scope.tasks.length;
                    switch(data.method){

                        case 'save':
                            var saved = false;
                            for( ; i < max; i += 1) {
                                if (data.task.id == $scope.tasks[i]['id']) {
                                    $scope.tasks[i] = data.task;
                                    saved = true;
                                    break;
                                }
                            }
                            if(!saved){
                                var found = $filter("filter")($scope.tasks, {text: data.task.text}, true);
                                //Show new tasks only for assigned users
                                if(found.length == 0) {
                                    var check_permission = $filter("filter")(data.task.assigned_to, {id: that.current_user.id }, true);
                                    if(check_permission.length > 0) {
                                        $scope.tasks.push(data.task);
                                    }
                                }
                            }

                            break;
                        case 'delete':
                            for( ; i < max; i += 1) {
                                if (data.task.id == $scope.tasks[i]['id']) {
                                    $scope.tasks.splice(i, 1);
                                    break;
                                }
                            }
                        default:
                            ;
                    }
                });

                /**
                 * Fetch current_user
                 */
                $http.get('/current_user/').success(function(data){
                    that.current_user = data[0]['fields'];
                    that.current_user.id = data[0]['pk'];

                    // Filter tasks by current
                    Tasks.getAll(data[0]['pk']).then(function(response) {
                        $scope.tasks = response.data.objects;
                    });

                });

                /**
                 * Add task by Ctrl + Enter
                 */

                $scope.down = function(e){
                    if(e.ctrlKey && e.keyCode == 13){
                        that.add();
                    }
                };

            },
            controllerAs: 'task_item'
        };
    });

})();