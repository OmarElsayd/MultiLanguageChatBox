from fastapi.security import OAuth2PasswordBearer


class OAuthSchemaBearer:
    def __int__(self):
        self.OAuthSchema = OAuth2PasswordBearer(tokenUrl="token")

    def get_o_auth_schema(self):
        return self.OAuthSchema
