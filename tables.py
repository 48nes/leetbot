import os
import psycopg2 as sql
from psycopg2 import OperationalError

DATABASE_URL = os.environ['DATABASE_URL']

conn = sql.connect(DATABASE_URL, sslmode='require')


def connect(db_name, user_, password_, host_ip, port_):
    connection = None
    try:
        connection = sql.connect(
            database=db_name,
            user=user_,
            password=password_,
            host=host_ip,
            port=port_
        )
        print("Connection successful.")
    except OperationalError as e:
        print(f"Error '{e}' has occurred.")
    return connection


def query(connection, query_db):
    connection.autocommit = True

    try:
        connection.cursor().execute(query_db)
        print("Query executed.")
    except OperationalError as e:
        print(f"Error '{e}' has occurred.")


def create_tables():
    sql_commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            discord_id BIGINT PRIMARY KEY,
            leetcode_username TEXT NOT NULL,
            num_total INTEGER NOT NULL,
            num_easy INTEGER NOT NULL,
            num_medium INTEGER NOT NULL,
            num_hard INTEGER NOT NULL
        );
        """)
    sql_conn = None
    try:
        # connect to the PostgreSQL server
        sql_conn = sql.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        # create table one by one
        for command in sql_commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        sql_conn.commit()
    except (Exception, sql.DatabaseError) as error:
        print(error)
    finally:
        if sql_conn is not None:
            sql_conn.close()


def check_discord(discord_id):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT leetcode_username FROM users WHERE discord_id=%s", (discord_id,))
    leetcode = cur.fetchone()
    con.close()
    if leetcode is None:
        return ""
    else:
        return leetcode


def check_leetcode(leetcode_username):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT 1 FROM users WHERE leetcode_username=%s", (leetcode_username,))
    users = cur.fetchone()
    con.close()
    if users is None:
        return ""
    else:
        return users


def insert_into_table(discord_id, leetcode_username, num_total, num_easy, num_medium, num_hard):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (discord_id,leetcode_username,num_total,num_easy,num_medium,num_hard) VALUES (%s,%s,%s,"
        "%s,%s,%s)",
        (discord_id, leetcode_username, num_total, num_easy, num_medium, num_hard,))
    con.commit()
    con.close()


def remove_from_table(discord_id):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "DELETE FROM users WHERE discord_id=%s", (discord_id,))
    con.commit()
    con.close()


def remove_by_leetcode(leetcode_username):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "DELETE FROM users WHERE leetcode_username=%s", (leetcode_username,))
    con.commit()
    con.close()


def select_all():
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT leetcode_username, num_total FROM users")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows

