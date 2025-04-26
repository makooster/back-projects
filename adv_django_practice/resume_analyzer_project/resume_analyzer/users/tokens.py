from rest_framework_simplejwt.tokens import RefreshToken

def get_email_verification_token(user):
    """
    Generate a JWT access token to verify user email.
    """
    refresh = RefreshToken.for_user(user)
    token = refresh.access_token
    token['user_id'] = user.id  
    return str(token)
