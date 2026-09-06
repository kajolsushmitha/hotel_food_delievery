from fastapi import APIRouter, HTTPException
from backend.schema.pass_schema import PassengerUpdate,PassengerCreate
from backend.services.pass_services import (
    add_passenger,
    get_passengers,
    get_passenger,
    remove_passenger,
    edit_passenger,
    PassengerAlreadyExistsException,
    PassengerNotFoundException
)

router = APIRouter(
    prefix="/passengers",
    tags=["Passengers"]
)

@router.post("/", status_code=201)
def create_passenger(passenger: PassengerCreate):
    try:
        return add_passenger(passenger)

    except PassengerAlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get("/")
def get_all_passengers():
    try:
        return get_passengers()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch passengers"
        )


@router.get("/{passenger_id}")
def get_passenger_by_id(passenger_id: int):
    try:
        return get_passenger(passenger_id)

    except PassengerNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch passenger"
        )


@router.delete("/{passenger_id}")
def delete_passenger_by_id(passenger_id: int):
    try:
        return remove_passenger(passenger_id)

    except PassengerNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete passenger"
        )

@router.patch("/{passenger_id}")
def update_passenger_by_id(
    passenger_id: int,
    passenger: PassengerUpdate
):
    try:
        return edit_passenger(
            passenger_id,
            passenger
        )

    except PassengerNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except PassengerAlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update passenger"
        )