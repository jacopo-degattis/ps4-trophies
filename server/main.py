import sys
from pathlib import Path
from flask import Flask, request, Response, send_from_directory

parent_dir = Path(__file__).resolve().parent.parent

sys.path.append(str(parent_dir))

from lib.ftp import PsFTP
from lib.trophy import Trophy

# pf = PsFTP()
app = Flask("ps4-trophies-server")


@app.route("/")
def serve_frontend():
    # This function must serve static files of frontend build (svelte-ui or svelte-kit)
    pass


# Get trophies list as XML from a given np_comm_id
@app.route("/api/pull-trophies", methods=["POST"])
def pull_trophy():
    data = request.json
    np_comm_id = data.get("np_comm_id")

    if not np_comm_id:
        return Response("You must provide a np_comm_id value", 400)

    # TODO: Check that is a valid NP_COMM_ID

    def handle_update(curr_len, total_len):
        pass

    try:
        # TODO: maybe use 'in-memory' instead of stepping through a tmp local file
        # pf.get_trophy_for_comm_id(np_comm_id, handle_update)

        # WITH CONSOLE ON
        # tmp_file = open(f"{np_comm_id}.TRP", "rb").read()

        # WITH CONSOLE OFF (DEBUG AND DEV PURPOSES)
        tmp_file = open("test.TRP", "rb").read()

        # This must stay
        t = Trophy(np_comm_id=np_comm_id, from_bytes=tmp_file)
        t.extract_files(custom_path="./static")
        xml_data = t.decrypt_esfm_file(f"./static/{np_comm_id}/TROP.ESFM")

        return Response(xml_data, 200)
    except Exception as e:
        print(e)
        return Response(status=500)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

# from lib.trophy import Trophy

# if __name__ == "__main__":
#     t = Trophy("./TROPHY.TRP", "NPWR32931_00")

#     print(t.header.version)
#     print(t.entries[0].name)

#     t.extract_files()
#     t.decrypt_esfm_file("./NPWR32931_00/TROP.ESFM")
