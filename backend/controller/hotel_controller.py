from fastapi import APIRouter, HTTPException, Depends, status

from backend.schema.hotel_schema import (
    HotelCreate,
    HotelUpdate,
    HotelResponse
)

from backend.services.hotel_services import (
    create_hotel,
    get_all_hotels,
    get_hotel_by_id,
    update_hotel,
    delete_hotel,
    HotelNotFoundException
)

from backend.repository.hotel_repository import (
    HotelDatabaseException
)
from backend.dependencies.auth_dependency import get_current_hotel


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.post(
    "/",
    response_model=HotelResponse,
    status_code=201
)
def create_hotel(hotel: HotelCreate):

    try:
        return create_hotel(hotel)

    except HotelDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[HotelResponse]
)
def get_all_hotels():

    try:
        return get_all_hotels()

    except HotelDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/{hotel_id}",
    response_model=HotelResponse
)
def get_hotel(hotel_id: int):

    try:
        return get_hotel_by_id(hotel_id)

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except HotelDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.patch(
    "/{hotel_id}",
    response_model=HotelResponse
)
def update_hotel(
    hotel_id: int,
    hotel: HotelUpdate,
    current_hotel: dict = Depends(get_current_hotel)
):
    if current_hotel["id"] != hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only update your own hotel profile"
        )

    try:
        return update_hotel(
            hotel_id,
            hotel
        )

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except HotelDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete(
    "/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_hotel(
    hotel_id: int,
    current_hotel: dict = Depends(get_current_hotel)
):
    if current_hotel["id"] != hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only delete your own hotel"
        )

    try:
        delete_hotel(hotel_id)

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except HotelDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )