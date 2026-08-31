# pip install fastapi uvicorn python-keycloak python-jose

import os
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from keycloak import KeycloakOpenID, KeycloakAdmin

from fastapi import FastAPI, Depends, HTTPException, status

# --- Keycloak Configuration ---
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080/")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "datahub")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "fastapi")

PORT = int(os.getenv('PORT', '8000'))
PROXY_ROOT_PATH = os.getenv('PROXY_ROOT_PATH', '')

app = FastAPI(
    title="Datahub - Example backend using FastAPI framework",
    description="do something awesome",
    version="1.0.0",
    root_path=PROXY_ROOT_PATH
)

# Keycloak OpenID client
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
)

KEYCLOAK_ADMIN = KeycloakAdmin(server_url=KEYCLOAK_URL,
                               client_id=KEYCLOAK_CLIENT_ID,
                               realm_name=KEYCLOAK_REALM,
                               client_secret_key=KEYCLOAK_CLIENT_SECRET,
                               verify=False)

# This enables the "Authorize" button in FastAPI Swagger UI
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodes and validates the token using Keycloak's public key.
    """
    try:
        # 1. Get the public key from Keycloak to verify signature
        # In production, you should cache this key!
        keycloak_public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{keycloak_openid.public_key()}"
            "\n-----END PUBLIC KEY-----"
        )

        # 2. Decode and verify the JWT
        payload = jwt.decode(
            token,
            keycloak_public_key,
            algorithms=["RS256"],
            audience="account"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "Public endpoint - welcome!"}


@app.get("/my-profile")
def read_secure_data(user: dict = Depends(get_current_user)):

    print_kc_info()

    """
    This endpoint requires a valid token from Keycloak.
    """
    return {
        "message": "You are authenticated: %s (%s)" %( user.get("preferred_username"),
                                                       user.get("email")),
        "user_info": {
            "username": user.get("preferred_username"),
            "email": user.get("email"),
            "roles": user.get("realm_access", {}).get("roles", [])
        }
    }


def print_kc_info():
    print("key cloak url is: %s" % KEYCLOAK_URL)

    try:
        users = KEYCLOAK_ADMIN.get_users()
        print("===\nUsers in realm %s : %s\n===" % (KEYCLOAK_REALM, len(users)))
        for usr in users:
            print(usr)
    except Exception as e:
        print("error fetching users")
        print(e)


if __name__ == "__main__":
    import uvicorn

    #print_kc_info()

    uvicorn.run(app, host="0.0.0.0", port=PORT)
