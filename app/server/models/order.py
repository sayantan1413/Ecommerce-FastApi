from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
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

class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int
    unitPrice: float

class OrderItemResponse(BaseModel):
    productId: str
    boughtQuantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zipCode: str


class OrderCreateModel(BaseModel):
    id: PydanticObjectId = None
    createdOn: datetime = Field(None, title="Auto-generated timestamp")
    items: list[OrderItem]
    userAddress: UserAddress
    totalAmount: float = Field(None, description="Total value of all items bought")

    @classmethod
    def calculate_total_amount(cls, items):
        print(items, "items")
        return sum(item.boughtQuantity * item.unitPrice for item in items)
    
class OrderCreateResponseModel(BaseModel):
    id: PydanticObjectId
    createdOn: datetime
    items: List[OrderItemResponse]
    userAddress: UserAddress
    totalAmount: float
