from flask import redirect, url_for, request
from flask.views import MethodView
import gbmodel

class DeleteSong(MethodView):
    def post(self, song_id):
        """
        Deletes the specified song from the database.
        """
        model = gbmodel.get_model()
        model.delete_song(song_id)  # Delete the song
        return redirect(url_for('view_songs'))  # Redirect back to the view page
