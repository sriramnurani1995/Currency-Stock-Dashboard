from datetime import date
from .Model import Model
import sqlite3

DB_FILE = 'entries.db'  

class model(Model):
    def __init__(self):
        """
        Initializes the database connection and ensures that the necessary tables 
        (artists, genres, songs) are created if they do not already exist.

        The following tables are created:
        - artists: Stores artist names, with a UNIQUE constraint to avoid duplicates.
        - genres: Stores genre names, with a UNIQUE constraint to avoid duplicates.
        - songs: Stores song information, referencing artists and genres using foreign keys.

        A persistent connection to the SQLite database is established in this method, 
        and will be reused throughout the lifetime of this instance.

        :raises sqlite3.OperationalError: If there's an issue with the database during 
                                          table creation or connection.
        """
        self.conn = sqlite3.connect(DB_FILE)  
        cursor = self.conn.cursor()

        # Attempt to check if the 'songs' table exists, create tables if not
        try:
            cursor.execute("SELECT count(rowid) FROM songs")
        except sqlite3.OperationalError:
            # Create artists table: artist names must be unique to avoid duplicates
            cursor.execute('''CREATE TABLE IF NOT EXISTS artists (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

            # Create genres table: genre names must be unique to avoid duplicates
            cursor.execute('''CREATE TABLE IF NOT EXISTS genres (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

            # Create songs table: stores song details and references artist and genre
            cursor.execute('''CREATE TABLE IF NOT EXISTS songs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                artist_id INTEGER,
                                genre_id INTEGER,
                                release_date TEXT,
                                lyrics TEXT,
                                rating REAL,
                                FOREIGN KEY (artist_id) REFERENCES artists(id),
                                FOREIGN KEY (genre_id) REFERENCES genres(id))''')

        cursor.close()

    def add_artist(self, name):
        """
        Inserts a new artist into the 'artists' table if the artist does not already exist.
        
        This method ensures that each artist has a unique name due to the UNIQUE constraint 
        on the 'name' column. The method inserts the artist and returns the auto-generated 
        artist ID for use in other operations.

        :param name: The name of the artist to be added.
        :return: The ID of the newly inserted or existing artist.
        :raises sqlite3.DatabaseError: If there's an issue with inserting the artist into the database.
        """
        cursor = self.conn.cursor()  # Reuse the persistent connection
        cursor.execute('INSERT INTO artists (name) VALUES (?)', (name,))
        artist_id = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return artist_id

    def add_genre(self, name):
        """
        Inserts a new genre into the 'genres' table if it does not already exist.
        
        This method ensures that each genre has a unique name due to the UNIQUE constraint 
        on the 'name' column. If a genre with the given name already exists, it will be ignored.

        :param name: The name of the genre to be added.
        :return: The ID of the newly inserted or existing genre.
        :raises sqlite3.DatabaseError: If there's an issue with inserting the genre into the database.
        """
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO genres (name) VALUES (?)', (name,))
        genre_id = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return genre_id

    def add_song(self, title, artist, genre, release_date, lyrics, rating):
        """
        Inserts a new song into the 'songs' table, linking it with the appropriate artist and genre.

        This method first ensures that the artist and genre exist in their respective tables 
        by calling the 'add_artist' and 'add_genre' methods. The song is then inserted with 
        references (foreign keys) to the artist and genre.

        :param title: The title of the song.
        :param artist: The name of the artist performing the song.
        :param genre: The name of the genre the song belongs to.
        :param release_date: The release date of the song.
        :param lyrics: The lyrics of the song.
        :param rating: The rating of the song (numeric value).
        :return: None
        :raises sqlite3.DatabaseError: If there's an issue with inserting the song into the database.
        """
        artist_id = self.add_artist(artist)  # Ensure the artist exists
        genre_id = self.add_genre(genre)     # Ensure the genre exists

        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO songs (title, artist_id, genre_id, release_date, lyrics, rating)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                          (title, artist_id, genre_id, release_date, lyrics, rating))
        self.conn.commit()
        cursor.close()

    def get_all_songs(self):
        """
        Retrieves all songs from the 'songs' table, including associated artist and genre names.

        This method performs an INNER JOIN to combine data from the 'songs', 'artists', and 'genres' 
        tables, ensuring that only songs with valid artist and genre entries are returned.

        :return: A list of tuples, where each tuple contains the song title, artist name, genre name, 
                 release date, lyrics, and rating.
        :raises sqlite3.DatabaseError: If there's an issue retrieving the songs from the database.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT songs.title, artists.name AS artist, genres.name AS genre, 
                          songs.release_date, songs.lyrics, songs.rating 
                          FROM songs
                          INNER JOIN artists ON songs.artist_id = artists.id
                          INNER JOIN genres ON songs.genre_id = genres.id''')
        songs = cursor.fetchall()
        cursor.close()
        return songs

    def close(self):
        """
        Closes the persistent connection to the SQLite database.

        This method should be called when the application is finished interacting with the database
        to ensure that all resources are properly released.

        :return: None
        """
        self.conn.close()  
