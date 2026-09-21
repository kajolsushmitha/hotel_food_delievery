import mysql.connector
from backend.db import get_connection


class MenuDatabaseException(Exception):
    pass


class MenuNotFoundException(Exception):
    pass


class HotelNotFoundException(Exception):
    pass


def hotel_exists(hotel_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT id
            FROM hotel
            WHERE id = %s
        """

        cursor.execute(query, (hotel_id,))
        result = cursor.fetchone()

        return result is not None

    except mysql.connector.Error as e:
        raise MenuDatabaseException(
            f"Database error while checking hotel: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_menu_item_by_name(hotel_id: int, name: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                hotelId,
                name,
                description,
                price,
                category,
                is_available
            FROM menu_item
            WHERE hotelId = %s AND LOWER(TRIM(name)) = LOWER(TRIM(%s))
            LIMIT 1
        """

        cursor.execute(query, (hotel_id, name))
        return cursor.fetchone()

    except mysql.connector.Error as e:
        raise MenuDatabaseException(
            f"Database error while checking menu item by name: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def create_menu_item(hotel_id: int, menu_data):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO menu_item
            (
                hotelId,
                name,
                description,
                price,
                category,
                is_available
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            hotel_id,
            menu_data.name,
            menu_data.description,
            menu_data.price,
            menu_data.category,
            menu_data.is_available
        )

        cursor.execute(query, values)
        connection.commit()

        menu_id = cursor.lastrowid

        return get_menu_item_by_id(menu_id)

    except mysql.connector.IntegrityError as e:
        if connection:
            connection.rollback()

        raise MenuDatabaseException(
            f"Database integrity error: {str(e)}"
        )

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise MenuDatabaseException(
            f"Database error while creating menu item: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_menu_items_by_hotel(hotel_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                hotelId,
                name,
                description,
                price,
                category,
                is_available
            FROM menu_item
            WHERE hotelId = %s
            ORDER BY id
        """

        cursor.execute(query, (hotel_id,))
        return cursor.fetchall()

    except mysql.connector.Error as e:
        raise MenuDatabaseException(
            f"Database error while fetching menu items: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_menu_item_by_id(menu_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                hotelId,
                name,
                description,
                price,
                category,
                is_available
            FROM menu_item
            WHERE id = %s
        """

        cursor.execute(query, (menu_id,))
        result = cursor.fetchone()

        if not result:
            raise MenuNotFoundException(
                f"Menu item with id {menu_id} not found"
            )

        return result

    except MenuNotFoundException:
        raise

    except mysql.connector.Error as e:
        raise MenuDatabaseException(
            f"Database error while fetching menu item: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_menu_item(menu_id: int, menu_data):
    connection = None
    cursor = None

    allowed_fields = {
        "name",
        "description",
        "price",
        "category",
        "is_available"
    }

    try:
        data = menu_data.model_dump(
            exclude_unset=True,
            include=allowed_fields
        )

        if not data:
            return get_menu_item_by_id(menu_id)

        connection = get_connection()
        cursor = connection.cursor()

        set_clauses = []
        values = []

        for field, value in data.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)

        values.append(menu_id)

        query = f"""
            UPDATE menu_item
            SET {", ".join(set_clauses)}
            WHERE id = %s
        """

        cursor.execute(query, tuple(values))

        if cursor.rowcount == 0:
            connection.rollback()

            get_menu_item_by_id(menu_id)

        connection.commit()

        return get_menu_item_by_id(menu_id)

    except MenuNotFoundException:
        raise

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise MenuDatabaseException(
            f"Database error while updating menu item: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_menu_item(menu_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM menu_item
            WHERE id = %s
        """

        cursor.execute(query, (menu_id,))

        if cursor.rowcount == 0:
            connection.rollback()

            raise MenuNotFoundException(
                f"Menu item with id {menu_id} not found"
            )

        connection.commit()

        return True

    except MenuNotFoundException:
        raise

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise MenuDatabaseException(
            f"Database error while deleting menu item: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()