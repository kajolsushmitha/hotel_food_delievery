import mysql.connector
from backend.db import get_connection
from backend.model.pass_model import Passenger


class PassengerDatabaseException(Exception):
    pass


def get_passenger_by_phone(phone: str):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                name,
                phone,
                busNo,
                email,
                age,
                gender,
                seatNo
            FROM passenger
            WHERE phone = %s
        """

        cursor.execute(query, (phone,))
        row = cursor.fetchone()

        if row:
            return Passenger(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                busNo=row["busNo"],
                email=row["email"],
                age=row["age"],
                gender=row["gender"],
                seatNo=row["seatNo"]
            )

        return None

    except mysql.connector.Error as e:
        raise PassengerDatabaseException(
            f"Failed to check passenger: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def create_passenger(
    name: str,
    phone: str,
    busNo: str,
    email: str,
    age: int,
    gender: str,
    seatNo: int
) -> Passenger:

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO passenger
            (name, phone, busNo, email, age, gender, seatNo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            phone,
            busNo,
            email,
            age,
            gender,
            seatNo
        )

        cursor.execute(query, values)
        connection.commit()

        passenger_id = cursor.lastrowid

        return Passenger(
            id=passenger_id,
            name=name,
            phone=phone,
            busNo=busNo,
            email=email,
            age=age,
            gender=gender,
            seatNo=seatNo
        )

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise PassengerDatabaseException(
            f"Failed to create the passenger: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_all_passengers():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                name,
                phone,
                busNo,
                email,
                age,
                gender,
                seatNo
            FROM passenger
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        passengers = []

        for row in rows:
            passengers.append(
                Passenger(
                    id=row["id"],
                    name=row["name"],
                    phone=row["phone"],
                    busNo=row["busNo"],
                    email=row["email"],
                    age=row["age"],
                    gender=row["gender"],
                    seatNo=row["seatNo"]
                )
            )

        return passengers

    except mysql.connector.Error as e:
        raise PassengerDatabaseException(
            f"Failed to fetch passengers: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_passenger_by_id(passenger_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                id,
                name,
                phone,
                busNo,
                email,
                age,
                gender,
                seatNo
            FROM passenger
            WHERE id = %s
        """

        cursor.execute(query, (passenger_id,))
        row = cursor.fetchone()

        if row:
            return Passenger(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                busNo=row["busNo"],
                email=row["email"],
                age=row["age"],
                gender=row["gender"],
                seatNo=row["seatNo"]
            )

        return None

    except mysql.connector.Error as e:
        raise PassengerDatabaseException(
            f"Failed to fetch passenger: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def delete_passenger(passenger_id: int):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM passenger
            WHERE id = %s
        """

        cursor.execute(query, (passenger_id,))

        if cursor.rowcount == 0:
            return False

        connection.commit()

        return True

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise PassengerDatabaseException(
            f"Failed to delete passenger: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def update_passenger(passenger_id: int, passenger_data):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        data = passenger_data.model_dump(exclude_unset=True)

        if not data:
            return None

        fields = []
        values = []

        for field, value in data.items():
            fields.append(f"{field} = %s")
            values.append(value)

        query = f"""
            UPDATE passenger
            SET {", ".join(fields)}
            WHERE id = %s
        """

        values.append(passenger_id)

        cursor.execute(query, tuple(values))

        if cursor.rowcount == 0:
            return None

        connection.commit()

        return True

    except mysql.connector.Error as e:
        if connection:
            connection.rollback()

        raise PassengerDatabaseException(
            f"Failed to update passenger: {str(e)}"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()