import json
import sqlite3
import logging
from typing import List

from entities import UselessFact

logger = logging.getLogger()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('RandomFacts.db')

    def delete_all_entries(self):
        curs = self.conn.cursor()
        curs.execute(
            '''
                DELETE FROM random_facts;
            '''
        )

    def init_db(self):
        curs = self.conn.cursor()
        curs.execute(
            '''
                CREATE TABLE IF NOT EXISTS random_facts (
                    id TEXT PRIMARY KEY, 
                    text TEXT,
                    source TEXT,
                    source_url TEXT,
                    language TEXT,
                    permalink TEXT
                ) WITHOUT ROWID;
            '''
        )
        curs.execute(
            '''
                CREATE TABLE IF NOT EXISTS finished_insert (
                    id INTEGER PRIMARY KEY,
                    flag TEXT
                );
            '''
        )
        curs.execute(
            '''
                INSERT INTO finished_insert (id, flag)
                VALUES (1, "FALSE")
                ON CONFLICT(id) DO UPDATE SET flag = "FALSE";
            '''
        )

    def insert(self, records: List):
        if len(records) > 0:
            columns_str: str = ", ".join(records[0]._fields)
            placeholders = ', '.join('?' * len(records[0]._fields))

            curs = self.conn.cursor()
            try:
                curs.executemany(
                    f'''
                        INSERT OR IGNORE INTO random_facts ({columns_str})  
                        VALUES ({placeholders});
                    ''', records
                )
                logger.info(f'Inserted {curs.rowcount} records to the table.')
            except sqlite3.Error as err:
                logger.error(err)
                self.update_flag_to_error()

    def count_all_rows(self) -> int:
        curs = self.conn.cursor()
        curs.execute(
            '''
                SELECT COUNT(*) FROM random_facts;
            '''
        )
        return int(curs.fetchone())

    def count_unique_rows(self) -> int:
        curs = self.conn.cursor()
        curs.execute(
            '''
                SELECT COUNT(DISTINCT id) FROM random_facts;
            '''
        )
        return int(curs.fetchone())

    def update_flag_to_finished(self):
        curs = self.conn.cursor()
        curs.execute(
            '''
                UPDATE finished_insert 
                SET flag = "TRUE"
                WHERE id = 1;
            '''
        )

    def update_flag_to_error(self):
        curs = self.conn.cursor()
        curs.execute(
            '''
                UPDATE finished_insert 
                SET flag = "ERROR"
                WHERE id = 1;
            '''
        )

    def check_status(self) -> str:
        curs = self.conn.cursor()
        curs.execute(
            '''
                SELECT flag FROM finished_insert
                WHERE id = 1;
            '''
        )
        return curs.fetchone()

    def get_ids(self) -> List[str]:
        curs = self.conn.cursor()
        curs.execute(
            '''
                SELECT id FROM random_facts;
            '''
        )
        res = curs.fetchall()
        for i in range(len(res)):
            res[i] = res[i][0]
        return res

    def get_fact_by_id(self, fact_id) -> dict:
        curs = self.conn.cursor()
        curs.execute(
            '''
                SELECT * FROM random_facts
                WHERE id = ?;
            ''', (fact_id,)
        )
        res = UselessFact(*curs.fetchone())
        return res._asdict()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self.conn.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.__exit__(exc_type, exc_val, exc_tb)
