"""
This module manages the SQLite3 database for handling songs, artists, and genres.
It provides a series of functions to perform CRUD (Create, Read, Update, Delete) operations
on the song records and their associated artists and genres.

The database is stored in 'entries.db' and is used to store information about songs, including:
- `artists`: Stores artist names (unique).
- `genres`: Stores genre names (unique).
- `songs`: Stores details about songs, including foreign keys linking to `artists` and `genres`.
"""

from datetime import date
import sqlite3

DB_FILE = 'entries.db'  # File for storing the SQLite database

def get_db_connection():
    """
    Provides a new SQLite database connection for each request.

    :return: SQLite3 connection object.
    """
    return sqlite3.connect(DB_FILE)

class model:
    """
    SQLite3 model for managing song entries, including their related artists and genres.
    This class provides methods for creating, retrieving, updating, and deleting songs.
    
    Each method uses a separate database connection.
    """
    def __init__(self):
        """
        Initializes the database connection and ensures the required tables
        (artists, genres, songs) are created if they do not already exist.

        Tables created:
        - `artists`: Stores artist names, with a UNIQUE constraint to prevent duplicates.
        - `genres`: Stores genre names, with a UNIQUE constraint to prevent duplicates.
        - `songs`: Stores song information and references artists and genres via foreign keys.

        This method ensures the songs table exists, and if not, creates all required tables.
        """
        connection = get_db_connection()  # Get a new connection for setup
        cursor = connection.cursor()

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
        connection.close()

    def add_artist(self, name):
        """
        Inserts a new artist into the 'artists' table if it doesn't already exist.
        Returns the ID of the existing or newly inserted artist.

        :param name: The name of the artist to be added.
        :return: The ID of the newly inserted or existing artist.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT OR IGNORE INTO artists (name) VALUES (?)", (name,))
        
        if cursor.lastrowid:
            artist_id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
            artist_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()

        return artist_id

    def add_genre(self, name):
        """
        Inserts a new genre into the 'genres' table if it doesn't already exist.
        Returns the ID of the existing or newly inserted genre.

        :param name: The name of the genre to be added.
        :return: The ID of the newly inserted or existing genre.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (name,))

        if cursor.lastrowid:
            genre_id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM genres WHERE name = ?", (name,))
            genre_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()

        return genre_id

    def add_song(self, title, artist, genre, release_date, lyrics, rating):
        """
        Inserts a new song into the 'songs' table, linking it with the appropriate artist and genre.

        :param title: Title of the song.
        :param artist: Name of the artist.
        :param genre: Name of the genre.
        :param release_date: Release date of the song.
        :param lyrics: Lyrics of the song.
        :param rating: Rating of the song (numeric value between 1 and 10).
        """
        artist_id = self.add_artist(artist)
        genre_id = self.add_genre(genre)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO songs (title, artist_id, genre_id, release_date, lyrics, rating)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                          (title, artist_id, genre_id, release_date, lyrics, rating))
        connection.commit()
        cursor.close()
        connection.close()

    def get_all_songs(self):
        """
        Retrieves all songs from the 'songs' table, including associated artist and genre names.

        :return: A list of tuples, where each tuple contains the song title, artist name, genre name,
                 release date, lyrics, rating, and song id.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT songs.title, artists.name AS artist, genres.name AS genre, 
                          songs.release_date, songs.lyrics, songs.rating, songs.id 
                          FROM songs
                          JOIN artists ON songs.artist_id = artists.id
                          JOIN genres ON songs.genre_id = genres.id''')
        songs = cursor.fetchall()
        cursor.close()
        connection.close()
        return songs

    def get_song_by_id(self, song_id):
        """
        Fetches a song by its ID from the database.

        :param song_id: The ID of the song to fetch.
        :return: A tuple containing the song details (or None if not found).
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM songs WHERE id=?', (song_id,))
        song = cursor.fetchone()
        cursor.close()
        connection.close()
        return song

    def update_song(self, song_id, title, artist, genre, release_date, lyrics, rating):
        """
        Updates an existing song in the database.

        :param song_id: The ID of the song to update.
        :param title: Updated title of the song.
        :param artist: Updated artist name.
        :param genre: Updated genre name.
        :param release_date: Updated release date of the song.
        :param lyrics: Updated lyrics of the song.
        :param rating: Updated rating of the song.
        """
        artist_id = self.add_artist(artist)
        genre_id = self.add_genre(genre)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''UPDATE songs
                          SET title=?, artist_id=?, genre_id=?, release_date=?, lyrics=?, rating=?
                          WHERE id=?''',
                          (title, artist_id, genre_id, release_date, lyrics, rating, song_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_song(self, song_id):
        """
        Deletes a song by its ID from the database.

        :param song_id: The ID of the song to delete.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM songs WHERE id=?', (song_id,))
        connection.commit()
        cursor.close()
        connection.close()
