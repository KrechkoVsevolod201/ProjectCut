import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_project(conn, history):
    """
    Create a new project into the projects table
    :param conn:
    :param history:
    :return: f_name
    """
    sql = ''' INSERT INTO history(name,directory,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, history)
    conn.commit()
    return cur.lastrowid


def create_task(conn, picture):
    """
    Create a new picture
    :param conn:
    :param picture:
    :return:
    """

    sql = ''' INSERT INTO pictures(f_name,date,hist_id,type,photo)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, picture)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"D:\PycharmProjects\ProjectCut\DATABase\sqlite\GCHist\Debas.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        history = ('Dro4ilnya', '2015-01-01', '2015-01-30');
        hist_id = create_project(conn, history)

        # tasks
        picture_1 = ('chlepozdilo', '2015-01-01', hist_id, 1, 'jnfsjnfj')
        picture_2 = ('Kak je ja zaebalsya', '2025-01-01', hist_id, 3, 'Pizdos')

        # create tasks
        create_task(conn, picture_1)
        create_task(conn, picture_2)


if __name__ == '__main__':
    main()