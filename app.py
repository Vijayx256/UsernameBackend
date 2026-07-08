import os
import base64
from flask import Flask, Response
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ["MONGO_URI"])

db = client["newclonemanagerfilestore"]
uname = db["uname"]


def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

@app.route("/")
def home():
    return "Backend API is running."


@app.route("/getbot/<short_link>")
def get_bot(short_link):
    try:
        decoded = decode(short_link)

        try:
            user_id = int(decoded.split("_")[0])
        except:
            user_id = int(decoded.split("_")[1])

        find = uname.find_one({"user_id": user_id})

        if not find:
            return Response("Nothing", mimetype="text/plain")

        username = find["chat_id"]

        if not username:
            return Response("Nothing", mimetype="text/plain")

        return Response(username.replace("@", ""), mimetype="text/plain")

    except Exception:
        return Response("Nothing", mimetype="text/plain")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
