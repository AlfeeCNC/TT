onload = function(){
    setInterval(go, 1000);
}

var time = 2;
function go() {
    if (time >= 0){
        document.getElementById("countDown").innerText = time ;
    }
    else{
        location.href="../../";
    }
    time--;
}