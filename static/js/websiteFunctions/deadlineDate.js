var deadline1 = document.getElementById("deadline1");
var deadline2 = document.getElementById("deadline2");
var deadline3 = document.getElementById("deadline3");

deadline1.addEventListener('click', function () {
    if (deadline2.checked == false) {
        deadline3.innerHTML = "";
    }
});

deadline2.addEventListener('click', function () {
    if (deadline2.checked == true) {
        deadline3.innerHTML = "<input type='date' class='form-control' id='deadlineDate' name='deadlineDate'>";
    }
});