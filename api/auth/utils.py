import jwt

from api.auth.exceptions import ForbiddenException, BadRequestException
from config.auth_setting import auth_settings, auth_endpoints


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, permissions=None, scopes=None):
        self.permissions = permissions
        self.scopes = scopes
        self.config = auth_settings
        self.endpoints = auth_endpoints

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = self.endpoints.JWKS_ENDPOINT
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self, token: str):

        try:

            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                token
            ).key

        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}

        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:

            payload = jwt.decode(
                token,
                self.signing_key,
                algorithms=self.config.ALGORITHM,
                audience=self.config.AUDIENCE,
                issuer=self.config.ISSUER,
            )

        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            self._check_claims(payload, 'scope', str, self.scopes.split(' '))

        if self.permissions:
            self._check_claims(payload, 'permissions', list, self.permissions)

        return payload

    @staticmethod
    def _check_claims(payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            raise BadRequestException(message=f"No claim '{claim_name}' found in token")

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:

                raise ForbiddenException(message=f"Insufficient {claim_name} ({value}). You "
                                 "don't have access to this resource")

        return result
