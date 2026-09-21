from fastapi import APIRouter, HTTPException, Depends, status
from backend.schema.pass_schema import PassengerUpdate, PassengerCreate
from backend.services.pass_services import (
    add_passenger,
    get_passengers,
    get_passenger,
    remove_passenger,
    edit_passenger,
    PassengerAlreadyExistsException,
    PassengerNotFoundException
)
from backend.dependencies.auth_dependency import get_current_passenger
from backend.model.pass_model import Passenger

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
def delete_passenger_by_id(
    passenger_id: int,
    current_passenger: Passenger = Depends(get_current_passenger)
):
    if current_passenger.id != passenger_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only delete your own profile"
        )

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
    passenger: PassengerUpdate,
    current_passenger: Passenger = Depends(get_current_passenger)
):
    if current_passenger.id != passenger_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only update your own profile"
        )

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