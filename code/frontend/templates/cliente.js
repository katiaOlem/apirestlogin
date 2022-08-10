getInformation(sessionStorage.getItem("token"));

function getInformation(token){

    var request = new XMLHttpRequest();
    request.open("GET","https://8080-katiaolem-apirestlogin-hb1jsfk1n87.ws-us59.gitpod.io/",true);
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