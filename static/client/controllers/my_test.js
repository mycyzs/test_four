controllers.controller("my_test", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", "$stateParams",function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal,$stateParams) {
    $scope.kaoshi_id = $stateParams.id
    $scope.args = {};

    $scope.initsdd = function () {
        loading.open();
        sysService.search_detail({}, {id:$scope.kaoshi_id}, function (res) {
            loading.close();
            $scope.args = res.data
        })
    };
    $scope.initsdd();



     $scope.get_count_zhu = function () {
        loading.open();
        sysService.get_count_zhu({}, {id: $scope.kaoshi_id}, function (res) {
            loading.close();
            if (res.result) {
                $scope.test_column = res.data

            }else {
                errorModal.open(res.message);
            }
        });
    };

      $scope.get_count_zhu();


      $scope.test_chart = {
        //柱状图标题
        title: {text: '考试统计', enabled: false},
        //y轴
        yAxis: {
            title: {text: '数目'}, //y轴标题
            lineWidth: 2, //基线宽度1
            //tickPositions: [0, 1, 2, 3, 4]
        },
        //提示框位置和显示内容
        tooltip: {
            headerFormat: '<table\>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f} 台</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true,
            positioner: function () {
                return {x: 80, y: 80}
            }
        },
        data: "test_column"
    };

    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };



    $scope.down = function () {

            window.open('down_load?template_id=' + $scope.kaoshi_id);
        };




    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.hostList ? $scope.hostList : [], pageSize, page);
    };

    //查询系统表
    $scope.search_sys_info = function () {
        loading.open();
        sysService.search_kao_info({}, {id: $scope.kaoshi_id}, function (res) {
            loading.close();
            if (res.result) {
                $scope.hostList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            } else {
                errorModal.open(res.msg);
            }
        })
    };
    $scope.search_sys_info();


    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);


    $scope.uploadCsv = function () {
            CWApp.uploadCsv("uploadFile", callBack);
        };
        var callBack = function () {

            var content = fr.result;
            content = content.replace(new RegExp("\"", "gm"), "");
            var temp_list = [];
            var content_list = content.substring(0, content.lastIndexOf("\n")).split("\n");
            var column_len = content_list[0].split(",").length;
            var up_cvs = function (data) {
                loading.open();
                // 导入的后台方法
                sysService.up_cvs({}, data, function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "上传成功！！");
                        $scope.search_sys_info();
                        $scope.get_count_zhu()
                    }
                    else {
                        alert('上传失败')
                    }
                })
            }
            for (var i = 1; i < content_list.length; i++) {
                var device_obj = {};
                var columns = content_list[i].replace("\r", "").split(",");
                var a = columns.slice(0,8);
                var b = columns.slice(8);
                var device_obj = {
                    name: a[0],
                    depart: a[1],
                    score: a[2],
                    result: a[3],
                    comment: a[4],
                    kaoshi_id: $scope.kaoshi_id

                };
                temp_list.push(device_obj)
            }
            $scope.csvList = temp_list;
            // 开始请求后台方法
            up_cvs($scope.csvList)
        };




      $scope.gridOption = {
        data: "PagingData",
        enablePaging: true,
        enableColumnResize: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: "name", displayName: "考生", width: 230},
            {field: "depart", displayName: "部门", width: 230},
            {field: "score", displayName: "得分", width: 230},
            {field: "result", displayName: "结果", width: 230},
            {field: "comment", displayName: "备注", width: 230},

        ]
    };

}]);


