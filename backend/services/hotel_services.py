from backend.repository.hotel_repository import (
    create_hotel as repository_create_hotel,
    get_all_hotels as repository_get_all_hotels,
    get_hotel_by_id as repository_get_hotel_by_id,
    update_hotel as repository_update_hotel,
    delete_hotel as repository_delete_hotel,
    HotelDatabaseException
)


class HotelNotFoundException(Exception):
    pass


def create_hotel(hotel_data):
    return repository_create_hotel(hotel_data)


def get_all_hotels():
    return repository_get_all_hotels()


def get_hotel_by_id(hotel_id: int):

    hotel = repository_get_hotel_by_id(hotel_id)

    if not hotel:
        raise HotelNotFoundException(
            f"Hotel with id {hotel_id} not found"
        )

    return hotel


def update_hotel(hotel_id: int, hotel_data):

    existing_hotel = repository_get_hotel_by_id(hotel_id)

    if not existing_hotel:
        raise HotelNotFoundException(
            f"Hotel with id {hotel_id} not found"
        )

    data = hotel_data.model_dump(
        exclude_unset=True
    )

    return repository_update_hotel(
        hotel_id,
        data
    )


def delete_hotel(hotel_id: int):

    existing_hotel = repository_get_hotel_by_id(hotel_id)

    if not existing_hotel:
        raise HotelNotFoundException(
            f"Hotel with id {hotel_id} not found"
        )

    repository_delete_hotel(hotel_id)

    return True