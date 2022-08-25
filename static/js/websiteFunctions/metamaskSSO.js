web3 = new Web3(window.ethereum);
$("#account").val("");
$("#signature").val("");
$("#message").val("");

let nonceToSign = "";

$("#connectMetaMask").click(function () {
    ethereum.request({ method: 'eth_requestAccounts' })
        .then(buttonStatus_Connected(), getNonce(),)
        .catch(buttonStatus_Disconnected);
})

$("#metamaskLogin").click(function () {
    msgToSign = "為認證您為該地址的合法持有人，我們將要求您簽署這串文字，進行簽章驗證" + nonceToSign
    ethereum.request({ method: 'eth_requestAccounts' }).then(
        web3.eth.getAccounts()
            .then(result => addr = result)
            .then(result =>
                web3.eth.personal.sign(msgToSign, web3.utils.toChecksumAddress(result[0]))
                    .then(result => loginForm(addr, String(result), msgToSign))));
})

function buttonStatus_Connected() {
    document.getElementById("connectMetaMask").setAttribute('disabled', '');
    document.getElementById("connectMetaMask").setAttribute("aria-disabled", "true");
    connectMetaMask.innerText = "已連結";
    document.getElementById("metamaskLogin").setAttribute("aria-disabled", "false");
    document.getElementById("metamaskLogin").removeAttribute('disabled');
}

function buttonStatus_Disconnected() {
    document.getElementById("connectMetaMask").removeAttribute('disabled');
    document.getElementById("connectMetaMask").setAttribute("aria-disabled", "false");
    connectMetaMask.innerText = "連結 MetaMask";
    document.getElementById("metamaskLogin").setAttribute("aria-disabled", "true");
    document.getElementById("metamaskLogin").setAttribute('disabled', '');
}

function loginForm(address, signature, message) {
    // message = web3.eth.accounts.hashMessage(message)
    $("#account").val(address);
    $("#signature").val(signature);
    $("#message").val(message);
    $("#loginForm").submit();
}

function getNonce() {
    $.getJSON("nonce", function (result) {
        nonceToSign = result.nonce;
    })
}