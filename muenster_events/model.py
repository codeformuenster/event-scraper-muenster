"""Model functions for storing scraped event data."""

import sqlite3


def get_database_connection():
    """Get connection string to database."""
    return sqlite3.connect("data/events.db")


def execute_query(query_string):
    """Execute query_string on database."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(query_string)
    conn.commit()
    conn.close()


def initialize_database():
    """If not exists yet, create database and tables."""
    execute_query("CREATE TABLE IF NOT EXISTS event_ids (id integer);")
    execute_query("CREATE TABLE IF NOT EXISTS events(" +
                  "  id INT KEY," +
                  "  title TEXT, address TEXT, details TEXT, link TEXT," +
                  "  subtitle TEXT, time TEXT, location TEXT"
                  ");")


def get_event_ids():
    """Get ids of all events from DB."""
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT id FROM event_ids;")
    event_ids = [i[0] for i in c.fetchall()]
    conn.close()
    return event_ids


def add_event_ids_to_db(new_event_ids):
    """Add a list of new event ids to database table 'event_ids'."""
    # making new_event_ids unique
    new_event_ids = list(set(new_event_ids))
    # get list of ids from database
    db_event_ids = get_event_ids()
    # add new events to db
    conn = get_database_connection()
    c = conn.cursor()
    for new_event in new_event_ids:
        if int(new_event) not in db_event_ids:
            c.execute('INSERT INTO event_ids (id) VALUES (?);', (new_event,))
    conn.commit()
    conn.close()
