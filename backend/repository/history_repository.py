import json

from backend.db import get_connection
from backend.model.history_model import HotelOrderHistory


def get_order_history(
    hotel_id: int,
    start_time=None,
    end_time=None,
    limit=20,
    offset=0
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                o.id AS id,
                o.hotelId,
                o.passengerId,
                o.id AS orderId,
                UNIX_TIMESTAMP(o.orderTime) AS orderTimestamp,
                CAST(o.totalAmount AS FLOAT) AS totalAmount,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'id', oi.id,
                        'menuItemId', oi.menuItemId,
                        'quantity', oi.quantity,
                        'price', CAST(oi.price AS FLOAT),
                        'subtotal', CAST(oi.subtotal AS FLOAT)
                    )
                ) AS items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.orderId
            WHERE o.hotelId = %s
        """

        parameters = [hotel_id]

        if start_time is not None:
            query += """
                AND o.orderTime >= %s
            """
            parameters.append(start_time)

        if end_time is not None:
            query += """
                AND o.orderTime <= %s
            """
            parameters.append(end_time)

        query += """
            GROUP BY o.id
            ORDER BY o.orderTime DESC
            LIMIT %s OFFSET %s
        """

        parameters.append(limit)
        parameters.append(offset)

        cursor.execute(query, parameters)

        rows = cursor.fetchall()

        order_history_list = []

        for row in rows:

            items = row["items"]

            if isinstance(items, str):
                items = json.loads(items)

            order_history = HotelOrderHistory(
                id=row["id"],
                hotel_id=row["hotelId"],
                passenger_id=row["passengerId"],
                order_id=row["orderId"],
                order_timestamp=row["orderTimestamp"],
                total_amount=row["totalAmount"],
                items=items
            )

            order_history_list.append(order_history)

        return order_history_list

    finally:
        cursor.close()
        connection.close()

def count_order_history(
    hotel_id: int,
    start_time=None,
    end_time=None
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT COUNT(*) AS total
            FROM orders o
            WHERE o.hotelId = %s
        """

        parameters = [hotel_id]

        if start_time is not None:
            query += """
                AND o.orderTime >= %s
            """
            parameters.append(start_time)

        if end_time is not None:
            query += """
                AND o.orderTime <= %s
            """
            parameters.append(end_time)

        cursor.execute(query, parameters)

        result = cursor.fetchone()

        return result["total"]

    finally:
        cursor.close()
        connection.close()