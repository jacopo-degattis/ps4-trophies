import sys
from pathlib import Path
from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import cross_origin

parent_dir = Path(__file__).resolve().parent.parent

sys.path.append(str(parent_dir))

from lib.ftp import PsFTP
from lib.trophy import Trophy

pf = PsFTP()
app = Flask("ps4-trophies-server")


@app.route("/")
def serve_frontend():
    # This function must serve static files of frontend build (svelte-ui or svelte-kit)
    pass


# Get trophies list as XML from a given np_comm_id
@app.route("/api/pull-trophies", methods=["POST"])
@cross_origin()
def pull_trophy():
    data = request.json
    np_comm_id = data.get("np_comm_id")

    if not np_comm_id:
        return Response("You must provide a np_comm_id value", 400)

    # TODO: Check that is a valid NP_COMM_ID

    def handle_update(curr_len, total_len):
        pass

    try:
        file_buffer = pf.get_trophy_for_comm_id(np_comm_id, handle_update)

        t = Trophy(np_comm_id=np_comm_id, from_bytes=file_buffer)
        t.extract_files(custom_path="./static")
        response = t.trophies_as_json(f"./static/{np_comm_id}/TROP.ESFM")

        return jsonify(response)
    except Exception as e:
        print(e)
        return Response(status=500)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
