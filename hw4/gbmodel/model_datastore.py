from google.cloud import datastore

class model:
    def __init__(self):
        # Initialize the Datastore client
        self.client = datastore.Client()

    def add_artist(self, name):
        # Insert a new artist entity in Datastore if it doesn't exist
        key = self.client.key('Artist', name)  # Use name as the unique ID
        artist = datastore.Entity(key=key)
        artist['name'] = name
        self.client.put(artist)
        return artist.key.id_or_name  # Return the ID or name as identifier

    def add_genre(self, name):
        # Insert a new genre entity in Datastore if it doesn't exist
        key = self.client.key('Genre', name)  # Use name as the unique ID
        genre = datastore.Entity(key=key)
        genre['name'] = name
        self.client.put(genre)
        return genre.key.id_or_name  # Return the ID or name as identifier

    def add_song(self, title, artist, genre, release_date, lyrics, rating):
        # Link artist and genre, then insert a new song entity
        artist_id = self.add_artist(artist)
        genre_id = self.add_genre(genre)
        key = self.client.key('Song')
        song = datastore.Entity(key=key)
        song.update({
            'title': title,
            'artist_id': artist_id,
            'genre_id': genre_id,
            'release_date': release_date,
            'lyrics': lyrics,
            'rating': rating
        })
        self.client.put(song)

    def get_all_songs(self):
        # Query all songs
        query = self.client.query(kind='Song')
        songs = list(query.fetch())

        # For each song, fetch the artist and genre names based on stored IDs
        for song in songs:
            # Retrieve artist information
            if 'artist_id' in song:
                artist_key = self.client.key('Artist', song['artist_id'])
                artist = self.client.get(artist_key)
                song['artist_name'] = artist['name'] if artist else None
            else:
                song['artist_name'] = None

            # Retrieve genre information
            if 'genre_id' in song:
                genre_key = self.client.key('Genre', song['genre_id'])
                genre = self.client.get(genre_key)
                song['genre_name'] = genre['name'] if genre else None
            else:
                song['genre_name'] = None

        # Format each song in a dictionary with all details for easier display
        formatted_songs = [
            {
                'title': song.get('title'),
                'artist': song.get('artist_name'),
                'genre': song.get('genre_name'),
                'release_date': song.get('release_date'),
                'lyrics': song.get('lyrics'),
                'rating': song.get('rating'),
                'id': song.key.id_or_name
            }
            for song in songs
        ]
        return formatted_songs

    def get_song_by_id(self, song_id):
        # Retrieve a song by its ID
        key = self.client.key('Song', song_id)
        song = self.client.get(key)
        
        if song:
            # Retrieve artist name
            if 'artist_id' in song:
                artist_key = self.client.key('Artist', song['artist_id'])
                artist = self.client.get(artist_key)
                song['artist_name'] = artist['name'] if artist else None
            else:
                song['artist_name'] = None

            # Retrieve genre name
            if 'genre_id' in song:
                genre_key = self.client.key('Genre', song['genre_id'])
                genre = self.client.get(genre_key)
                song['genre_name'] = genre['name'] if genre else None
            else:
                song['genre_name'] = None

        return song

    def update_song(self, song_id, title, artist, genre, release_date, lyrics, rating):
        # Update an existing song entity in Datastore
        key = self.client.key('Song', song_id)
        song = self.client.get(key)
        if song:
            artist_id = self.add_artist(artist)
            genre_id = self.add_genre(genre)
            song.update({
                'title': title,
                'artist_id': artist_id,
                'genre_id': genre_id,
                'release_date': release_date,
                'lyrics': lyrics,
                'rating': rating
            })
            self.client.put(song)

    def delete_song(self, song_id):
        # Delete a song entity by its ID
        key = self.client.key('Song', song_id)
        self.client.delete(key)
