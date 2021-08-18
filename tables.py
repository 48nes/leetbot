import os
import psycopg2 as sql
from psycopg2 import OperationalError

DATABASE_URL = os.environ['DATABASE_URL']

'''
Executes the SQL query on the database connected to the connection object.
:type connection: Connection
:type query_db: String
:return: void
'''
def query(connection, query_db):
    connection.autocommit = True

    try:
        connection.cursor().execute(query_db)
        print("Query executed.")
    except OperationalError as e:
        print(f"Error '{e}' has occurred.")

'''
Gets the leetcode username associated with the given discord id or the empty 
string if there is none.
:type discord_id: Long
:return: String
'''
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

'''
Checks if the leetcode username is contained in the database. Returns 1 if true, or the empty string if false.
:type leetcode_username: String
:return: String
'''
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

'''
Gets the top ten leetcode users stored in the database. 
This is determined by problems done, either all, easy, medium, or hard problems.
:type type: String
:return: List[tuples]
:ValueError: if the type is not supported.
'''
def get_top10(type):
    lowered_type = type.lower()
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    
    if (lowered_type == "" or lowered_type == "all"):
        cur.execute("SELECT leetcode_username, num_total FROM users ORDER BY num_total desc FETCH FIRST 10 ROWS ONLY")
    elif (lowered_type == "easy"):
        cur.execute("SELECT leetcode_username, num_easy FROM users ORDER BY num_easy desc FETCH FIRST 10 ROWS ONLY")
    elif (lowered_type == "medium"):
        cur.execute("SELECT leetcode_username, num_medium FROM users ORDER BY num_medium desc FETCH FIRST 10 ROWS ONLY")
    elif (lowered_type == "hard"):
        cur.execute("SELECT leetcode_username, num_hard FROM users ORDER BY num_hard desc FETCH FIRST 10 ROWS ONLY")
    else:
        raise ValueError("Invalid problem type for leaderboards")
    
    top10 = cur.fetchall()
    con.close()
    return top10

'''
Inserts the leetcode profile under the given discord id into the database.
:type discord_id: Long
:type leetcode_username: String
:type num_total: int
:type num_easy: int
:type num_medium: int
:type num_hard: int
:type total_subs: int
:return: void
'''
def insert_into_table(discord_id, leetcode_username, num_total, num_easy, num_medium, num_hard, total_subs):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (discord_id,leetcode_username,num_total,num_easy,num_medium,num_hard,total_subs) VALUES ("
        "%s,%s,%s,%s,%s,%s,%s)",
        (discord_id, leetcode_username, num_total, num_easy, num_medium, num_hard, total_subs,))
    con.commit()
    con.close()

"""
Removes the user associated with the given discord id from the database if the user exists.
:type discord_id: Long
:return: void
"""
def remove_from_table(discord_id):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "DELETE FROM users WHERE discord_id=%s", (discord_id,))
    con.commit()
    con.close()

"""
Removes the user associated with the given leetcode username from the database if the user exists.
:type leetcode_username: String
:return: void
"""
def remove_by_leetcode(leetcode_username):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "DELETE FROM users WHERE leetcode_username=%s", (leetcode_username,))
    con.commit()
    con.close()

"""
Returns a list of all users in the database with their leetcode usernames and total submissions.
:return: List[tuple]
"""
def select_all():
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT leetcode_username, total_subs FROM users")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows

'''
Updates the given user's information in the database.
:type leetcode_username: String
:type num_total: int
:type num_easy: int
:type num_medium: int
:type num_hard: int
:type total_subs: int
:return: void
'''
def update_table(leetcode_username, num_total, num_easy, num_medium, num_hard, total_subs):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET num_total=%s, num_easy=%s, num_medium=%s, num_hard=%s, total_subs=%s WHERE "
        "leetcode_username=%s", (num_total, num_easy, num_medium, num_hard, total_subs, leetcode_username,))
    con.commit()
    con.close()

'''
Gets the last channel that the bot was connected to
:return: int
'''
def get_last_channel():
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT * FROM channel")
    channel = cur.fetchone()[0]
    con.close()
    return channel

'''
Updates the database with the new channel
:type channel: int
:return: void
'''
def set_channel(channel):
    con = sql.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("UPDATE channel SET last_channel=" + str(channel))
    con.commit()
    con.close()
