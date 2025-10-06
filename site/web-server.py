from flask import Flask, send_file, Response, request
app = Flask(__name__)

@app.route("/master-birder/ontology", methods=["GET"])
def serve_ontology():
    # Always serve Turtle; most clients accept it
    return send_file("index.ttl", mimetype="text/turtle")

# Nice-to-have aliases:
@app.route("/master-birder/ontology.ttl", methods=["GET"])
def serve_ontology_ttl():
    return send_file("index.ttl", mimetype="text/turtle")

@app.route("/master-birder/ontology/", methods=["GET"])
def serve_ontology_slash():
    return send_file("index.ttl", mimetype="text/turtle")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
