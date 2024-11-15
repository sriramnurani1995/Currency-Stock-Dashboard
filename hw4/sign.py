from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Sign(MethodView):
    def get(self):
        """
        Displays the form for adding a new song.
        """
        return render_template('sign.html')

    def post(self):
        """
        Processes the form for adding a new song.
        Accepts POST requests and inserts the song into the database.
        Redirects to the index when completed.
        """
        model = gbmodel.get_model()
        
        # Extract song details from the form
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        release_date = request.form['release_date']
        lyrics = request.form['lyrics']
        rating = float(request.form['rating'])  
        
        # Add the song to the database
        model.add_song(title, artist, genre, release_date, lyrics, rating)
        
        # Redirect to the index page after the song is added
        return redirect(url_for('index'))
