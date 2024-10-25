from datetime import date
import sqlite3

DB_FILE = 'entries.db'  # File for storing the SQLite database

def get_db_connection():
    """
    Creates a new SQLite database connection for each request.
    Ensures the connection is not shared across threads.
    """
    return sqlite3.connect(DB_FILE)

class model:
    def __init__(self):
        """
        Initializes the database connection and ensures the required tables
        (artists, genres, songs) are created if they do not already exist.
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
        """
        connection = get_db_connection()  # Get a new connection for this operation
        cursor = connection.cursor()

        # Attempt to insert the artist
        cursor.execute("INSERT OR IGNORE INTO artists (name) VALUES (?)", (name,))
        
        # Now, check if a new row was inserted
        if cursor.lastrowid:  # If a new row was inserted, lastrowid will be non-zero
            artist_id = cursor.lastrowid
        else:  # If no new row was inserted (insert ignored), fetch the existing artist's ID
            cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
            artist_id = cursor.fetchone()[0]  # Fetch the ID of the existing artist

        connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

        return artist_id

    def add_genre(self, name):
        """
        Inserts a new genre into the 'genres' table if it doesn't already exist.
        Returns the ID of the existing or newly inserted genre.
        """
        connection = get_db_connection()  # Get a new connection for this operation
        cursor = connection.cursor()

        # Attempt to insert the genre
        cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (name,))

        # Check if a new row was inserted
        if cursor.lastrowid:  # New row inserted, get the ID
            genre_id = cursor.lastrowid
        else:  # Existing genre, fetch its ID
            cursor.execute("SELECT id FROM genres WHERE name = ?", (name,))
            genre_id = cursor.fetchone()[0]

        connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

        return genre_id

    def add_song(self, title, artist, genre, release_date, lyrics, rating):
        """
        Inserts a new song into the 'songs' table, linking it with the appropriate artist and genre.

        :param title: Title of the song.
        :param artist: Name of the artist.
        :param genre: Name of the genre.
        :param release_date: Release date of the song.
        :param lyrics: Lyrics of the song.
        :param rating: Rating of the song (can be a float or integer).
        """
        artist_id = self.add_artist(artist)  # Ensure the artist exists
        genre_id = self.add_genre(genre)     # Ensure the genre exists

        connection = get_db_connection()  # Get a new connection for this operation
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
                 release date, lyrics, and rating.
        """
        connection = get_db_connection()  # Get a new connection for this operation
        cursor = connection.cursor()
        cursor.execute('''SELECT songs.title, artists.name AS artist, genres.name AS genre, 
                          songs.release_date, songs.lyrics, songs.rating 
                          FROM songs
                          JOIN artists ON songs.artist_id = artists.id
                          JOIN genres ON songs.genre_id = genres.id''')
        songs = cursor.fetchall()
        cursor.close()
        connection.close()
        return songs

    def close(self):
        """
        Closes the database connection.
        In this version, each operation gets its own connection, so no persistent connection to close.
        """
        pass  # No need to explicitly close in this case since each method handles connection close
