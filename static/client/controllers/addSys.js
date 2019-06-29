controllers.controller("addSys", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal","$filter",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal,$filter) {
    $scope.title = "添加系统";
    $scope.args = {
        biz: "",
        name: "",
        type:"",
        owner:"",
        phone:"",
        start_time:"",
        address:"",
        title:"",
        bizL: []

    };
    $scope.bizList = [];

    $scope.inits = function () {
        loading.open();
        sysService.search_biz({}, $scope.args, function (res) {
            loading.close();
            $scope.bizList = res.data
            $scope.args.bizL = res.data
        })
    };
    $scope.inits();

    // multiple为true则是多选
    $scope.dbOption1 = {
        data: "bizList",
        multiple: false,
        modelData: ""
    };
    $scope.uList = [{id:1,text:'运维开发工程师'},{id:2,text:'运维自动化工程师'}]
    $scope.dbOption2 = {
        data: "uList",
        multiple: false,
        modelData: ""
    };

    $scope.userList = []
    $scope.initsdd = function () {
        loading.open();
        sysService.search_user({}, {}, function (res) {
            loading.close();
            $scope.userList = res.data
        })
    };
    $scope.initsdd();


     $scope.dbOption3 = {
        data: "userList",
        multiple: false,
        modelData: ""
    };




      $scope.uploadCsv = function () {
          $scope.args.title = "考试题目1"
          alert("上传文件成功")
        };





    // 复选框

    // 判断全选或者全不选
    $scope.check = function(){
        var box = document.getElementById("thead_ck");
        var suns = document.getElementsByName("sun_ck");
        if(box.checked == false){
            for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = false;
                }
        }else {
           for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = true;
                }
        }
    };

    // 每选择一个子节点检查 全选或全不选要不要打勾
    $scope.check_sum = function(){
        var box = document.getElementById("thead_ck");
        var suns = document.getElementsByName("sun_ck");
        var checked_host = [];
        for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_host.push(suns[i].value)
            }
        }
        if(suns.length == checked_host.length){
            box.checked = true
        }else {
            box.checked = false
        }
    };

    // 获取选择的复选框
     var suns = document.getElementsByName("sun_ck");
        var checked_ip = [];
        for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_ip.push(suns[i].value)
            }
        }

     // 时间控件
    var dateNow = new Date();
    var effective_time = dateNow.setDate(dateNow.getDate() + 365);
    // 把时间转成普通格式
    $scope.args.start_time = $filter('date')(effective_time, 'yyyy-MM-dd HH:mm')





    $scope.confirm = function () {


        if ($scope.args.sys_name == '') {
            msgModal.open("error", "请输入系统名！");
            return
        }

        //请求后台函数存入数据
        loading.open();
        sysService.add_sys({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加考试成功！！");
                $modalInstance.close(res.data);
             }
            else {
                errorModal.open(res.msg);
             }
         })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };


}]);