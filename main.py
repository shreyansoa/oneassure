from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from database import data
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from datetime import timedelta, datetime
import uvicorn
from jose import jwt
import json
from bson.json_util import dumps
import random, string

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

app=FastAPI()

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username:str
    name:str
    phone:int
    password:str
    Description: Optional[str]=None

SECRET_KEY='26e06c153bb674f81c83b1919977a7989d594be75debb8f24afdc1b7930a569e'
ALGORITHM='HS256'

token_dict={}

@app.put('/signup/')
def signup(user: User):
     item={"_id":user.username, "name":user.name, "phone":user.phone, "password":get_password_hash(user.password), "Description":user.Description, "Key":generaterandom()}
     data.userdata(item)
     
     return user
def generaterandom():
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    return x

@app.post('/login')
def login (form_data: OAuth2PasswordRequestForm = Depends()):
    username=form_data.username
    password=form_data.password
    if get_authenticate(username, password):
        access_token=create_access_token(data={"sub":username}, expires_delta=timedelta(minutes=2))
        token_dict[username]=access_token
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

def get_authenticate(username, password):
    actual_password=data.userquery(username)
    
    return(pwd_context.verify(password, actual_password))
    
def create_access_token(data:dict, expires_delta:timedelta):
    to_encode=data.copy()
    expire= datetime.now()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token (token):
    try:
        decoded=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Session expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid Token')

@app.post('/login/update/phone/{username}/{number}')
def update(username:str, number:int):
    if username in token_dict:
        verify=decode_token(token_dict[username])
        if username == verify['sub']:
            data.updatephone(username, number)
        else:
            return HTTPException(status_code=401, detail='Session expired')
    else:
        return HTTPException(status_code=401, detail='Invalid Token')

@app.post('/login/update/name/{username}/{newname}')
def nameupdate(username:str, newname:str):
    if username in token_dict:
        verify=decode_token(token_dict[username])
        if username == verify['sub']:
            data.nameupdate(username, newname)
        else:
            return HTTPException(status_code=401, detail='Session expired')
    else:
        return HTTPException(status_code=401, detail='Invalid Token')


@app.get('/login/getDetails/{username}')
def getDetails(username:str):
    if username in token_dict:
        verify=decode_token(token_dict[username])
        if username == verify['sub']:
            
            user=data.getUserDetails(username)
            jsondic=dumps(user, indent=2)
            return jsondic
            
        else:
            return HTTPException(status_code=401, detail='Session expired')
    else:
        return HTTPException(status_code=401, detail='Invalid Token')

if __name__ == "__main__":
    uvicorn.run(app)



