from fastapi import APIRouter, Depends, HTTPException, status

from backend.schema.history_schema import HistoryQueryParams
from backend.services.history_services import (
    get_hotel_order_history,
    HotelOrderHistoryNotFoundException,
    InvalidDateRangeException
)
from backend.dependencies.auth_dependency import get_current_hotel


router = APIRouter(
    prefix="/hotels",
    tags=["Order History"]
)


@router.get(
    "/{hotel_id}/order-history"
)
def get_order_history(
    hotel_id: int,
    params: HistoryQueryParams = Depends(),
    current_hotel: dict = Depends(get_current_hotel)
):
    if current_hotel["id"] != hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only view order history for your own hotel"
        )

    try:
        return get_hotel_order_history(
            hotel_id=hotel_id,
            start_time=params.start_time,
            end_time=params.end_time,
            limit=params.limit,
            offset=params.offset
        )

    except HotelOrderHistoryNotFoundException as error:
        raise HTTPException(
            status_code=404,
            detail=error.message
        )

    except InvalidDateRangeException as error:
        raise HTTPException(
            status_code=400,
            detail=error.message
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )