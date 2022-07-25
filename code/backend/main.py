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
    name        : str
    


#urls
origins = [
    "https://8000-katiaolem-apirestlogin-hb1jsfk1n87.ws-us54.gitpod.io/",
    "https://8080-katiaolem-apirestlogin-hb1jsfk1n87.ws-us54.gitpod.io/",
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

@app.get("/")  #para saber que funciona la api
def root():
    return {"message": "Hola"}

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


@app.get("/")
def root():
    return {"message": "Hola"}

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"],
  )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      email = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(email, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as error:
      print(f"Error: {error}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Get a token for a user",
  description="Get a token for a user",
  tags=["auth"],
)
async def get_token(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId']
      user_data = db.child("users").child(uid).get().val()
      response = {
        "user_data": user_data,
      }
      return response
    except Exception as error:
      print(f"Error: {error}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(
  "/user/",
  summary="Create a new user",
  description="Create a new user",
  tags=["Create"])
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