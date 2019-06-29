controllers.controller("site", ["$scope",
function ($scope) {
    $scope.menuList = [
        {
            displayName: "首页", iconClass: "fa fa-tachometer fa-lg", url: "#/"
        },


    ];
    $scope.menuOption = {
        data: $scope.menuList
    };
}]);

