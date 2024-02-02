from bson import ObjectId
from fastapi import APIRouter, HTTPException
from ..database import orders_collection, products_collection
from ..models.order import OrderCreateModel, OrderCreateResponseModel, OrderItemResponse
from datetime import datetime

router = APIRouter()

@router.post("/create-order/", response_model=OrderCreateResponseModel)
async def create_order(order_data: OrderCreateModel):
    """
    Create a new order and update product quantities in MongoDB.

    Args:
        order_data (OrderCreateModel): Order data received from the client.

    Returns:
        OrderCreateResponseModel: Response model with order details.
    """
    try:
        if order_data.createdOn is None:
            order_data.createdOn = datetime.utcnow()

        order_data.totalAmount = OrderCreateModel.calculate_total_amount(order_data.items)
        order_dict = order_data.dict()
        updated_quantities = []

        for item in order_data.items:
            product_id = ObjectId(item.productId)

            product = products_collection.find_one({"_id": product_id})

            if product:
                if product["quantity"] >= item.boughtQuantity:
                    new_quantity = product["quantity"] - item.boughtQuantity
                    products_collection.update_one(
                        {"_id": product_id},
                        {"$set": {"quantity": new_quantity}}
                    )
                    updated_quantities.append({"productId": item.productId, "newQuantity": new_quantity})
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient quantity for product {product_id}"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product not found for ID {product_id}"
                )
            
        order_id = orders_collection.insert_one(order_dict).inserted_id
        order_data.id = str(order_id)

        response_model = OrderCreateResponseModel(
            id=order_data.id,
            createdOn=order_data.createdOn,
            items=[OrderItemResponse(productId=item.productId, boughtQuantity=item.boughtQuantity) for item in order_data.items],
            userAddress=order_data.userAddress,
            totalAmount=order_data.totalAmount,
        )

        return response_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    