
function alertAtDom(msg, dom)
{
    if(null == dom)
    {
        alert(msg)
        return
    }

    // alert for default
    alert(msg)
}

function userSignIn()
{
    var userName = document.getElementById('inputUserName').value
    var userPswd = document.getElementById('inputUserPswd').value

    if(userName == '' || userPswd == '')
    {
        alertAtDom('user name or password is null.', null)
        return
    }

    document.getElementById('formUserInfo').submit()
}

function userSignUp()
{
    var userName = document.getElementById('inputUserName').value
    var userPswd = document.getElementById('inputUserPswd').value
    var userPswdAck = document.getElementById('inputUserPswdAgain').value

    if(userName == '' || userPswd == '' || userPswdAck == '')
    {
        alertAtDom('user name or password is null.', null)
        return
    }

    if(userPswd != userPswdAck)
    {
        alertAtDom('pwd ack is not the same as pwd', null)
        return
    }

    if(userPswd.length < 6)
    {
        alertAtDom('the length of pwd is less than 6', null)
        return
    }

    document.getElementById('formUserInfo').submit()
}

function gotoSignUp()
{
    window.location.href='/doczone/login/signup/'
}

