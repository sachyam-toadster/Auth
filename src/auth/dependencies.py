from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, status, Request
from src.auth.utils import decode_token

class AccessTokenBearer(HTTPBearer):
    # def __init__(self, auto_error=True):
    #     super().__init__(auto_error=auto_error)

    # async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
    #     creds = await super().__call__(request)
    #     token = creds.credentials

    #     if not self.token_valid(token):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN, detail={
    #                 "error":"This token is invalid or expired",
    #                 "resolution":"Please get new token"
    #             }
    #         )


    #     return token
    
    # def token_valid(self, token: str) -> bool:

    #     token_data = decode_token(token)

    #     return token_data is not None 

    pass