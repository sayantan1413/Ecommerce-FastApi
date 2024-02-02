from pydantic import BaseModel
from typing import List, Union
from bson import ObjectId


class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return str(ObjectId(v))
        except Exception:
            raise ValueError('Invalid ObjectId format')
    
class ProductModel(BaseModel):
    id: PydanticObjectId
    name: str
    price: float
    quantity: int

class PageMetadataModel(BaseModel):
    limit: int
    next_offset: Union[int, None]
    prev_offset: Union[int, None]
    total: int

class ProductResponseModel(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

class ProductListResponseModel(BaseModel):
    data: List[ProductResponseModel]
    page: PageMetadataModel

class ProductCreateModel(BaseModel):
    name: str
    price: float
    quantity: int
