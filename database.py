import os
import sqlite3
import config

def connect_to_db() -> config.Connection:
    os.makedirs(config.RESULT_DATABASE.split('/')[0], exist_ok=True)

    db = sqlite3.connect(config.RESULT_DATABASE)
    return config.Connection(db=db, cursor=db.cursor())


def create_table(table_name: str = "similar_skills") -> None:
    db, cursor = connect_to_db()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                    db_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill VARCHAR(255),
                    similar_skill VARCHAR(255),
                    similar_skill_id INTEGER,
                    similarity_percent INTEGER
    )""")
    db.commit()
    db.close()


def add_similar_skill_to_table(data: config.SimilarSkill, table_name: str = "similar_skills") -> None:
    db, cursor = connect_to_db()
    cursor.execute(f"""INSERT INTO {table_name}(skill, similar_skill, similar_skill_id, similarity_percent) VALUES(?, ?, ?, ?)""", 
    (data.name, data.similar_skill, data.similar_skills_id, data.percent))
    
    db.commit()
    db.close()