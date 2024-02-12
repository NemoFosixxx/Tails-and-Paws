import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('core/database/new.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS default_profile(user_id TEXT PRIMARY KEY, username TEXT)")

    cur.execute(
        'CREATE TABLE IF NOT EXISTS authorized_profile(user_id TEXT PRIMARY KEY, username TEXT)')

    db.commit()


async def create_profile(user_id, username):
    user = cur.execute(
        "SELECT 1 FROM default_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO default_profile VALUES(?, ?)",
                    (user_id, username))
    db.commit()


async def upgrade_profile(user_id, username):
    user = cur.execute(
        "SELECT 1 FROM default_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if user:
        cur.execute(
            "DELETE FROM default_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
        cur.execute("INSERT INTO authorized_profile VALUES(?, ?)",
                    (user_id, username))
    db.commit()


async def delete_profile(user_id, username):
    user = cur.execute(
        "SELECT 1 FROM authorized_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if user:
        cur.execute(
            "DELETE FROM authorized_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
        cur.execute("INSERT INTO default_profile VALUES(?, ?)",
                    (user_id, username))
    db.commit()


async def check_user_exist(user_id):
    user = cur.execute(
        "SELECT 1 FROM authorized_profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    return bool(user)


async def get_default_users():
    return cur.execute("SELECT user_id FROM default_profile").fetchall
