import psycopg2
from constants import *
import bcrypt


connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                              user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
pointer = connection.cursor()


# def get_user_id(username):
#     try:
#         pointer.execute(
#             f"SELECT id FROM User WHERE username='{username}'")
#         result = pointer.fetchone()
#         if result:
#             return result[0]
#         else:
#             return None
#     except psycopg2.Error as e:
#         print(ERROR_MESSAGE, e)
#         return None


def get_name(username):
    try:
        pointer.execute(
            f"SELECT first_name FROM \"user\" WHERE username='{username}'")
        first_name = pointer.fetchone()
        pointer.execute(
            f"SELECT last_name FROM \"user\" WHERE username='{username}'")
        last_name = pointer.fetchone()

        if first_name[0] and last_name[0]:
            return first_name[0], last_name[0]
        else:
            return False
    except psycopg2.Error as e:
        print(ERROR_MESSAGE, e)
        return False


def username_check(username):
    try:
        pointer.execute(
            f"SELECT * FROM \"user\" WHERE username='{username}'")
        result = pointer.fetchone()
        if result:
            return True
        else:
            return False
    except psycopg2.Error as e:
        print(ERROR_MESSAGE, e)
        return False


def password_check(username, password):
    try:
        pointer.execute(
            f"SELECT * FROM \"user\" WHERE username='{username}'")
        result = pointer.fetchone()

        if result[4] == bcrypt.hashpw(password.encode('utf-8'), result[4].encode('utf-8')).decode('utf-8'):
            pointer.execute(
                f"SELECT * FROM \"user\" WHERE username = '{username}'")
            result = pointer.fetchone()
            if result:
                return True
            else:
                return False
        else:
            return False
    except psycopg2.Error as e:
        print(ERROR_MESSAGE, e)
        return False


def check_file(user_id):
    try:
        query = """
        SELECT file_path FROM \"transcript_file\"
        WHERE username = %s;
        """
        pointer.execute(query, (user_id,))
        result = pointer.fetchone()

        if result:
            return result[0]
        else:
            return False
    except psycopg2.Error as e:
        print(ERROR_MESSAGE, e)
        return False


def set_opinion(user_opinion, user_id):
    try:
        query = """
        INSERT INTO \"comment\" (username, comment_text)
        VALUES (%s, %s);
        """
        pointer.execute(query, (user_id, user_opinion))
        connection.commit()
    except psycopg2.Error as e:
        print(ERROR_MESSAGE, e)
        return False
