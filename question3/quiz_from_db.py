import random
import mysql.connector

# Database connection settings for the quiz Docker setup
DB_CONFIG = {
    "host": "localhost",
    "port": 3308,              # Docker: host 3308 -> container 3306
    "user": "quizuser",
    "password": "quizpassword",
    "database": "quizdb",
}


# ---------- Database helpers ----------

def get_connection():
    """Open a new connection to the quiz database."""
    return mysql.connector.connect(**DB_CONFIG)


def _rows_to_question_dicts(rows):
    """
    Convert rows from the JOIN query into a list of question dicts.

    Each question dict looks like:
    {
        "question": "text",
        "content": ["opt A", "opt B", ...],
        "correct": index_of_correct_option
    }
    """
    questions_by_id = {}

    for q_id, q_text, correct_idx, opt_idx, opt_text in rows:
        if q_id not in questions_by_id:
            questions_by_id[q_id] = {
                "question": q_text,
                "content": [],
                "correct": correct_idx,
            }

        options = questions_by_id[q_id]["content"]

        # Make sure the list is long enough for this option index
        if len(options) <= opt_idx:
            options.extend([""] * (opt_idx + 1 - len(options)))

        options[opt_idx] = opt_text

    return list(questions_by_id.values())


def get_questions_for_game(game_id: int):
    """Return all questions for one game as a list of dicts."""
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
    """Return questions from all games."""
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


# ---------- Quiz logic ----------

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_OF_GAMES = 5  # We know we have 5 games in the DB


def choose_mode():
    """
    Show the main menu and return the list of questions
    based on the user's choice.
    """
    while True:
        # Fetch questions for each game so we can show counts
        game_questions = []
        for game_id in range(1, NUMBER_OF_GAMES + 1):
            game_questions.append(get_questions_for_game(game_id))

        total_all = sum(len(qs) for qs in game_questions)

        print("\n=== Main Menu (DB version) ===")
        for i, qs in enumerate(game_questions, start=1):
            print(f"{i}. Game {i} ({len(qs)} questions)")
        print(f"{NUMBER_OF_GAMES + 1}. All games mixed ({total_all} questions)")
        print(f"{NUMBER_OF_GAMES + 2}. Random 15 from all games")

        pick = input(f"Choose 1-{NUMBER_OF_GAMES + 2}: ").strip()

        if pick.isdigit():
            pick = int(pick)

            # Single game
            if 1 <= pick <= NUMBER_OF_GAMES:
                return list(game_questions[pick - 1])

            # All questions from all games
            if pick == NUMBER_OF_GAMES + 1:
                all_q = []
                for qs in game_questions:
                    all_q.extend(qs)
                return all_q

            # Random 15 questions from all games
            if pick == NUMBER_OF_GAMES + 2:
                all_q = []
                for qs in game_questions:
                    all_q.extend(qs)
                if len(all_q) <= 15:
                    return all_q
                return random.sample(all_q, 15)

        print("Invalid input. Try again.")


def ask_question(q, number):
    """Ask a single question and return the chosen option index, or None if user quits."""
    print(f"\nQ{number}: {q['question']}")

    options = q["content"]
    for i, opt in enumerate(options):
        print(f"  {LETTERS[i]}. {opt}")

    while True:
        answer = input("Your answer (A, B, C, D or Q to quit): ").strip().upper()

        if answer == "Q":
            return None

        if len(answer) == 1 and answer in LETTERS[: len(options)]:
            return LETTERS.index(answer)

        print("Please choose a valid letter.")


def run_quiz(questions):
    """Run the quiz loop and return statistics."""
    random.shuffle(questions)

    stats = {
        "total": 0,
        "correct": 0,
        "incorrect": [],
    }

    for idx, q in enumerate(questions, start=1):
        user_answer = ask_question(q, idx)

        if user_answer is None:
            print("Quiz ended by user.")
            break

        stats["total"] += 1

        if user_answer == q["correct"]:
            print("Correct!\n")
            stats["correct"] += 1
        else:
            print("Incorrect.\n")
            stats["incorrect"].append(
                {
                    "question": q,
                    "your_answer": user_answer,
                }
            )

    return stats


def show_summary(stats):
    """Print a summary of the quiz results."""
    total = stats["total"]
    correct = stats["correct"]
    wrong = total - correct

    print("\n=== Quiz Summary (DB version) ===")
    print(f"Questions answered: {total}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {wrong}")

    if total > 0:
        score = round((correct / total) * 100)
        print(f"Score: {score}%")

    if stats["incorrect"]:
        print("\nReview of incorrect questions:")
        for item in stats["incorrect"]:
            q = item["question"]
            user_idx = item["your_answer"]
            correct_idx = q["correct"]

            print(f"- {q['question']}")
            print(f"  Your answer:   {q['content'][user_idx]}")
            print(f"  Correct answer:{q['content'][correct_idx]}\n")


def main():
    try:
        questions = choose_mode()
    except Exception as e:
        print("Error loading questions from database:", e)
        return

    print(f"\nStarting quiz with {len(questions)} questions (DB)...")
    stats = run_quiz(questions)
    show_summary(stats)


if __name__ == "__main__":
    main()
