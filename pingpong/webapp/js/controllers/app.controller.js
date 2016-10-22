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
		})
		.state('manage', {
			parent: 'menubar-page',
			url: '/manage',
			views: {
				'content@': {
					templateUrl: '/html/manage.html',
					controller: 'manageCtrl'
				}
			}
		}).state('rule', {
			parent: 'menubar-page',
			url: '/rule',
			views: {
				'content@': {
					templateUrl: '/html/rule.html',
					controller: 'ruleCtrl'
				}
			}
		}).state('signature', {
			parent: 'menubar-page',
			url: '/signature',
			views: {
				'content@': {
					templateUrl: '/html/signature.html',
					controller: 'signatureCtrl'
				}
			}
		}).state('settings', {
			parent: 'menubar-page',
			url: '/settings',
			views: {
				'content@': {
					templateUrl: '/html/settings.html',
					controller: 'settingsCtrl'
				}
			}
		}).state('help', {
			parent: 'menubar-page',
			url: '/help',
			views: {
				'content@': {
					templateUrl: '/html/help.html',
				}
			}
		});
	});