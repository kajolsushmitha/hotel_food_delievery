
from backend.db import get_connection

class HotelDatabaseException(Exception):
    pass


def create_hotel(hotel_data):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            INSERT INTO hotel
            (name, location, phone, is_active)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            hotel_data.name,
            hotel_data.location,
            hotel_data.phone,
            hotel_data.is_active
        )

        cursor.execute(query, values)
        connection.commit()

        hotel_id = cursor.lastrowid

        return get_hotel_by_id(hotel_id)

    except Exception as e:
        if connection:
            connection.rollback()

        raise HotelDatabaseException(
            f"Database error while creating hotel: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_all_hotels():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, name, location, phone, is_active
            FROM hotel
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Exception as e:
        raise HotelDatabaseException(
            f"Database error while fetching hotels: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_hotel_by_id(hotel_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, name, location, phone, is_active
            FROM hotel
            WHERE id = %s
        """

        cursor.execute(query, (hotel_id,))

        return cursor.fetchone()

    except Exception as e:
        raise HotelDatabaseException(
            f"Database error while fetching hotel: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_hotel_by_phone(phone: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, name, location, phone, is_active
            FROM hotel
            WHERE phone = %s
        """

        cursor.execute(query, (phone,))
        return cursor.fetchone()

    except Exception as e:
        raise HotelDatabaseException(
            f"Database error while fetching hotel by phone: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def update_hotel(hotel_id: int, data: dict):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        fields = []
        values = []

        for field, value in data.items():
            fields.append(f"{field} = %s")
            values.append(value)

        if not fields:
            return get_hotel_by_id(hotel_id)

        values.append(hotel_id)

        query = f"""
            UPDATE hotel
            SET {', '.join(fields)}
            WHERE id = %s
        """

        cursor.execute(query, tuple(values))
        connection.commit()

        return get_hotel_by_id(hotel_id)

    except Exception as e:
        if connection:
            connection.rollback()

        raise HotelDatabaseException(
            f"Database error while updating hotel: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def delete_hotel(hotel_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM hotel
            WHERE id = %s
        """

        cursor.execute(query, (hotel_id,))
        connection.commit()

        return cursor.rowcount

    except Exception as e:
        if connection:
            connection.rollback()

        raise HotelDatabaseException(
            f"Database error while deleting hotel: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_hotel_by_name(hotel_name: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, name, location, phone, is_active
            FROM hotel
            WHERE LOWER(name) = LOWER(%s)
               OR LOWER(name) LIKE CONCAT('%', LOWER(%s), '%')
            LIMIT 1
        """

        cursor.execute(query, (hotel_name, hotel_name))
        return cursor.fetchone()

    except Exception as e:
        raise HotelDatabaseException(
            f"Database error while searching hotel by name: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_active_hotels_with_menus():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                h.id AS hotel_id,
                h.name AS hotel_name,
                h.location AS hotel_location,
                m.id AS menu_id,
                m.name AS item_name,
                m.price,
                m.category,
                m.description,
                m.is_available
            FROM hotel h
            LEFT JOIN menu_item m ON h.id = m.hotelId AND m.is_available = 1
            WHERE h.is_active = 1
            ORDER BY h.name, m.name
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        raise HotelDatabaseException(
            f"Database error while fetching active hotels and menus: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()