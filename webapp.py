import json
import os
from contextlib import closing
from typing import List

from flask import Flask
import logging

from database import DB

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'RandomFacts.db'),
)
logger = logging.getLogger()


@app.route("/status", methods=['GET'])
def status() -> str:
    return str(get_status())


@app.route("/facts", methods=['GET'])
def facts() -> str:
    with closing(DB()) as db:
        with db:
            fact_ids: List[str] = db.get_ids()
    return f"All the facts received: \n {fact_ids}"


@app.route("/facts/<fact_id>", methods=['GET'])
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
        result = json.dumps(obj)
        return result
    else:
        return ""


def get_status() -> dict:
    with closing(DB()) as db:
        with db:
            rows_quantity = db.count_all_rows()
            rows_quantity_unique = db.count_unique_rows()
            status = db.check_status()

    st = {"status": status, "facts": {}}
    st["facts"]["total"] = rows_quantity
    st["facts"]["unique"] = rows_quantity_unique
    return st
