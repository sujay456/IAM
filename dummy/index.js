
const loginForm=document.getElementById("login_form")
const messageContainer=document.querySelector('.message')
// console.log(loginForm)
const client_secret='b9009fbd-cd7e-4289-8c82-59e91a078374'

const base_url="http://3.110.132.231/"
var UserToken
loginForm.addEventListener("submit",(e)=>{
    e.preventDefault()
    username=e.target.username.value
    password=e.target.password.value
    
    $.ajax({
        url:base_url+"api/samsung/login/",
        type:"POST",
        data:{'username':username, 'password':password},
        headers:{'client-secret':client_secret},
        success: (data)=>{
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("username",data.username)
            localStorage.setItem("refresh_token",data.refresh_token)
            window.location.href = "http://127.0.0.1:5500/dummy/home.html";

        },
        error:(data)=>{
            console.log(data)
            messageContainer.innerHTML=`<p>${data.responseJSON.message}</p>`
        },
        complete: (data)=>{
        }

    })
})
