CLIENT_CONFIG = {
    "web": {
        "client_id": "ВАШ_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "ВАШ_PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "ВАШ_CLIENT_SECRET",
        "redirect_uris": ["http://localhost:8080/callback"]  # Для разработки
    }
}

SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.heart_rate.read",
    "https://www.googleapis.com/auth/fitness.sleep.read"
]