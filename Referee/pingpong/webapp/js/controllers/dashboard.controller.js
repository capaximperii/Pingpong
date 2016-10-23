var app = angular.module('AF');

app.controller('dashboardCtrl', function ($scope, $timeout, GameResource) {
	$scope.games = [];

	$scope.loadAllGames = function() {
		$scope.message = "Loading ...";
		GameResource.get(function(games) {
			$scope.games = games.data;
		    $timeout(function () {
				$scope.loadAllGames();
		    }, 5000);
		});
	}


	$scope.loadAllGames();

});