from fastapi import APIRouter, HTTPException, Depends, status

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
    delete_menu,
    MenuItemAlreadyExistsException
)

from backend.repository.menu_repository import (
    MenuDatabaseException,
    MenuNotFoundException,
    HotelNotFoundException
)
from backend.dependencies.auth_dependency import get_current_hotel


router = APIRouter(
    tags=["Menu"])


@router.post(
    "/hotels/{hotel_id}/menu",
    response_model=MenuItemResponse,
    status_code=201
)
def create_menu(
    hotel_id: int,
    menu_data: MenuItemCreate,
    current_hotel: dict = Depends(get_current_hotel)
):
    if current_hotel["id"] != hotel_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only add menu items to your own hotel"
        )

    try:
        return add_menu_item(hotel_id, menu_data)

    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuItemAlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
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
    menu_data: MenuItemUpdate,
    current_hotel: dict = Depends(get_current_hotel)
):
    # Verify ownership before updating
    try:
        item = get_menu(menu_id)
        if item["hotelId"] != current_hotel["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only update menu items belonging to your hotel"
            )
        return update_menu(menu_id, menu_data)

    except MenuNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except MenuItemAlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except HTTPException:
        raise

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete(
    "/menu/{menu_id}"
)
def remove_menu_item(
    menu_id: int,
    current_hotel: dict = Depends(get_current_hotel)
):
    
    try:
        item = get_menu(menu_id)
        if item["hotelId"] != current_hotel["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only delete menu items belonging to your hotel"
            )

        delete_menu(menu_id)

        return {
            "message": f"Menu item {menu_id} deleted successfully"
        }

    except MenuNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except HTTPException:
        raise

    except MenuDatabaseException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )