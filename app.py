from flask import Flask
from flask import jsonify
from flask import request
from scrapping_segs.get_segment import get_segments_data

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, it really really works!"


@app.route("/api/", methods=['POST'])
def segments():
    if not request.json or not ("segment_ids" in request.json) or not request.json["segment_ids"]:
        return jsonify({"error": "Bad request"})

    segment_ids = str(request.json["segment_ids"])
    segment_ids = [int(i) for i in segment_ids.strip('[]').split(', ')]
    return jsonify(get_segments_data(segment_ids))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
