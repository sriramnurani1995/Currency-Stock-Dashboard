class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        
        # Fetch songs from the database
        entries = [dict(title=row[0], artist=row[1], genre=row[2], release_date=row[3], lyrics=row[4], rating=row[5]) 
                   for row in model.get_all_songs()]
        
        # Render the songs in the index template
        return render_template('index.html', entries=entries)