function getCliente(){
    
    const token = sessionStorage.getItem('token')
    var id_cliente = window.location.search.substring(1);
    console.log("id_cliente: " + id_cliente);
    
    
    var request = new XMLHttpRequest();
    request.open('GET', "https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us60.gitpod.io/clientes/{id}?id_cliente="+ id_cliente,true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("content-type", "application/json");
    
    
    
    
    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response);
        direccion=json.cliente.Direccion;
        nombre=json.cliente.Nombre;
        email=json.cliente.Email;

        const status    = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){



            let direccion = document.getElementById("direccion")
            let nombre  = document.getElementById("nombre");
            let email   = document.getElementById("email");


            direccion.value = json.cliente.Direccion;
            nombre.value    = json.cliente.Nombre;
            email.value     = json.cliente.Email;
        }
        else if(status==404){
            let direccion = document.getElementById("direccion")
            let nombre  = document.getElementById("nombre");
            let email   = document.getElementById("email");

            direccion.value = "none";
            nombre.value    = "None";
            email.value     = "None";
            alert("Cliente no encontrado");
        }
    }
    request.send();
}