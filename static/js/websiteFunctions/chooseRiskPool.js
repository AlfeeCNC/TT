var joinType = { "個人": ['請選擇進行方式', '分擔'], "團體": ['請選擇進行方式', '分擔', '互助'] };
var joinType1 = document.getElementById("join_type1");
var joinType2 = document.getElementById("join_type2");
//設定監聽器
joinType1.addEventListener('change', function () {

    //取得被選中的值
    var selected_option = joinType[this.value];

    //清空副選單現有的值
    while (joinType2.options.length > 0) {
        joinType2.options.remove(0);
    }

    //列出副選單新的值
    Array.from(selected_option).forEach(function (el) {

        let option = new Option(el, el);

        joinType2.appendChild(option);
    });

});

joinType2.addEventListener('change', function () {
    var btns = document.getElementById('btns')

    if (joinType1.value == '個人') {
        btns.innerHTML = '<a class="mt-4 btn btn-success w-100" href="/clubs/startPlan/individualPlan">創建個人分擔計畫</a>'
    }
    else if (joinType1.value == '團體') {
        if (joinType2.value == '分擔') {
            btns.innerHTML = '<a class="mt-4 btn btn-success w-100" href="/clubs/startPlan/createShareClub"}>創建風險分擔群組</a> <a class="mt-1 btn btn-warning w-100" href={% url "startPlanForm" %}>加入現有群組</a>'
        }
        else if (joinType2.value == '互助') {
            btns.innerHTML = '<a class="mt-4 btn btn-success w-100" href="/clubs/startPlan/createMutualHelpClub" %}>創建風險互助群組</a> <a class="mt-1 btn btn-warning w-100" href={% url "startPlanForm" %}>加入現有群組</a>'
        }
    }
})