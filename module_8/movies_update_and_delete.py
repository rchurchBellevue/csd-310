import mysql.connector
from mysql.connector import errorcode

config= {
"user": "movies_user",
"password": "popcorn",
"host": "127.0.0.1",
"database": "movies",
"raise_on_warnings": True
}

def show_fims(cursor,title):
    sql_query_string = """
       SELECT film_name as Name,film_director as Director,genre_name as Genre,studio_name as 'Studio Name' 
       FROM film INNER JOIN studio on film.studio_id=studio.studio_id 
       INNER JOIN genre on film.genre_id=genre.genre_id;"""
    cursor.execute(sql_query_string)
    movies = cursor.fetchall()
    print('\n  ---{} --'.format(title))
    for movie in movies:
        print("Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n "
              .format(movie[0], movie[1], movie[2], movie[3]))


try:
   db = mysql.connector.connect(**config)
   cursor = db.cursor()

   # First Query:
   show_fims(cursor,'DISPLAYING FILMS')

   sql_insert_string = """
          INSERT INTO film  (film_name,film_releaseDate,film_runtime,film_director,studio_id,genre_id)
          VALUES ('Star Wars','1977',121,'George Lucas',1,2)"""
   cursor.execute(sql_insert_string)
   show_fims(cursor, 'DISPLAYING FILMS AFTER INSERT')

   sql_update_string = "UPDATE film SET film.genre_id=1 WHERE film_name='Alien'"
   cursor.execute(sql_update_string)
   show_fims(cursor, 'DISPLAYING FILMS AFTER UPDATE Changed Alien to Horror')

   sql_delete_string = "DELETE FROM film WHERE film_name='Gladiator'"
   cursor.execute(sql_delete_string)
   show_fims(cursor, 'DISPLAYING FILMS AFTER DELETE')

except mysql.connector.Error as err:
    if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
	    print("  The supplied username or password are invalid")
    elif err.errno==errorcode.ER_BAD_DB_ERROR:
	    print("  The specified database does not exist")
    else:
	    print(err)

finally:
    db.close()