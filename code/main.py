from fastapi import Depends, FastAPI , HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import pyrebase

app = FastAPI()

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

securityBasic  = HTTPBasic()
securityBearer = HTTPBearer()


#token de usuario
@app.get(
    "/users/token",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for user",
    description="Get a token for user",
    tags=["auth"],
)

def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
    
        response = {
            "token": user["idToken"]  #id del token
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )

@app.get(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for user",
    description="Get a token for user",
    tags=["auth"]
)

async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:

        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user["users"][0]["localId"] #uid de Authentication firebase

        db=firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            "user_data" : user_data
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )