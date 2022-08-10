function getClientes() {
    
    const token = sessionStorage.getItem('token');
    var request = new XMLHttpRequest();
    request.open('GET', "https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us60.gitpod.io/clientes/");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("content-type", "application/json");
    
    const  tabla    = document.getElementById("tabla_clientes");
    var tblBody     = document.createElement("tbody");
    var tblHead     = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>

            <th>Detalle</th>
            <th>Actualizar</th>
            <th>Borrar</th>
            <th>ID Cliente</th>
            <th>Direccion</th>
            <th>Nombre</th>
            <th>Email</th>
        </tr>`;

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);

        console.log(json);

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }
        
        else if (request.status == 202){
            const response = request.responseText;
            const parseo_json = JSON.parse(response);
            
            for (var key in parseo_json) {
                
                for (var id in parseo_json[key]) {
                    console.log(id);
                    console.log(parseo_json[key][id].Nombre)
                    var tr          = document.createElement('tr');
                    var detalle     = document.createElement('td');
                    var actualizar  = document.createElement('td');
                    var borrar      = document.createElement('td');
                    var id_cliente  = document.createElement('td');
                    var direccion   = document.createElement('td');
                    var nombre      = document.createElement('td');
                    var email       = document.createElement('td');
                    
                    
                
                    detalle.innerHTML       = "<a href='/templates/get_cliente.html?"+id+"'> Detalles </a>";
                    actualizar.innerHTML    = "<a href='/templates/update_cliente.html?"+id+"'> Actualizar </a>";
                    borrar.innerHTML        = "<a href='/templates/delete_clientes.html?"+id+"'> Borrar </a>";
                    id_cliente.innerHTML    = id;
                    nombre.innerHTML        = parseo_json[key][id].Nombre;
                    email.innerHTML         = parseo_json[key][id].Email;
                    direccion.innerHTML =parseo_json[key][id].Direccion;
                    tr.appendChild(detalle);
                    tr.appendChild(actualizar);
                    tr.appendChild(borrar);
                    tr.appendChild(id_cliente);
                    tr.appendChild(direccion);
                    tr.appendChild(nombre);
                    tr.appendChild(email);                
                    tblBody.appendChild(tr);
                }
            }
            tabla.appendChild(tblHead);
            tabla.appendChild(tblBody);
        }
    };
    request.send();
}