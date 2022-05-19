function check_username( thisObj )
{
    if (!document.getElementById("log_username").checkValidity())
    {
        thisObj.value = ""
        thisObj.placeholder = "Invalid username"
        thisObj.style.border = "2px solid red"
        thisObj.style.setProperty("--c", "red")
        thisObj.classList.add('error')
    }
    else
    {
        thisObj.style.border = "none"
    }
}

function check_password( thisObj )
{
    if (!document.getElementById("log_password").checkValidity())
    {
        thisObj.value = ""
        thisObj.placeholder = "Invalid password"
        thisObj.style.border = "2px solid red"
        thisObj.style.setProperty("--c", "red")
        thisObj.classList.add('error')
    }
    else
    {
        thisObj.style.border = "none"
    }
}

function password_visible( thisObj )
{   
    if (thisObj.classList.contains("bi-eye"))
    {
        document.getElementById("log_password").type = "text"
        thisObj.classList.replace("bi-eye", "bi-eye-slash")
    }
    else
    {
        document.getElementById("log_password").type = "password"
        thisObj.classList.replace("bi-eye-slash", "bi-eye")
    }
}


function check_password_conf( thisObj )
{
    var password_conf = document.getElementById("password");
    if (thisObj.value != password.value)
    {
        thisObj.value = ""
        thisObj.placeholder = "Passwords do not match"
        thisObj.style.border = "2px solid red"
        thisObj.style.setProperty("--c", "red")
        thisObj.classList.add('error')
    }
    else
    {
        thisObj.style.border = "none"
        document.getElementById("submit").disabled = false
    }
}


function select_language( thisObj )
{
    var clicked_name = thisObj.name;
    var clicked_text = thisObj.innerText;
    document.getElementById("select_language").innerHTML = clicked_text
    document.getElementById("input_language").value= clicked_name
}
    
function select_lan( thisObj )
{
    var clicked_name = thisObj.name;
    var clicked_text = thisObj.innerText;
    document.getElementById("select_language").innerHTML = clicked_text
    document.getElementById("input_language").value= clicked_name
}

function filter_category( thisObj )
{
    var clicked_name = thisObj.name;
    var clicked_text = thisObj.innerText;
    document.getElementById("select_filter_category").innerHTML = clicked_text
    document.getElementById("input_filter").value= clicked_name
}

function redheart( thisObj ) 
{
    thisObj.style.color = "red"
}

function share_over(thisObj)
{
    thisObj.classList.replace("bi-share", "bi-share-fill")
}

function share_out( thisObj )
{
    thisObj.classList.replace("bi-share-fill", "bi-share")
}

function trash_over(thisObj)
{
    thisObj.classList.replace("bi-trash3", "bi-trash3-fill")
}

function trash_out(thisObj)
{
    thisObj.classList.replace("bi-trash3-fill", "bi-trash3")
}