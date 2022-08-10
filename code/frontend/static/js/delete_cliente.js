function DeleteCliente(){

    const token = sessionStorage.getItem('token');

    var id_cliente = window.location.search.substring(1);
    console.log("id_cliente: " + id_cliente);
    
    var request = new XMLHttpRequest();
    request.open('DELETE', "https://8080-katiaolem-apirestlogin-hb1jsfk1n87.ws-us60.gitpod.io/clientes/"+ id_cliente,true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("content-type", "application/json");

    
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
                text: "Volver a la lista de clientes ",
                type: "success"
            }).then(function() {
                window.location = "/templates/get_clientes.html";
            });
        }
    };
    request.send();
}