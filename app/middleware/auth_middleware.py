import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException


SECRET_KEY = "kjdqslkdjsqlkdjsqkdsqjdlkqsjdqlkjdkqlfjqskdfjqk"
ALGORITHM = "HS256"

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        protected_paths = ["/api/protected"]

        if any(request.url.path.startswith(path) for path in protected_paths):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer") :
                raise HTTPException(status_code= 401,detail="Token requis")
            
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
                request.state.user = payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code= 401,detail="Token expire")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code= 401,detail="Token invalide")

        response = await call_next(request)
        return response
