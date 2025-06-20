from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, CookieTransport
from config import SECRET_KEY

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
