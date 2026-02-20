import app.models
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter,Request  
from app.schemas import CreateProduct, Product
from app.database import engine, get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
router=APIRouter(prefix="/products",
                   tags=["Products"])
limiter = Limiter(key_func=get_remote_address)
@router.get("/",status_code=status.HTTP_200_OK,response_model=list[Product])
def get_products(db:Session=Depends(get_db),
                 search:str="",
                 limit:int=10,
                 skip:int=0):
        """ Retrieve a list of products.
        Args:
            search: Optional search term to filter products by title
            limit: Maximum number of products to return (default: 10)
            skip: Number of products to skip for pagination (default: 0)
            db: Database session
        Returns:
                A list of products matching the search criteria
        """
        results=(
                db.query(app.models.Product)
                .group_by(app.models.Product.id)
                .filter(app.models.Product.name.ilike(f"%{search}%"))
                .limit(limit)
                .offset(skip)
                .all()
            )
        return [product  for product in results]
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Product)
@limiter.limit("20/hour")   
def create_product(request: Request,
                   product:CreateProduct,
                   db:Session=Depends(get_db))->Product:
    """ Create a new product.
    Rate Limit: 20 requests per hour
    Args:
        request: HTTP request object
        product: Product data for the new product
        db: Database session
    Returns:
            The newly created product
    """
    try:
        new_product=app.models.Product(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    except IntegrityError:
            db.rollback()
            raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail="Product with that name already exists."
                                )


@router.get("/{id}",response_model=Product)
def get_product(id:int,db:Session=Depends(get_db))->Product:
    """ Retrieve a product by its ID.
    Args:
        id: Product ID
        db: Database session
    Returns:
            The product associated with the given ID
    """
    product=(
        db.query(app.models.Product)
        .filter(app.models.Product.id==id)
        .first()
       )
    if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product