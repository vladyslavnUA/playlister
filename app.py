from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.Playlister
playlists = db.playlists



app = Flask(__name__)



#our mock array of projects
#playlists = [
#    { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#    { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
#]


@app.route('/')
def playlists_index():
    return render_template('playlists_index.html', playlists = playlists.find())


@app.route('/playlists/new')
def playlists_new():
    """create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))    



@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
