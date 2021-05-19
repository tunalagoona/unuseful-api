import json
import os
from contextlib import closing
import logging

from flask import Flask, request, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from googletrans import Translator

from database import DB


auth = HTTPBasicAuth()

app = Flask(__name__)
app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'RandomFacts.db'),)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

logger = logging.getLogger()


@app.route("/status", methods=['GET'])
@auth.login_required
def status() -> str:
    return json.dumps(get_status())


@app.route("/facts", methods=['GET'])
@auth.login_required
def facts() -> str:
    with closing(DB()) as db:
        with db:
            fact_ids = json.dumps(db.get_ids())
    return fact_ids


@app.route("/facts/<fact_id>", methods=['GET'])
@auth.login_required
def fact(fact_id) -> str:
    if fact_id:
        with closing(DB()) as db:
            with db:
                fact_obj: dict = db.get_fact_by_id(fact_id)
        obj = {
            "id": fact_obj["id"],
            "text": fact_obj["text"],
            "url": fact_obj["source_url"],
            "language": fact_obj["language"]
        }

        language = request.args.get('lang')

        if language:
            obj["language"] = language

            translator = Translator()
            t = translator.translate(obj["text"], dest=language, src='en')
            obj["text"] = t.text
        return str(obj)
    else:
        return ""


def get_status() -> dict:
    with closing(DB()) as db:
        with db:
            rows_quantity_unique = db.count_unique_rows()
            status, rows_quantity = db.check_status()

    st = {"status": status, "facts": {}}
    st["facts"]["total"] = rows_quantity
    st["facts"]["unique"] = rows_quantity_unique
    return st


@auth.verify_password
def verify_password(username, password) -> bool:
    # Using hardcoded user/pass because of time limitations
    check_user = 'admin'
    check_password = 'QWxhZGRpb'
    if username != check_user or password != check_password:
        return False
    g.user = check_user
    return True
