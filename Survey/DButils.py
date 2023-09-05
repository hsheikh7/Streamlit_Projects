import sqlite3
import pandas as pd 

DATABASE_NAME = "survey.db"

def create_tables():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY,
            question_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS choice (
            id INTEGER PRIMARY KEY,
            choice_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questionnaire (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            choice_id INTEGER,
            FOREIGN KEY (question_id) REFERENCES question(id),
            FOREIGN KEY (choice_id) REFERENCES choice(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS response (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            choice_id INTEGER,
            FOREIGN KEY (question_id) REFERENCES question(id),
            FOREIGN KEY (choice_id) REFERENCES choice(id)
        )
    ''')
    connection.commit()
    connection.close()

def get_survey():
    connection = sqlite3.connect(DATABASE_NAME)
    
    query = '''
        SELECT q.question_text as question, GROUP_CONCAT(c.choice_text, ', ') as choices
        FROM questionnaire n
        JOIN question q ON n.question_id = q.id
        JOIN choice c ON n.choice_id = c.id
        GROUP BY q.id
    '''
    df = pd.read_sql_query(query, connection)
    
    connection.close()
    return df

def save_question(q_text, q_choices):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO question (question_text) VALUES (?)', (q_text,))
    question_id = cursor.lastrowid

    choices = q_choices.split(',')
    for choice_text in choices:
        choice_text = choice_text.strip()
        cursor.execute('SELECT id FROM choice WHERE choice_text = ?', (choice_text,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute('INSERT INTO choice (choice_text) VALUES (?)', (choice_text,))
            choice_id = cursor.lastrowid
        else:
            choice_id = row[0]
        
        cursor.execute('INSERT INTO questionnaire (question_id, choice_id) VALUES (?, ?)', (question_id, choice_id))

    connection.commit()
    connection.close()

def get_choice_id(choice_text):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM choice WHERE choice_text = ?', (choice_text,))
    row = cursor.fetchone()
    connection.close()
    return row[0] if row else None

def save_results(responses):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    for question_id, choice_id in responses:
        cursor.execute('INSERT INTO response (question_id, choice_id) VALUES (?, ?)', (question_id, choice_id))

    connection.commit()
    connection.close()

def get_results():
    connection = sqlite3.connect(DATABASE_NAME)
    
    query = '''
        SELECT q.id, q.question_text, c.choice_text, COUNT(r.choice_id) as count
        FROM questionnaire n
        JOIN question q ON n.question_id = q.id
        JOIN choice c ON n.choice_id = c.id
        LEFT JOIN response r ON r.question_id = q.id AND r.choice_id = c.id
        GROUP BY q.id, c.id
    '''
    df = pd.read_sql_query(query, connection)
    
    connection.close()
    return df

        
def remove_question(question_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Delete the question from the question table
    cursor.execute('DELETE FROM question WHERE id = ?', (question_id,))

    # Delete the question's choices from the questionnaire table
    cursor.execute('DELETE FROM questionnaire WHERE question_id = ?', (question_id,))

    # Delete the question's responses from the response table
    cursor.execute('DELETE FROM response WHERE question_id = ?', (question_id,))

    connection.commit()
    connection.close()