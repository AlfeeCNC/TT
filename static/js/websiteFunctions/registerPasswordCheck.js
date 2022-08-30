var password = document.getElementById('password');
var passwordConfirm = document.getElementById('passwordConfirm');
var sign = document.getElementById('sign');
var submitButton = document.getElementById('submitButton');

passwordConfirm.addEventListener('input', function(){
    if (password.value == passwordConfirm.value){
        sign.innerHTML = "<small style='color :green;''><strong>兩次輸入相同</strong></small>";
        submitButton.disabled = false;
    }
    else{
        sign.innerHTML = "<small style='color :red;''><strong>兩次密碼不相同，請再次確認</strong></small>";
        submitButton.disabled = true;
    }
})