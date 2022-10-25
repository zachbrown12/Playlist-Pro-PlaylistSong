from crypt import methods
from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from service_factory import ServiceFactory
# from playlists_resource import PlaylistResource
# from playlist_song_resource import PlaylistSongResource
from flask_cors import CORS
from dotenv import load_dotenv

# load environment variables fron .env
load_dotenv()

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

service_factory = ServiceFactory()


@app.route("/api/health", methods=["GET"])
def get_health():
    msg = {
        "name": "PlaylistSong Microservice",
        "health": "Good",
        "at time": str(datetime.now())
    }
    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

# /songs
# /playlists
@app.route('/api/<resource_collection>', methods=['GET','POST'])
def do_resource_collection(resource_collection):
    request_inputs = rest_utils.RESTContext(request, resource_collection)
    svc = service_factory.get(resource_collection, None)

    if request_inputs.method == "GET":
        res = svc.get_by_template(template=request_inputs.args,
                                  field_list=request_inputs.fields)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "POST":
        res = svc.create_resource(resource_data=request_inputs.data)
        rsp = Response(res['text'], status=res['status'], content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp

# playlists get info, update, delete
@app.route("/api/playlists/<id>", methods=["GET", "PUT", "DELETE"])
def getPlaylist(id):
    request_inputs = rest_utils.RESTContext(request, id)
    svc = service_factory.get("playlists", None)

    if request_inputs.method == "GET":
        res = svc.get_resource_by_id(id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "PUT":
        res = svc.update_resource(id, resource_data=request_inputs.data)
        rsp = Response(res['text'], status=res['status'], content_type="text/plain")
    elif request_inputs.method == "DELETE":
        res = svc.delete_resource(id)
        rsp = Response(res['text'], status=res['status'], content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp

# add songs to playlist
@app.route("/api/playlists/<id>/song", methods=["POST", "DELETE"])
def addPlaylistSong(id):
    request_inputs = rest_utils.RESTContext(request, id)
    svc = service_factory.get("playlistsongs", None)
    request_inputs.data['playlistId'] = id

    if request_inputs.method == "POST":
        res = svc.create_resource(resource_data=request_inputs.data)
        rsp = Response(res['text'], status=res['status'], content_type="text/plain")
    elif request_inputs.method == "DELETE":
        res = svc.delete_resource(resource_data=request_inputs.data)
        rsp = Response(res['text'], status=res['status'], content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

