getInformation(sessionStorage.getItem("token"));

function getInformation(token){

    var request = new XMLHttpRequest();
    request.open("GET","https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us54.gitpod.io/user/",true);
    request.setRequestHeader('Authorization', 'Bearer '+token);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('accept', 'application/json');

    request.onload = function(){

        const status = request.status

        if (status == 202) {
            json = JSON.parse(request.responseText);
            
        }

        else{
            alert(json.detail);
        }
    }
    request.send();
}