from fastapi import Depends, FastAPI , HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import pyrebase

app = FastAPI()

class UserIU(BaseModel):
    email       : str
    password    : str

class Respuesta (BaseModel) :  
    message: str 

class Cliente (BaseModel):  
    direccion : str
    nombre: str  
    email: str 

class ClienteID (BaseModel):  
    id_cliente: str
    direccion: str
    nombre: str  
    email: str  
    

#urls
origins = [
    "https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us54.gitpod.io/",
    "https://8080-katiaolem-apirestlogin-hb1jsfk1n87.ws-us54.gitpod.io/",
    "*",              
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#copiar de configuración de firebase de la webapp y poner comillas
firebaseConfig = {
  "apiKey": "AIzaSyDaqg2xylEwjrs-16j9s_Oul2IhFCHzzCE",
  "authDomain": "login3-6edbb.firebaseapp.com",
  "databaseURL": "https://login3-6edbb-default-rtdb.firebaseio.com",
  "projectId": "login3-6edbb",
  "storageBucket": "login3-6edbb.appspot.com",
  "messagingSenderId": "865275330485",
  "appId": "1:865275330485:web:00fb9db201c5e08251a3fc",
  "measurementId": "G-97DWZ8KSM4"
};

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

#prueba de funcionamiento
@app.get("/")
def root():
    return {"message": "Hola"}

#validación
@app.post("/user/token",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"],
  )
async def get_token(usuario: UserIU ):
    try:
        auth = firebase.auth ()
        user = auth.sign_in_with_email_and_password(usuario.email, usuario.password)
        response = {
        "token": user['idToken'],
         }
        return response
    except Exception as error:
      print(f"Error: {error}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)

@app.get(
  "/users/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Get a UID for a user",
  description="Get a UID for a user",
  tags=["auth"],
)
async def get_user(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
        auth=firebase.auth()
        user=auth.get_account_info(credentials.credentials)
        uid= user['users'][0]['localId']       
        db= firebase.database()
        user_data=db.child('users').child(uid).get().val()
        response={
            "user_data":user_data 
            }
        return response
    except Exception as error:
        return(f"Erroruser:{error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(
  "/user/",
  summary="Create a new user",
  description="Create a new user",
  tags=["user"])
async def create_user(email:str,password:str,name:str):
  try:
    user = auth.create_user_with_email_and_password(email, password)
    user = auth.sign_in_with_email_and_password(email, password)
    uid = user['localId']
    print(uid)
    data= {
      "nombre":name,
      "nivel":"User"
      }
    userData = db.child("users").child(uid).set(data)
    message = {"token":user['idToken']}
    return message

  except Exception as error:
    print(f"Error: {error}")


##tabla de clientes
@app.get( "/clientes/", status_code=status.HTTP_202_ACCEPTED,
    summary = "Listado de clientes",
    description = "Listado de clientes",
    tags=["Cliente"]
    )

async def get_clientes(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        db = firebase.database()
        clientes = db.child("clientes").get().val()
        response = {
            "clientes": clientes
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error verifique sus datos",
            headers={"WWW-Authenticate": "Basic"},        
        )
    

#get
@app.get( "/clientes/{id}", status_code=status.HTTP_202_ACCEPTED,
    summary = "Retorna Cliente",
    description = "Retorna Cliente",
    tags = ["Cliente"]
)
async def get_cliente_id(id_cliente: str, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:       
        db = firebase.database()
        auth = firebase.auth()
        id = id_cliente
        print(id)
        cliente = db.child("clientes").child(id).get().val()

        response = {
            "cliente" : cliente
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )

#Post cliente
@app.post("/clientes/", status_code=status.HTTP_202_ACCEPTED,
    summary = "Agregar un cliente",
    description = "Agregar un cliente",
    tags=["Cliente"]
)
async def post_clientes(cliente: Cliente, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        db = firebase.auth()
        db = firebase.database()
        db.child("clientes").push({"Nombre": cliente.nombre, "Email": cliente.email,"Direccion":cliente.direccion})
        response = {"code": status.HTTP_201_CREATED, "message": "Se agrego correctamente"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        return(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
#Put cliente
@app.put( "/clientes/", response_model=Respuesta, status_code=status.HTTP_202_ACCEPTED,
    summary="Actualiza un cliente",
    description="Actualiza un cliente",
    tags=["Cliente"]
    
)
async def put_clientes(cliente:ClienteID, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:   
        db = firebase.auth() 
        db = firebase.database()
        db.child("clientes").child(cliente.id_cliente).update({"Nombre": cliente.nombre, "Email": cliente.email,"Direccion": cliente.direccion})
        response = {"message":"Cliente actualizado"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )
    
#delete cliente
@app.delete("/clientes/{id_cliente}", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
    summary = "Elimina un cliente",
    description = "Elimina un cliente",
    tags = ["Cliente"]
)
async def delete_clientes(id_cliente: str, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        db = firebase.auth()       
        db = firebase.database()
        id = id_cliente
        print(id)
        db.child("clientes").child(id).remove()
        response = {"message":"Cliente eliminado correctamente"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )