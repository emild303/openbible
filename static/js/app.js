angular.module('app', ['infinite-scroll', 'ngAnimate', 'ngRoute', 'ngResource', 'ngSanitize'])

.config(function($routeProvider) {
  $routeProvider
    .when('/book', {
      templateUrl:'/static/partials/book.html',
      controller:'BookCtrl',
    })
    .when('/map', {
      templateUrl:'/static/partials/map.html',
      controller:'MapCtrl',
    })
    /*.when('/', {
      templateUrl:'/static/partials/land.html'
    })*/
    .otherwise({redirectTo: '/book'});
})

angular.module('app').controller('AppCtrl', function($document, $rootScope, $location, $scope, $http, $timeout) {
  $rootScope.themes = [
    {'id': 'default', 'name': 'Default'},
    {'id': 'solarized-light', 'name': 'Solarized Light'},
    {'id': 'solarized-dark', 'name': 'Solarized Dark'}
  ]

  $rootScope.books = [
    {'title': 'Genesis', 'chapters': 50},
    {'title': 'Exodus', 'chapters': 40},
    {'title': 'Leviticus', 'chapters': 27},
    {'title': 'Numbers', 'chapters': 36},
    {'title': 'Deuteronomy', 'chapters': 34},
    {'title': 'Joshua', 'chapters': 24},
    {'title': 'Judges', 'chapters': 21},
    {'title': 'Ruth', 'chapters': 4},
    {'title': '1 Samuel', 'chapters': 31},
    {'title': '2 Samuel', 'chapters': 24},
    {'title': '1 Kings', 'chapters': 22},
    {'title': '2 Kings', 'chapters': 25},
    {'title': '1 Chronicles', 'chapters': 29},
    {'title': '2 Chronicles', 'chapters': 36},
    {'title': 'Ezra', 'chapters': 10},
    {'title': 'Nehemiah', 'chapters': 13},
    {'title': 'Esther', 'chapters': 10},
    {'title': 'Job', 'chapters': 42},
    {'title': 'Psalms', 'chapters': 150},
    {'title': 'Proverbs', 'chapters': 31},
    {'title': 'Ecclesiastes', 'chapters': 12},
    {'title': 'Song of Solomon', 'chapters': 8},
    {'title': 'Isaiah', 'chapters': 66},
    {'title': 'Jeremiah', 'chapters': 52},
    {'title': 'Lamentations', 'chapters': 5},
    {'title': 'Ezekiel', 'chapters': 48},
    {'title': 'Daniel', 'chapters': 12},
    {'title': 'Hosea', 'chapters': 14},
    {'title': 'Joel', 'chapters': 3},
    {'title': 'Amos', 'chapters': 9},
    {'title': 'Obadiah', 'chapters': 1},
    {'title': 'Jonah', 'chapters': 4},
    {'title': 'Micah', 'chapters': 7},
    {'title': 'Nahum', 'chapters': 3},
    {'title': 'Habakkuk', 'chapters': 3},
    {'title': 'Zephaniah', 'chapters': 3},
    {'title': 'Haggai', 'chapters': 2},
    {'title': 'Zechariah', 'chapters': 14},
    {'title': 'Malachi', 'chapters': 4},
    {'title': 'Matthew', 'chapters': 28},
    {'title': 'Mark', 'chapters': 16},
    {'title': 'Luke', 'chapters': 24},
    {'title': 'John', 'chapters': 21},
    {'title': 'Acts', 'chapters': 28},
    {'title': 'Romans', 'chapters': 16},
    {'title': '1 Corinthians', 'chapters': 16},
    {'title': '2 Corinthians', 'chapters': 13},
    {'title': 'Galatians', 'chapters': 6},
    {'title': 'Ephesians', 'chapters': 6},
    {'title': 'Philippians', 'chapters': 4},
    {'title': 'Colossians', 'chapters': 4},
    {'title': '1 Thessalonians', 'chapters': 5},
    {'title': '2 Thessalonians', 'chapters': 3},
    {'title': '1 Timothy', 'chapters': 6},
    {'title': '2 Timothy', 'chapters': 4},
    {'title': 'Titus', 'chapters': 3},
    {'title': 'Philemon', 'chapters': 1},
    {'title': 'Hebrews', 'chapters': 13},
    {'title': 'James', 'chapters': 5},
    {'title': '1 Peter', 'chapters': 5},
    {'title': '2 Peter', 'chapters': 3},
    {'title': '1 John', 'chapters': 5},
    {'title': '2 John', 'chapters': 1},
    {'title': '3 John', 'chapters': 1},
    {'title': 'Jude', 'chapters': 1},
    {'title': 'Revelation', 'chapters': 22}
  ]

  $rootScope.modules = [
    {
      'id': 'esv',
      'title': 'ESV',
      'language': 'English'

    },
    {
      'id': 'aleppo',
      'title': 'Hebrew',
      'font': 'modernhebrew',
      'language': 'Hebrew',
      'text': 'right'
    },
    {
      'id': 'aleppo',
      'title': 'Paleo Hebrew',
      'font': 'paleohebrew',
      'language': 'Hebrew',
      'text': 'right'
    },
    {
      'id': 'aleppo',
      'title': 'Proto Sinaitic',
      'font': 'protosinaitic',
      'language': 'Hebrew',
      'text': 'right'
    }
  ]

  /* defaults */
  $rootScope.theme = $rootScope.themes[0];
  $rootScope.book = $rootScope.books[0];
  $rootScope.module = $rootScope.modules[0];
  $rootScope.chapter = 1;

  $rootScope.setModule = function(module) {
    $rootScope.module = module;

    $rootScope.$broadcast('reset');
    document.body.scrollTop = document.documentElement.scrollTop = 0;
  }

  $rootScope.setBook = function(book) {

    if ($rootScope.book != book) {
      $rootScope.book = book;
      $rootScope.chapter = 1;

      if ($location.path() == '/') {
        $location.path('/book')
      }

      $rootScope.$broadcast('reset');
      document.body.scrollTop = document.documentElement.scrollTop = 0;
    }

    $('#collapse-books').collapse('hide')
  }

  $rootScope.setChapter = function(chapter) {
    $rootScope.$broadcast('reset');
    document.body.scrollTop = document.documentElement.scrollTop = 0;
  }

  $rootScope.getBook = function(title) {
    for (idx=0;idx<$rootScope.books.length;idx++) {
      if ($rootScope.books[idx].title == title) {
        return $rootScope.books[idx]
      }
    }
  }

  /* utils */

  $rootScope.makeid = function() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ ) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }

  $rootScope.getTimes = function(n){
    return new Array(n);
  };

  $rootScope.safeApply = function(scope) {
    (scope.$$phase || scope.$root.$$phase) ? true : scope.$apply();
  }
});
