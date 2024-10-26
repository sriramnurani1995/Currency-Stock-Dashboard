from flask import Flask, redirect, request, url_for, render_template
from index import Index
from sign import Sign
from view import ViewSongs
from update import Update  # Import the update route
from delete import DeleteSong  # Import the delete route
from update import Update




app = Flask(__name__)

# Route for the landing page
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

# Route for viewing all songs
app.add_url_rule('/view',
                 view_func=ViewSongs.as_view('view_songs'),
                 methods=["GET"])

# Route for adding a new song
app.add_url_rule('/sign',
                 view_func=Sign.as_view('sign'),
                 methods=['GET', 'POST'])

# Register the update view with a URL rule
app.add_url_rule('/update/<int:song_id>', view_func=Update.as_view('update'), methods=['GET', 'POST'])


# Route for deleting a song
app.add_url_rule('/delete/<int:song_id>',
                 view_func=DeleteSong.as_view('delete_song'),
                 methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
