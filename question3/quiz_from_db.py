import random
from question3.quiz_db import get_questions_for_game, get_all_questions

# Letters used for answer options
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_OF_GAMES = 5  # we know there are 5 games in the DB


def choose_mode():
    """
    Shows the menu and returns a list of questions fetched from the database.
    Options:
      1-5: single game
      6  : all games mixed
      7  : random 15 from all games
    """
    while True:
        # Fetch questions for each game so we can show counts
        game_questions = []
        for game_id in range(1, NUMBER_OF_GAMES + 1):
            qs = get_questions_for_game(game_id)
            game_questions.append(qs)

        total_all = sum(len(qs) for qs in game_questions)

        print("\n=== Main Menu (DB version) ===")
        for i, qs in enumerate(game_questions, start=1):
            print(f"{i}. Game {i} ({len(qs)} questions)")

        print(f"{NUMBER_OF_GAMES + 1}. All games mixed ({total_all} questions)")
        print(f"{NUMBER_OF_GAMES + 2}. Random 15 from all games")

        pick = input(f"Choose 1-{NUMBER_OF_GAMES + 2}: ").strip()

        if pick.isdigit():
            pick = int(pick)

            # Single game 1-5
            if 1 <= pick <= NUMBER_OF_GAMES:
                return list(game_questions[pick - 1])  # copy

            # All games full (75)
            if pick == NUMBER_OF_GAMES + 1:
                all_q = []
                for qs in game_questions:
                    all_q.extend(qs)
                return all_q

            # Random 15 from all games
            if pick == NUMBER_OF_GAMES + 2:
                all_q = []
                for qs in game_questions:
                    all_q.extend(qs)
                if len(all_q) <= 15:
                    return all_q
                return random.sample(all_q, 15)

        print("Invalid input. Try again.")


def ask_question(q, number):
    """Asks one question and returns chosen answer index."""
    print(f"\nQ{number}: {q['question']}")

    options = q["content"]
    for i, opt in enumerate(options):
        print(f"  {LETTERS[i]}. {opt}")

    while True:
        ans = input("Your answer (A, B, C, D or Q to quit): ").strip().upper()

        if ans == "Q":
            return None

        if len(ans) == 1 and ans in LETTERS[: len(options)]:
            return LETTERS.index(ans)

        print("Please choose a valid letter.")


def run_quiz(questions):
    """Main question loop."""
    random.shuffle(questions)

    stats = {
        "total": 0,
        "correct": 0,
        "incorrect": []
    }

    for idx, q in enumerate(questions, start=1):
        user_ans = ask_question(q, idx)

        if user_ans is None:
            print("Quiz ended early by user.")
            break

        stats["total"] += 1

        if user_ans == q["correct"]:
            print("Correct!\n")
            stats["correct"] += 1
        else:
            print("Incorrect.\n")
            stats["incorrect"].append({
                "question": q,
                "your_answer": user_ans
            })

    return stats


def show_summary(stats):
    """Prints results at the end."""
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
