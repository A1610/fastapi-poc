# main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from supabase_client import supabase

app = FastAPI(title="FastAPI Supabase POC")

# ---------- MODELS ----------
class SignupModel(BaseModel):
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str


# ---------- SIGNUP ----------
@app.post("/signup")
async def signup(data: SignupModel):
    try:
        res = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password,
            }
        )

        if res.user is None:
            raise HTTPException(status_code=400, detail=res.session)

        return {
            "status": "ok",
            "user": res.user.email,
            "message": "Signup successful. Check email if confirmations enabled."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- LOGIN ----------
@app.post("/login")
async def login(data: LoginModel):
    try:
        res = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password
            }
        )

        if res.session is None:
            raise HTTPException(status_code=400, detail="Invalid login credentials")

        return {
            "status": "ok",
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": res.user.email,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- AUTH MIDDLEWARE ----------
def get_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split("Bearer ")[1]

    try:
        res = supabase.auth.get_user(token)

        if res.user is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return res.user

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ---------- PROFILE ----------
@app.get("/profile")
async def profile(user=Depends(get_user)):
    return {
        "status": "ok",
        "email": user.email,
        "id": user.id,
    }
