from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
import os
#  pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()




auth_bearer_scheme = HTTPBearer(scheme_name="BearerAuth")


def get_current_user(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(auth_bearer_scheme)],
):
    try:
        print(auth)
        payload = jwt.decode(
            auth.credentials, os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM")
        )
        print(payload)
        return {"sub": payload["sub"], "id": payload["id"]}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
        )
