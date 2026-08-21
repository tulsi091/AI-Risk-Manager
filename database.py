import sqlite3


DB_NAME = "risk_reports.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company TEXT,

        industry TEXT,

        score INTEGER,

        level TEXT,

        analysis TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_report(company, industry, score, level, analysis):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO reports(

    company,
    industry,
    score,
    level,
    analysis

    )

    VALUES(?,?,?,?,?)

    """,

    (

    company,
    industry,
    score,
    level,
    analysis

    )

    )

    conn.commit()
    conn.close()


def get_reports():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    company,
    industry,
    score,
    level,
    created_at

    FROM reports

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_report(company):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM reports WHERE company=?",

        (company,)

    )

    conn.commit()

    conn.close()
def get_risk_trend():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    company,
    score

    FROM reports

    ORDER BY id

    """)

    data = cursor.fetchall()

    conn.close()

    return data