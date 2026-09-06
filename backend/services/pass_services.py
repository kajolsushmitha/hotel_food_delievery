from backend.repository.pass_repository import (
    create_passenger,
    get_passenger_by_phone,
    get_all_passengers,
    get_passenger_by_id,
    delete_passenger,
    update_passenger
)

class PassengerAlreadyExistsException(Exception):
    def __init__(self, phone: str):
        self.message = f"Passenger with phone {phone} already exists"
        super().__init__(self.message)


class PassengerNotFoundException(Exception):
    def __init__(self, passenger_id: int):
        self.message = f"Passenger with id {passenger_id} not found"
        super().__init__(self.message)


def add_passenger(passenger_data):
    existing_passenger = get_passenger_by_phone(
        passenger_data.phone
    )

    if existing_passenger:
        raise PassengerAlreadyExistsException(
            passenger_data.phone
        )

    return create_passenger(
        passenger_data.name,
        passenger_data.phone,
        passenger_data.busNo,
        passenger_data.email,
        passenger_data.age,
        passenger_data.gender,
        passenger_data.seatNo
    )


def get_passengers():
    return get_all_passengers()


def get_passenger(passenger_id: int):
    passenger = get_passenger_by_id(passenger_id)

    if passenger is None:
        raise PassengerNotFoundException(passenger_id)

    return passenger


def remove_passenger(passenger_id: int):
    passenger = get_passenger_by_id(passenger_id)

    if passenger is None:
        raise PassengerNotFoundException(passenger_id)

    delete_passenger(passenger_id)

    return {
        "message": f"Passenger with id {passenger_id} deleted successfully"
    }

def edit_passenger(passenger_id: int, passenger_data):

    passenger = get_passenger_by_id(passenger_id)

    if passenger is None:
        raise PassengerNotFoundException(passenger_id)

    if passenger_data.phone is not None:

        existing_passenger = get_passenger_by_phone(
            passenger_data.phone
        )

        if (
            existing_passenger
            and existing_passenger.id != passenger_id
        ):
            raise PassengerAlreadyExistsException(
                passenger_data.phone
            )

    updated = update_passenger(
        passenger_id,
        passenger_data
    )

    if updated is None:
        return get_passenger_by_id(passenger_id)

    return get_passenger_by_id(passenger_id)