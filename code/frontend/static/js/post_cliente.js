function PostCliente(){

    const token = sessionStorage.getItem('token');
    console.log(token);

    let direccion = document.getElementById("direccion");
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");

    let payload = {

        "direccion": direccion.value,
        "nombre": nombre.value,
        "email" : email.value,
    }

    
    var request = new XMLHttpRequest(); 
    request.open('POST', "https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us60.gitpod.io/clientes/",true);
    request.setRequestHeader("accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response); 
        
        const status    = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){

            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            Swal.fire({
                title: json.message,
                text: "Regresar a la lista de clientes ",
                type: "success"
            }).then(function() {
                window.location = "/templates/get_clientes.html";
            });
            
        }
    };
    request.send(JSON.stringify(payload));
};