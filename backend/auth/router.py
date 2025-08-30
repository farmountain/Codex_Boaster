from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Import the user models required for endpoint definitions
from backend.auth.models.user import User, UserCreate, UserInDB # <--- ADDED/UPDATED THIS LINE

from backend.auth.services.auth_service import AuthService
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency for getting the AuthService instance
def get_auth_service(db=Depends(AuthService.__init__)):
    # This dependency needs to return the AuthService instance, not just its init
    # Assuming AuthService can be directly instantiated or relies on get_db as a dependency itself
    return AuthService() # This line might need adjustment based on your AuthService constructor

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, auth_service: AuthService = Depends(AuthService)): # UserCreate is now defined
    """
    Registers a new user.
    """
    db_user = auth_service.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    db_user = auth_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Create the user and return the model that's suitable for API response
    return auth_service.create_user(user)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(AuthService)):
    """
    Authenticates a user and returns an access token.
    """
    user = auth_service.get_user_by_username(form_data.username)
    if not user or not auth_service.verify_password(form_data.password, user.password_hash): # Assuming user has password_hash in DB model
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30) # Example: 30 minutes expiration
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    auth_service.update_last_login(user) # Update last login timestamp
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(AuthService().get_current_user)):
    """
    Retrieves the current authenticated user's information.
    """
    return current_user

