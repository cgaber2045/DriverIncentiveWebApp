function checkPassComplexity()
{
    let pwd = document.getElementById('password');
    let message = document.getElementById('password-message');
    let submit = document.getElementById('signupbutton');
    let regex = /((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%]).{8,20})/;

    let good_color = "#66cc66";
    let bad_color = "#ff6666";

    if(regex.test(pwd.value))
    {
        pwd.style.backgroundColor = good_color;
        message.style.color = good_color;
        message.innerHTML = "<p>Password is strong!</p>";
        submit.disabled = false;
    }
    else
    {
        pwd.style.backgroundColor = bad_color;
        message.style.color = bad_color;
        message.innerHTML = "<p>Password needs to be between 8-20 characters and contain <br> 1 number, 1 uppercase, 1 lowercase, and 1 special character (!@#$%)</p>";
        submit.disabled = true;
    }
}

function checkPass()
{
   let pwd = document.getElementById('password');
   let pwd_check = document.getElementById('confirm');
   let message = document.getElementById('confirm-message');
   let submit = document.getElementById('signupbutton');

   let good_color = "#66cc66";
   let bad_color = "#ff6666";

   if(pwd.value === pwd_check.value)
   {
       pwd_check.style.backgroundColor = good_color;
       message.style.color = good_color;
       message.innerHTML = "<p>Passwords match!</p>";
       submit.disabled = false;
   }
   else
   {
      pwd_check.style.backgroundColor = bad_color;
      message.style.color = bad_color;
      message.innerHTML = "<p>Passwords do not match!</p>";
      submit.disabled = true;
   }
}

function showChangePass()
{
    button = document.getElementById('button');
    form = document.getElementById('passForm');

    form.style.visibility = 'visible';
    button.style.visibility = 'hidden';
}
