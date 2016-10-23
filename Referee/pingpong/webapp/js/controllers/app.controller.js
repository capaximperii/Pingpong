var app = angular.module('AF', ['ngResource', 'angularModalService', 'ui.router','nvd3ChartDirectives']);

app.controller('MainCtrl', function ($scope, $state) {
	$state.go('dashboard');
});

app.config(function ($stateProvider) {
	$stateProvider
		.state('menubar-page', {
	        'abstract': true,
	        views: {
	            'menubar@': {
	                templateUrl: '/html/leftmenu.html'
	            }
	        }
	    })
		.state('dashboard', {
			parent: 'menubar-page',
			url: '/dashboard',
			views: {
				'content@': {
					templateUrl: '/html/dashboard.html',
					controller: 'dashboardCtrl'
				}
			}
		})
		.state('alerts', {
			parent: 'menubar-page',
			url: '/alerts',
			views: {
				'content@': {
					templateUrl: '/html/alerts.html',
					controller: 'alertsCtrl'
				}
			}
		});
	});