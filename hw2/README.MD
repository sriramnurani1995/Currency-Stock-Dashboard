# **Song Database Web Application**

This is a simple web application built using Python and Flask, with an SQLite3 database. It allows users to add, view, update, and delete songs, along with managing related artists and genres.

## **Features**

- Add new songs with details such as title, artist, genre, release date, lyrics, and rating.
- View all songs in a table format.
- Edit and delete existing songs.
- Automatically manage artists and genres (add only when needed).
---
## **Technology Stack**

- **Backend**: Python, Flask
- **Database**: SQLite3
- **Frontend**: HTML, CSS
---
## **Project Structure**

```bash
project_folder/
├── static/
│   └── style.css                # Custom CSS for the front-end styling
├── templates/
│   ├── layout.html              # Main layout template for the app
│   ├── index.html               # Homepage
│   ├── sign.html                # Form for adding new songs
│   ├── update.html              # Form for updating songs
│   ├── view.html              # Form for Viewing songs   
├── app.py                       # Main Flask app routing
├── gbmodel/
│   ├── __init__.py              # Model initialization for database backends
│   ├── model_sqlite3.py         # SQLite3 model handling CRUD operations
├── entries.db                   # SQLite database file storing song data
├── README.md                    # This documentation file
```
---
## **Installation and Setup**

### 1. Clone the Repository
```bash
git clone git@gitlab.com:srirams3/cloud-nurani-srirams.git
cd hw2
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can run the application in two ways:
#### Using Flask directly:
```bash
flask run
```
#### Using Python to run the app.py file:
```bash
flask run
```
The app will run at **http://127.0.0.1:5000**.


---

## **Database Structure**:

The SQLite database (`entries.db`) consists of the following three tables:

1. **artists**
   - `id`: Integer (Primary Key, Auto-increment)
   - `name`: Text (Unique)

2. **genres**
   - `id`: Integer (Primary Key, Auto-increment)
   - `name`: Text (Unique)

3. **songs**
   - `id`: Integer (Primary Key, Auto-increment)
   - `title`: Text
   - `artist_id`: Integer (Foreign Key to `artists.id`)
   - `genre_id`: Integer (Foreign Key to `genres.id`)
   - `release_date`: Text (Format: YYYY-MM-DD)
   - `lyrics`: Text
   - `rating`: Real (Numeric value for the song's rating)

---

## **Routes**:

- `/`: Landing Page.
- `/sign`: Add a new song.
- `/view` View the List of Songs
- `/update/<song_id>`: Edit a song.
- `/delete/<song_id>`: Delete a song.



