from google_auth_oauthlib.flow import Flow
from credentials import CLIENT_CONFIG, SCOPES

def get_auth_url():
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri="http://localhost:8080/callback"
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    return auth_url

def get_tokens(auth_response):
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri="http://localhost:8080/callback"
    )
    flow.fetch_token(code=auth_response)
    return flow.credentials