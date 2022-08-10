function PutCliente(){
    const token = sessionStorage.getItem('token');
    
    var id_cliente = window.location.search.substring(1);
    let id_cliente1 = id_cliente;
    let direccion = document.getElementById("direccion");
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");    
    
    let payload = {
        "id_cliente": id_cliente1,
        "direccion" : direccion.value,
        "nombre": nombre.value,
        "email" : email.value,
    }

    console.log(payload);
    
    var request = new XMLHttpRequest();
    request.open('PUT','https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us59.gitpod.io/clientes/',true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("content-type", "application/json");
    
    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response);     
        const status    = request.status;
        console.log(json);

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){

            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);
        }
    };
    request.send(JSON.stringify(payload));
}