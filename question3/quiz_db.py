import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 3308,              # Docker mapping: 3308 -> 3306
    "user": "quizuser",
    "password": "quizpassword",
    "database": "quizdb",
}


def get_connection():
    """Create and return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def _rows_to_question_dicts(rows):
    """
    Convert joined rows (question + options) into the SAME structure
    as the original JSON file:

    {
        "question": "...",
        "content": ["A", "B", "C", "D"],
        "correct": 0
    }

    rows: list of tuples
      (question_id, question_text, correct_option_index, option_index, option_text)
    """
    questions_by_id = {}

    for q_id, q_text, correct_idx, opt_idx, opt_text in rows:
        if q_id not in questions_by_id:
            questions_by_id[q_id] = {
                "question": q_text,
                "content": [],
                "correct": correct_idx,
            }

        options_list = questions_by_id[q_id]["content"]

        # ensure list is long enough
        if len(options_list) <= opt_idx:
            options_list.extend([""] * (opt_idx + 1 - len(options_list)))

        options_list[opt_idx] = opt_text

    return list(questions_by_id.values())


def get_questions_for_game(game_id: int):
    """
    Return all questions for a single game as a list of dicts
    in the same structure as the JSON.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT
                q.id,
                q.question_text,
                q.correct_option_index,
                o.option_index,
                o.option_text
            FROM questions q
            JOIN options o ON q.id = o.question_id
            WHERE q.game_id = %s
            ORDER BY q.id, o.option_index;
        """
        cursor.execute(query, (game_id,))
        rows = cursor.fetchall()
        return _rows_to_question_dicts(rows)
    finally:
        cursor.close()
        conn.close()


def get_all_questions():
    """Return questions from all games (mixed)."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT
                q.id,
                q.question_text,
                q.correct_option_index,
                o.option_index,
                o.option_text
            FROM questions q
            JOIN options o ON q.id = o.question_id
            ORDER BY q.id, o.option_index;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return _rows_to_question_dicts(rows)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # quick test
    qs_game1 = get_questions_for_game(1)
    print("Game 1 questions:", len(qs_game1))
    print("First question:", qs_game1[0])
