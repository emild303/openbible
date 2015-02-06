angular.module('app').controller('BookCtrl', function($rootScope, $scope, $http, Text) {
  $scope.text = new Text($scope.module, $scope.book.title, $scope.chapter)
  $rootScope.page = "book";

  $scope.$on('reset', function() {
    $scope.text.reset($scope.module, $scope.book.title, $scope.chapter)
  });
});

angular.module('app').factory('Text', function($rootScope, $http, $sce) {
  var Text = function(module, title, chapter) {
    this.items = [];
    this.busy = false;

    this.module = module;
    this.title = title;
    this.chapter = chapter;
  };

  Text.prototype.reset = function(module, title, chapter) {
    this.module = module;
    this.title = title
    this.chapter = chapter

    this.addPage(true)
  }

  Text.prototype.increment = function() {
    this.chapter = this.chapter + 1
  }

  Text.prototype.addPage = function(reset) {
    if (this.chapter <= $rootScope.getBook(this.title)['chapters']) {
      if (this.busy) return;
      this.busy = true;

      $http.post('/proxy', {'module': this.module.id, 'book': this.title, 'chapter': this.chapter}).success(function(data) {
        if (reset) {
          this.items.length = 0;
          this.items.push({'chapter': this.chapter, 'text': $sce.trustAsHtml(data.html) });
        } else {
          this.items.push({'chapter': this.chapter, 'text': $sce.trustAsHtml(data.html) });
        }
        this.busy = false;

        this.increment()
      }.bind(this));
    }
  };

  return Text;
});
