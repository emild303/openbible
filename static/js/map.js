angular.module('app').controller('MapCtrl', function($rootScope, $scope, $http) {
  $rootScope.page = "map";

  $scope.loadMap = function() {
    L.mapbox.accessToken = 'pk.eyJ1Ijoiam9udGF5ZXNwIiwiYSI6InVJa25QU2sifQ.qL2m4ZMKnuiU5qf3z8GcIw';
    //$scope.map = L.mapbox.map('map', 'examples.map-i86nkdio');
    $scope.map = L.mapbox.map('map', 'jontayesp.l6n52786');
    $scope.loadLayer();
  }

  $scope.loadLayer = function() {
    if ($scope.layer != undefined) {
      $scope.map.removeLayer($scope.layer)
    }
    $scope.layer = omnivore.kml('/static/kml/' + $scope.book.title.toLowerCase() + '.kml')
    .on('ready', function() {
      $scope.map.fitBounds($scope.layer.getBounds());
      $scope.layer.eachLayer(function(layer) {
        layer.bindPopup("<b>" + layer.feature.properties.name + "</b><br/>" + layer.feature.properties.description);
      });
    })
    .addTo($scope.map);
  }

  $scope.$on('reset', function() {
    $scope.loadLayer()
  });

  $scope.loadMap()
})
