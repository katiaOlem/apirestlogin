function login() {   

    let email = document.getElementById("email");
    let password  = document.getElementById("password");  
    let payload = {
        "email" : email.value,
        "password" : password.value
    }
    console.log(email.value);
    console.log(password.value );
    console.log(payload);
    var request = new XMLHttpRequest();
    request.open('POST',"https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us59.gitpod.io/user/token",true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('accept', 'application/json');  
    request.onload = function(){
    try{
        const status = request.status
        json = JSON.parse(request.responseText);

        if (status == 202) {
            const response = request.responseText;
            const json = JSON.parse(response);
            console.log(json);   
            sessionStorage.setItem("token", json.token);
            window.location.replace("./bienvenida.html");           
        }}
        catch (error) {
            console.log(error);
            alert(error);
                  }
    
    };
    request.send(JSON.stringify(payload));
};
