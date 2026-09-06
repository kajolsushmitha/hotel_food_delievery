from fastapi import APIRouter, HTTPException, status

from backend.schema.menu_schema import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)

from backend.services.menu_services import (
    add_menu_item,
    get_hotel_menu,
    get_menu,
    update_menu,
    delete_menu
)

from backend.repository.menu_repository import (
    MenuDatabaseException,
    MenuNotFoundException,
    HotelNotFoundException
)


router = APIRouter(
    tags=["Menu"])


@router.post(
    "/hotels/{hotel_id}/menu",
    response_model=MenuItemResponse,
    status_code=201
)
def create_menu(
    hotel_id: int,
    menu_data: MenuItemCreate
):
    try:
        return add_menu_item(hotel_id, menu_data)

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/hotels/{hotel_id}/menu",
    response_model=list[MenuItemResponse]
)
def get_hotel_menu_items(hotel_id: int):

    try:
        return get_hotel_menu(hotel_id)

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/menu/{menu_id}",
    response_model=MenuItemResponse
)
def get_menu_item(menu_id: int):

    try:
        return get_menu(menu_id)

    except MenuNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.patch(
    "/menu/{menu_id}",
    response_model=MenuItemResponse
)
def patch_menu_item(
    menu_id: int,
    menu_data: MenuItemUpdate
):

    try:
        return update_menu(menu_id, menu_data)

    except MenuNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete(
    "/menu/{menu_id}"
)
def remove_menu_item(menu_id: int):

    try:
        delete_menu(menu_id)

        return {
            "message": f"Menu item {menu_id} deleted successfully"
        }

    except MenuNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )