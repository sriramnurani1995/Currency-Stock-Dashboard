from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import gbmodel

class Update(MethodView):
    def get(self, song_id):
        """
        GET request for rendering the update form.
        The form will be pre-filled with the song's current information.

        :param song_id: The ID of the song to be updated.
        :return: Rendered template with pre-filled data of the song to update.
        """
        model = gbmodel.get_model()
        song = model.get_song_by_id(song_id)
        return render_template('update.html', song=song)

    def post(self, song_id):
        """
        POST request for handling the update of an existing song.
        The updated data is received from the form and applied to the song.

        :param song_id: The ID of the song to be updated.
        :return: Redirects back to the song list after successful update.
        """
        model = gbmodel.get_model()
        
        # Retrieve updated form data
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        release_date = request.form['release_date']
        lyrics = request.form['lyrics']
        rating = request.form['rating']
        
        # Perform the update in the database
        model.update_song(song_id, title, artist, genre, release_date, lyrics, rating)
        
        # Redirect back to the list of songs after updating
        return redirect(url_for('view_songs'))
