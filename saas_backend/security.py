import time
import jwt
from fastapi import Header, HTTPException

SECRET = "CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"


def create_token(email: str):
    payload = {"sub": email, "iat": int(time.time())}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
