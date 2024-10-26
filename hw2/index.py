from flask import render_template
from flask.views import MethodView

class Index(MethodView):
    def get(self):
        """
        Renders the landing page with links to other parts of the app.
        """
        return render_template('index.html')  # Render the landing page template
