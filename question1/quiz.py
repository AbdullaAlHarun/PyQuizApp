import json
import random

# Letters used for answer options
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_data(filename):
    # loads the quiz data file
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def build_question_list(data, choice):
    # picks questions based on menu choice
    games = data.get("games", [])

    if 1 <= choice <= len(games):
        # return a copy so shuffle doesn't affect original list
        return list(games[choice - 1].get("questions", []))
    else:
        # all games mixed together
        all_q = []
        for game in games:
            all_q.extend(game.get("questions", []))
        return all_q


def choose_mode(data):
    # shows the menu and asks user to pick a game
    games = data.get("games", [])

    # count how many questions there are in total
    total_all = 0
    for g in games:
        total_all += len(g.get("questions", []))

    while True:
        print("\n=== Main Menu ===")

        for i, game in enumerate(games, start=1):
            print(f"{i}. Game {i} ({len(game.get('questions', []))} questions)")

        # option 6: all questions from all games
        print(f"{len(games) + 1}. All games mixed ({total_all} questions)")
        # option 7: only 15 random questions from all games
        print(f"{len(games) + 2}. Random 15 from all games")

        pick = input(f"Choose 1-{len(games) + 2}: ").strip()

        if pick.isdigit():
            pick = int(pick)

            # single game 1-5
            if 1 <= pick <= len(games):
                return build_question_list(data, pick)

            # all games full (75)
            if pick == len(games) + 1:
                return build_question_list(data, pick)

            # random 15 from all
            if pick == len(games) + 2:
                all_q = build_question_list(data, len(games) + 1)
                if len(all_q) <= 15:
                    return all_q
                # pick 15 different random questions
                return random.sample(all_q, 15)

        print("Invalid input. Try again.")


def ask_question(q, number):
    # asks one question and returns chosen answer index
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
    # main question loop
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
    # prints results at the end
    total = stats["total"]
    correct = stats["correct"]
    wrong = total - correct

    print("\n=== Quiz Summary ===")
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
    filename = "questions.json"

    try:
        data = load_data(filename)
    except Exception as e:
        print("Error loading file:", e)
        return

    questions = choose_mode(data)
    print(f"\nStarting quiz with {len(questions)} questions...")
    stats = run_quiz(questions)
    show_summary(stats)


if __name__ == "__main__":
    main()
