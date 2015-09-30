'use strict';

describe('Landing page directive', function(){
    var $scope, scope, controller, $el;
    beforeEach(module('landing'));
    beforeEach(module('my.templates'));
    beforeEach(inject(function($compile, $rootScope) {
        $scope = $rootScope.$new();
        var element = angular.element("<landing-page></landing-page>");
        $el = $compile(element)($scope);
        $scope.$digest();
        controller = element.controller();
        scope = element.isolateScope() || element.scope();

    }));

    it('should display description, features, and info about author', function(){
        expect($el.html()).toContain('Tasks MG - is the modern web');
        expect($el.html()).toContain('Bogdan Piven');
        expect($scope.features.length).toEqual(4);

    });

});
