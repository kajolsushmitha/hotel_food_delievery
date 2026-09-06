from fastapi import APIRouter, HTTPException, status

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


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.post(
    "/",
    response_model=HotelResponse,
    status_code=201
)
def create_hotel_api(hotel: HotelCreate):

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
def get_all_hotels_api():

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
def get_hotel_api(hotel_id: int):

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
def update_hotel_api(
    hotel_id: int,
    hotel: HotelUpdate
):

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
def delete_hotel_api(hotel_id: int):

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