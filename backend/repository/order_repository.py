import uuid
from backend.db import get_connection

def create_order(order_data):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            INSERT INTO orders
            (passengerId, hotelId, totalAmount)
            VALUES (%s, %s, %s)
        """

        values = (
            order_data.passengerId,
            order_data.hotelId,
            order_data.totalAmount
        )

        cursor.execute(query, values)
        order_id = cursor.lastrowid

        if hasattr(order_data, 'items') and order_data.items:
            item_query = """
                INSERT INTO order_items
                (id, orderId, menuItemId, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            item_values = [
                (
                    str(uuid.uuid4()),
                    order_id,
                    item.menuItemId,
                    item.quantity,
                    item.price,
                    item.subtotal
                )
                for item in order_data.items
            ]
            cursor.executemany(item_query, item_values)

        connection.commit()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE id = %s
            """,
            (order_id,)
        )

        return cursor.fetchone()

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_all_orders():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                o.id AS id,
                o.passengerId,
                p.name AS passengerName,
                p.phone AS passengerPhone,
                p.busNo AS busNo,
                p.email AS email,
                p.age AS age,
                p.gender AS gender,
                p.seatNo AS seatNo,

                o.hotelId,
                h.name AS hotelName,
                h.location AS hotelLocation,
                h.phone AS hotelPhone,

                o.totalAmount,
                o.status,
                o.orderTime

            FROM orders o

            JOIN passenger p
                ON o.passengerId = p.id

            JOIN hotel h
                ON o.hotelId = h.id

            ORDER BY o.orderTime DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_order_by_id(order_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                    o.id AS id,

                    o.passengerId,
                    p.name AS passengerName,
                    p.phone AS passengerPhone,
                    p.busNo,
                    p.email,
                    p.age,
                    p.gender,
                    p.seatNo,

                    o.hotelId,
                    h.name AS hotelName,
                    h.location AS hotelLocation,
                    h.phone AS hotelPhone,

                    o.totalAmount,
                    o.status,
                    o.orderTime

                FROM orders o

                JOIN passenger p
                    ON o.passengerId = p.id

                JOIN hotel h
                    ON o.hotelId = h.id

                WHERE o.id = %s
        """

        cursor.execute(query, (order_id,))

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_orders_by_passenger(passenger_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                o.id AS id,
                o.passengerId,

                o.hotelId,
                h.name AS hotelName,
                h.location AS hotelLocation,

                o.totalAmount,
                o.status,
                o.orderTime

            FROM orders o

            JOIN hotel h
                ON o.hotelId = h.id

            WHERE o.passengerId = %s

            ORDER BY o.orderTime DESC
        """

        cursor.execute(query, (passenger_id,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
 
def get_orders_by_hotel(hotel_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                o.id AS id,
                o.passengerId,
                p.name AS passengerName,
                p.phone AS passengerPhone,
                p.busNo,
                p.seatNo,
                o.hotelId,
                o.totalAmount,
                o.status,
                o.orderTime

            FROM orders o

            JOIN passenger p
                ON o.passengerId = p.id

            WHERE o.hotelId = %s

            ORDER BY o.orderTime DESC
        """

        cursor.execute(query, (hotel_id,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
            

def update_order_status(order_id: int, status: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            UPDATE orders
            SET status = %s
            WHERE id = %s
        """

        cursor.execute(query, (status, order_id))
        connection.commit()

        if cursor.rowcount == 0:
            return None

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE id = %s
            """,
            (order_id,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def delete_order(order_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM orders
            WHERE id = %s
        """

        cursor.execute(query, (order_id,))
        connection.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def delete_expired_orders(days: int = 30) -> list:
    """
    Deletes orders older than `days` (along with associated items) using TTL logic
    and returns the list of deleted orders.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Fetch expired orders before deletion
        fetch_query = """
            SELECT id, hotelId, passengerId, totalAmount, status, orderTime
            FROM orders
            WHERE orderTime < NOW() - INTERVAL %s DAY
        """
        cursor.execute(fetch_query, (days,))
        expired_orders = cursor.fetchall()

        if not expired_orders:
            return []

        expired_ids = [order["id"] for order in expired_orders]
        format_strings = ','.join(['%s'] * len(expired_ids))

        # 2. Delete associated order items
        delete_items_query = f"""
            DELETE FROM order_items
            WHERE orderId IN ({format_strings})
        """
        cursor.execute(delete_items_query, tuple(expired_ids))

        # 3. Delete expired orders
        delete_orders_query = f"""
            DELETE FROM orders
            WHERE id IN ({format_strings})
        """
        cursor.execute(delete_orders_query, tuple(expired_ids))

        connection.commit()
        return expired_orders

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()





