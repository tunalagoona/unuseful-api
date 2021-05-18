import time
import logging
from contextlib import closing
from typing import Optional, List

from requests import get, codes, Session
import json
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from database import DB
from entities import UselessFact


logging.basicConfig(
    filename="log.log",
    format="%(levelname)s %(asctime)s: %(message)s",
    level=logging.INFO,
    filemode="w+"
)
logger = logging.getLogger()

write_in_process = True


class FactsProcessor:
    @staticmethod
    def get_random_facts(url: str) -> Optional[UselessFact]:
        s = Session()
        s.mount(url, HTTPAdapter(max_retries=5))

        response = s.get(url, timeout=5)

        if response.status_code == codes.ok:
            obj = UselessFact(**json.loads(response.text))
            logger.info(f"Received the fact with the id: {obj.id}.")
            return obj
        else:
            logger.info(f"Could not connect to Random Useless Facts. Status code is {response.status_code}.")
            return None

    def save_random_facts(self, url):
        with closing(DB()) as db:
            with db:
                db.init_db()
                db.delete_all_entries()

        counter = 0
        records = []

        facts_quantity, batch_size, sleep_time = 1000, 5, 1

        pbar = tqdm(total=facts_quantity)
        pbar.set_description("Downloading random facts")

        while counter < facts_quantity:
            while counter < 1000 and len(records) < batch_size:
                fact = self.get_random_facts(url)
                if fact:
                    records.append(fact)
                    time.sleep(sleep_time)
                    counter += 1
                    pbar.update(1)

            with closing(DB()) as db:
                with db:
                    db.insert(records)

            records.clear()

        logger.info("Finished insertion to the DB.")
        pbar.close()

        with closing(DB()) as db:
            with db:
                db.update_flag_to_finished()


if __name__ == "__main__":
    FactsProcessor().save_random_facts('https://uselessfacts.jsph.pl/random.json?language=en')
