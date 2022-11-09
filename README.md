
# One Assure Asignment 

FastAPI backend that does CRUD operation on mongodb and stores user's username name phone number description fields



## Run Locally

Clone the project

```bash
  git clone https://github.com/shadanxd/oneassure.git
```

Go to the project directory

```bash
  cd oneassure
```

Install dependencies

```pip
  pip install fastapi
```
```pip
  pip install pymongo
  ```
  ```pip
  pip install uvicorn
 ```
 ```pip
  pip install fastapi-security
```
```pip
  pip install pydantic
```
```pip
  pip install python-jose
```

Start the server

```bash
  uvicorn main:app --reload
```

### Use FastAPI docs to check end points

```
localhost:8000/docs
```

## API Reference

#### SignUp

```http
  PUT /signup/
```
```JSON
  {
  "username": "string",
  "name": "string",
  "phone": 0,
  "password": "string",
  "Description": "string"
  }
```


#### Login

```http
  POST /login
```

#### Update phone number

```http
  POST /login/update/phone/{username}/{number}
```

#### Update Name of any user

```http
  POST /login/update/name/{username}/{newname}
```

#### Get User Details

```http
  GET /login/getDetails/{username}
```


