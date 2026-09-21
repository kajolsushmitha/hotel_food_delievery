from backend.repository.menu_repository import (
    hotel_exists,
    create_menu_item,
    get_menu_items_by_hotel,
    get_menu_item_by_id,
    get_menu_item_by_name,
    update_menu_item,
    delete_menu_item,
    HotelNotFoundException
)


class MenuItemAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.message = f"Menu item '{name}' is already available in this hotel"
        super().__init__(self.message)


def add_menu_item(hotel_id: int, menu_data):

    if not hotel_exists(hotel_id):
        raise HotelNotFoundException(
            f"Hotel with id {hotel_id} not found"
        )

    existing_item = get_menu_item_by_name(hotel_id, menu_data.name)
    if existing_item:
        raise MenuItemAlreadyExistsException(menu_data.name)

    return create_menu_item(hotel_id, menu_data)


def get_hotel_menu(hotel_id: int):

    if not hotel_exists(hotel_id):
        raise HotelNotFoundException(
            f"Hotel with id {hotel_id} not found"
        )

    return get_menu_items_by_hotel(hotel_id)


def get_menu(menu_id: int):

    return get_menu_item_by_id(menu_id)


def update_menu(menu_id: int, menu_data):

    current_item = get_menu_item_by_id(menu_id)

    if menu_data.name is not None:
        existing_item = get_menu_item_by_name(current_item["hotelId"], menu_data.name)
        if existing_item and existing_item["id"] != menu_id:
            raise MenuItemAlreadyExistsException(menu_data.name)

    return update_menu_item(menu_id, menu_data)


def delete_menu(menu_id: int):


    get_menu_item_by_id(menu_id)

    return delete_menu_item(menu_id)