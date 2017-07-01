
function userSignIn()
{
    var userName = document.getElementById('inputUserName').value
    var userPswd = document.getElementById('inputUserPswd').value

    if(userName == '' || userPswd == '')
    {
        alert('user name or password is null.')
        return
    }

    document.getElementById('formUserInfo').submit()
}

function gotoSignUp()
{
    window.location.href='/doczone/login/signup/'
}

