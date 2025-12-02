"""
 Authors: Abdulla Al Harun, Mostafa Maassou
 Notes:
     - The default MySQL port is 3306.
     - We use 3308 because our local MySQL instance runs inside
       Docker with a port mapping. If your MySQL runs on 3306,
       simply change "port": 3308 to 3306 below.
"""
import json
import mysql.connector

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": 3308,      # Docker mapping
    "user": "quizuser",
    "password": "quizpassword",
    "database": "quizdb",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def clear_existing_data(cursor):
    # Delete in correct order because of foreign keys
    cursor.execute("DELETE FROM options;")
    cursor.execute("DELETE FROM questions;")
    cursor.execute("DELETE FROM games;")

def import_questions_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", [])

    conn = get_connection()
    cursor = conn.cursor()

    try:
        clear_existing_data(cursor)

        for game_index, game in enumerate(games, start=1):
            game_name = f"Game {game_index}"

            cursor.execute(
                "INSERT INTO games (name) VALUES (%s);",
                (game_name,)
            )
            game_id = cursor.lastrowid

            for q in game.get("questions", []):
                cursor.execute(
                    """
                    INSERT INTO questions (game_id, question_text, correct_option_index)
                    VALUES (%s, %s, %s);
                    """,
                    (game_id, q["question"], q["correct"]),
                )
                question_id = cursor.lastrowid

                for i, text in enumerate(q["content"]):
                    cursor.execute(
                        """
                        INSERT INTO options (question_id, option_index, option_text)
                        VALUES (%s, %s, %s);
                        """,
                        (question_id, i, text),
                    )

        conn.commit()
        print("Import completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error during import:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import_questions_from_json("../question1/questions.json")
