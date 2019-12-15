import sqlite3
import pandas as pd
import logging

from tqdm import tqdm
from pathlib import Path
from sqlite3 import Error
from typing import Optional


def create_connection(db_file: Path) -> Optional[sqlite3.Connection]:
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file.as_posix())
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None


def check_if_file(path: Path) -> Path:
    if path.is_file():
        return path
    else:
        raise Exception("Sorry, this is not a file path")


def prepare_twitter_data(path: Path, connection: sqlite3.Connection):

    df = pd.read_csv(path, index_col=None, encoding="utf8")
    cursor = connection.cursor()

    for _, row in tqdm(df.iterrows()):
        try:

            week_day, month, day, time, _, year = row["date"].split(" ")
            cursor.execute(
                """INSERT INTO tweets VALUES (
                :id, :user, :time, :week_day, :day, :month, :year, :target, :tweet
                )""",
                {
                    "id": row["id"],
                    "user": row["user"],
                    "time": time,
                    "week_day": week_day,
                    "day": int(day),
                    "month": month,
                    "year": int(year),
                    "target": row["target"],
                    "tweet": row["text"],
                },
            )

            connection.commit()

        except KeyError:
            logging.warning(
                "Some fields are missing. This record was removed from dataset"
            )


def main():

    db_path = Path("/Users/mark/Documents/SQLite/1600k_tweets_database.db")
    tweets_path = check_if_file(
        Path(
            "/Users/mark/Documents/Datasets/Prepared_for_upload/Tweets_emotional_detection.csv"
        )
    )

    connection = create_connection(db_path)
    if connection is not None:

        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE tweets (
                id integer, user text, time text,
                week_day text, day integer, month text,
                year integer, target integer, tweet text
            )"""
        )
        connection.commit()

        prepare_twitter_data(tweets_path, connection)

        connection.close


if __name__ == "__main__":
    main()
