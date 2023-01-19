import argparse

import psycopg2

from config import get_config

def connect(movie_name):
    """ Connect to the PostgreSQL database server """
    conn: psycopg2._psycopg.connection = None
    try:
        # read connection parameters
        params = get_config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(host='localhost', username='postgres', ...)

        # create a cursor
        cur: psycopg2._psycopg.cursor = conn.cursor()

        # cur.close()

        # execute a statement
        print('Getting info about some movie')

        cur.close()


        # cur2 = conn.cursor()
        # provided_rating = 9
        # cur2.execute(f"SELECT * from imdb_top WHERE rating>{provided_rating}")
        # d2_rating = cur2.fetchall()
        # if d2_rating is None:
        #     print(f"No data found with rating > {provided_rating}")
        # else:
        #     print(f"Found {len(movie_data)} matches:")
        #     for movie in movie_data:
        #         print(f"\n"
        #               f"Movie name : {movie[0]}\n"
        #               f"Release date: {movie[1]}\n"
        #               f"Rating: {movie[2]}\n")
        # cur2.close()

        get_movie_info_by_name(db_connection=conn, movie_name=movie_name)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_movie_info_by_name(db_connection:psycopg2._psycopg.connection, movie_name ):
    cur: psycopg2._psycopg.cursor = db_connection.cursor()
    cur.execute(f"SELECT * from imdb_top WHERE movie_name  iLIKE '%{movie_name}%'")
    # cur.execute('SELECT * from bbb')

    # display the PostgreSQL database server version
    movie_data = cur.fetchall()

    if movie_data is None:
        print(f"No movie found")
    else:
        print(f"Found {len(movie_data)} matches:")
        for movie in movie_data:
            print(f"\n"
                  f"Movie name : {movie[0]}\n"
                  f"Release date: {movie[1]}\n"
                  f"Rating: {movie[2]}\n")
    cur.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog="IMDB seeker"
    )
    # parser.add_argument("imdb")
    parser.add_argument("-n", "--name", help="Name of the movie or part of it")
    input_data = parser.parse_args()._get_kwargs()[0][1]
    print(parser.parse_args()._get_kwargs()[0][1])

    # input_data = 'incept'

    connect(input_data)