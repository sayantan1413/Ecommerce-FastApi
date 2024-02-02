from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..database import products_collection
from ..models.product import PageMetadataModel, ProductCreateModel, ProductListResponseModel, ProductModel

router = APIRouter()

@router.post("/add-product/", response_model=ProductModel)
async def add_product(product_data: ProductCreateModel):
    """
    Add a new product to the database.

    Args:
        product_data (ProductCreateModel): Product data received from the client.

    Returns:
        ProductModel: Response model with the details of the added product.
    """
    try:
        product_dict = product_data.dict()
        result = products_collection.insert_one(product_dict)
        product_id = result.inserted_id
        product = ProductModel(id=str(product_id), **product_dict)

        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/products/", response_model=ProductListResponseModel)
async def list_products(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_price: float = None,
    max_price: float = None,
):
    """
    List products from the database based on filters.

    Args:
        limit (int): Number of products to retrieve per page.
        offset (int): Starting index of products to retrieve.
        min_price (float): Minimum price filter.
        max_price (float): Maximum price filter.

    Returns:
        Dict: Dictionary containing product data and pagination metadata.
    """
    try:
        pipeline = [
            {
                "$facet": {
                    "products": [
                        {"$match": {"price": {"$gte": min_price} if min_price else {"$exists": True}}},
                        {"$match": {"price": {"$lte": max_price} if max_price else {"$exists": True}}},
                        {"$skip": offset},
                        {"$limit": limit},
                        {"$project": {"id": {"$toString": "$_id"}, "name": 1, "price": 1, "quantity": 1}},
                    ],
                    "count": [{"$count": "total"}],
                }
            },
            {
                "$project": {
                    "data": "$products",
                    "page": {
                        "next_offset": {"$add": [offset, limit]},
                        "prev_offset": {"$cond": {"if": {"$gt": [offset, limit]}, "then": {"$subtract": [offset, limit]}, "else": 0}},
                        "total": {"$arrayElemAt": ["$count.total", 0]},
                    }
                }
            }
        ]

        result = list(products_collection.aggregate(pipeline))

        data = result[0]["data"] if result and "data" in result[0] else []
        total_records = result[0]["page"]["total"] if result else 0

        default_limit = 10

        next_offset = offset + limit if offset + limit < total_records else None
        prev_offset = offset - limit if offset - limit >= 0 else None
        actual_limit = limit if "data" in result[0] else default_limit

        metadata = PageMetadataModel(limit=actual_limit, next_offset=next_offset, prev_offset=prev_offset, total=total_records)

        return {"data": data, "page": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    