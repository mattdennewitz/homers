Date.prototype.ymd = function() {
    var m = (this.getMonth() + 1).toString(); // getMonth() is zero-based
    var d  = this.getDate().toString();
    return this.getFullYear().toString() + '-' + (m[1] ? m : "0" + m[0]) + '-' + (d[1] ? d : "0" + d[0]);
};

Array.prototype.extend = function(v) {
    this.push.apply(this, v);
}


var app = angular.module('homers', ['ngResource', 'ngRoute']);


app.config(function($interpolateProvider,
                    $routeProvider,
                    $locationProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    $routeProvider
        .when('/', {
            templateUrl: 'stacks/partials/pick_games.html',
            controller: 'pickGames'
        })
        .when('/stats', {
            templateUrl: 'stacks/partials/list_user_games.html',
            controller: 'userGames'
        });

    // $locationProvider.html5Mode(true);
});


app.factory('Play', ['$resource', function($resource) {
    return $resource('/api/v1/plays', {}, {
        query: {
            method: 'GET',
            isArray: false
        }
    });
}]);


app.controller('plays', function($scope, Play) {
    $scope.page = 1;
    $scope.loading = false;

    $scope.loadPage = function(action) {
        $scope.loading = true;

        Play.query({page: $scope.page}, function(response) {
            if(action == 'append') {
                var plays = $scope.plays.slice(0);
                plays.extend(response.plays);
                $scope.plays = plays;
            } else {
                $scope.plays = response.plays;
            }

            $scope.page = response.meta.next_page_number;
            $scope.loading = false;
        });
    }

    $scope.init = function() {
        $scope.loadPage();
    }
});


/*
app.controller('playsOnDate', function($scope, Play) {
    $scope.page = 1;
    $scope.loading = false;

    $scope.getPlaysForDate = function(action) {
        $scope.loading = true;

        Play.query({page: $scope.page}, function(resp) {
            if(action == 'append') {
                var plays = $scope.plays.slice(0);
                plays.extend(resp);
                $scope.plays = plays;
            } else {
                $scope.plays = resp;
            }

            $scope.loading = false;
        });
    }

    $scope.loadPrevious = function() {
        prevDate.setDate(prevDate.getDate() - 1);
        $scope.forDate = prevDate.ymd();
        $scope.getPlaysForDate('append')
    }

    $scope.init = function() {
        $scope.getPlaysForDate();
    }
});
*/
