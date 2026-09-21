from fastapi import APIRouter, HTTPException, Depends, status

from backend.schema.order_schema import (
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
    OrderDetailsResponse,
    PassengerOrderResponse,
    HotelOrderResponse
)

from backend.services import order_services
from backend.dependencies.auth_dependency import (
    get_current_passenger,
    get_current_hotel
)
from backend.model.pass_model import Passenger


router = APIRouter(
    tags=["Orders"])


@router.post(
    "/orders",
    response_model=OrderResponse
)
def create_order(order_data: OrderCreate):

    try:
        return order_services.create_order(order_data)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@router.get(
    "/orders/{order_id}",
    response_model=OrderDetailsResponse
)
def get_order(order_id: int):

    try:
        return order_services.get_order_by_id(order_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/passengers/{passenger_id}/orders",
    response_model=list[PassengerOrderResponse],
    summary="Get Passenger Orders (JWT Protected)",
    description="Fetches all orders placed by the passenger. Requires valid Passenger JWT token."
)
def get_passenger_orders(
    passenger_id: int,
    current_passenger: Passenger = Depends(get_current_passenger)
):
    if current_passenger.id != passenger_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only view your own orders"
        )

    return order_services.get_orders_by_passenger(
        passenger_id
    )


@router.get(
    "/hotels/{hotel_id}/orders",
    response_model=list[HotelOrderResponse]
)
def get_hotel_orders(
    hotel_id: int,
    current_hotel: dict = Depends(get_current_hotel)
):
    if current_hotel["id"] != hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only view orders for your own hotel"
        )

    return order_services.get_orders_by_hotel(
        hotel_id
    )


@router.patch(
    "/orders/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_hotel: dict = Depends(get_current_hotel)
):
    try:
        order = order_services.get_order_by_id(order_id)
        if order["hotelId"] != current_hotel["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only update orders belonging to your hotel"
            )

        return order_services.update_order_status(
            order_id,
            status_data.status
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except HTTPException:
        raise


@router.delete(
    "/orders/expired",
    summary="Delete expired orders (TTL)",
    description="Deletes orders older than the specified days threshold (default 30 days)."
)
def delete_expired_orders(days: int = 30):

    try:
        return order_services.cleanup_expired_orders(days=days)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete(
    "/orders/{order_id}"
)
def delete_order(order_id: int):

    try:
        order_services.delete_order(order_id)

        return {
            "message": "Order deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


    