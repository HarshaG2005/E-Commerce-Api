import  app.models
import app.utils
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter,Request
from app.schemas import CreateUser, User
from app.database import engine, get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
router=APIRouter(prefix="/users",
                   tags=["Users"])
limiter = Limiter(key_func=get_remote_address)


###################################CREATING_USER####################
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=User)
@limiter.limit("3/hour")
async def create_user(request: Request,
                user:CreateUser,
                db:Session=Depends(get_db))->User:
            """ Create a new user account.
              Rate Limit: 3 requests per hour
            Args:
                user: User data for the new account
                db: Database session
            Returns:
                   The newly created user account

            """
            try:
                #hash the password
                hashed_password=app.utils.hash(user.password)
                user.password=hashed_password
                new_user=app.models.User(**user.model_dump())
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
            
            except IntegrityError:
                    db.rollback()
                    raise HTTPException(
                           status_code=status.HTTP_400_BAD_REQUEST,
                           detail="User with that email already exists."
                                     )
           
#######################SELECT_USER_ACCOUNT############################
@router.get("/{id}",response_model=User)

async def select_user(id:int,db:Session=Depends(get_db))->User:
      """ Retrieve a user account by its ID.
      Args:
          id: User ID
          db: Database session
      Returns:
              The user account associated with the given ID
      """
  
      user=(
        db.query(app.models.User)
        .filter(app.models.User.id==id)
        .first())
      if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cant find user related to id:{id}")
      return user
