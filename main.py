#!/usr/bin/env python3
"""A terminal-based typing speed test that measures WPM and accuracy."""

import random
import time
import sys
import os
from datetime import datetime
from pathlib import Path
import json

SCORES_FILE = Path(__file__).parent / "scores.json"

SENTENCES = {
    "easy": [
        "The quick brown fox jumps over the lazy dog.",
        "A journey of a thousand miles begins with a single step.",
        "To be or not to be, that is the question.",
        "All that glitters is not gold.",
        "The early bird catches the worm.",
        "Practice makes perfect in everything you do.",
        "Every cloud has a silver lining.",
        "Actions speak louder than words.",
        "Knowledge is power and wisdom is strength.",
        "Time flies when you are having fun.",
    ],
    "medium": [
        "The only way to do great work is to love what you do and never give up on your dreams.",
        "In the middle of difficulty lies opportunity, and every challenge is a chance to grow stronger.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "The best time to plant a tree was twenty years ago. The second best time is now.",
        "Life is what happens when you are busy making other plans for the future.",
        "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "It does not matter how slowly you go as long as you do not stop moving forward.",
        "Believe you can and you are halfway there on the road to success and achievement.",
    ],
    "hard": [
        "Docker containers provide lightweight, portable environments that encapsulate applications and their dependencies for consistent deployment across infrastructure.",
        "Kubernetes orchestrates containerized workloads by automating deployment, scaling, and management of application containers across clusters of hosts.",
        "Infrastructure as Code enables teams to provision and manage cloud resources through machine-readable configuration files rather than manual processes.",
        "Continuous integration and continuous delivery pipelines automate the building, testing, and deployment of software changes to production environments.",
        "Microservices architecture decomposes applications into loosely coupled, independently deployable services that communicate through well-defined APIs.",
        "Terraform uses declarative configuration language to define infrastructure resources across multiple cloud providers with state management and planning capabilities.",
    ],
    "code": [
        "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
        "for i in range(len(array)): if array[i] > max_val: max_val = array[i]",
        "import os; path = os.path.join(os.getcwd(), 'data', 'output.json')",
        "result = [x**2 for x in range(100) if x % 2 == 0 and x > 10]",
        "with open('config.yaml', 'r') as f: config = yaml.safe_load(f.read())",
        "async def fetch_data(url): async with aiohttp.ClientSession() as session: return await session.get(url)",
    ],
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_scores() -> list[dict]:
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []


def save_score(score: dict):
    scores = load_scores()
    scores.append(score)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


def calculate_accuracy(original: str, typed: str) -> tuple[float, list[int]]:
    errors = []
    correct = 0
    total = max(len(original), len(typed))

    for i in range(min(len(original), len(typed))):
        if original[i] == typed[i]:
            correct += 1
        else:
            errors.append(i)

    extra = abs(len(original) - len(typed))
    accuracy = (correct / total) * 100 if total > 0 else 0
    return accuracy, errors


def show_diff(original: str, typed: str, errors: list[int]):
    """Show character-by-character diff with colors."""
    print("\n  Your input vs expected:\n")

    diff_line = "  "
    for i in range(max(len(original), len(typed))):
        if i < len(typed) and i < len(original):
            if typed[i] == original[i]:
                diff_line += f"\033[92m{typed[i]}\033[0m"  # green
            else:
                diff_line += f"\033[91m{typed[i]}\033[0m"  # red
        elif i < len(typed):
            diff_line += f"\033[91m{typed[i]}\033[0m"  # extra chars in red
        else:
            diff_line += f"\033[93m_\033[0m"  # missing chars in yellow

    print(diff_line)
    print(f"  \033[90m{original}\033[0m")  # expected in gray


def run_test(difficulty: str):
    sentences = SENTENCES.get(difficulty, SENTENCES["medium"])
    text = random.choice(sentences)

    print(f"\n  {'=' * 60}")
    print(f"  Typing Speed Test [{difficulty.upper()}]")
    print(f"  {'=' * 60}")
    print(f"\n  Type the following text as fast and accurately as you can.")
    print(f"  Press Enter when done.\n")
    print(f"  \033[1;36m{text}\033[0m\n")

    input("  Press Enter to start...")
    print(f"\n  \033[1;36m{text}\033[0m\n")

    start_time = time.time()
    typed = input("  > ")
    end_time = time.time()

    elapsed = end_time - start_time
    word_count = len(text.split())
    wpm = (word_count / elapsed) * 60
    cpm = (len(text) / elapsed) * 60
    accuracy, errors = calculate_accuracy(text, typed)

    show_diff(text, typed, errors)

    print(f"\n  {'─' * 40}")
    print(f"  RESULTS")
    print(f"  {'─' * 40}")
    print(f"  Time:       {elapsed:.2f} seconds")
    print(f"  WPM:        {wpm:.1f}")
    print(f"  CPM:        {cpm:.0f}")
    print(f"  Accuracy:   {accuracy:.1f}%")
    print(f"  Errors:     {len(errors)}")
    print(f"  Words:      {word_count}")

    rating = "Excellent!" if wpm > 80 and accuracy > 95 else \
             "Great!" if wpm > 60 and accuracy > 90 else \
             "Good!" if wpm > 40 and accuracy > 85 else \
             "Keep practicing!"
    print(f"  Rating:     {rating}")

    name = input("\n  Save score? Enter name (or Enter to skip): ").strip()
    if name:
        save_score({
            "name": name,
            "wpm": round(wpm, 1),
            "cpm": round(cpm, 0),
            "accuracy": round(accuracy, 1),
            "errors": len(errors),
            "difficulty": difficulty,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        print("  Score saved!")

    return wpm, accuracy


def show_scores():
    scores = load_scores()
    if not scores:
        print("\n  No scores recorded yet.")
        return

    scores = sorted(scores, key=lambda x: x["wpm"], reverse=True)[:15]
    print(f"\n  {'=' * 65}")
    print(f"  {'HIGH SCORES':^65}")
    print(f"  {'=' * 65}")
    print(f"  {'#':>3}  {'Name':<12} {'WPM':>6} {'Accuracy':>9} {'Errors':>7} {'Difficulty':<10} {'Date'}")
    print(f"  {'-' * 65}")
    for i, s in enumerate(scores, 1):
        print(f"  {i:>3}  {s['name']:<12} {s['wpm']:>6.1f} {s['accuracy']:>8.1f}% {s['errors']:>7} {s['difficulty']:<10} {s['date']}")


def practice_mode():
    print("\n  Practice Mode - Type as many sentences as you can!")
    print("  Type 'quit' to stop.\n")

    total_wpm = []
    total_accuracy = []
    round_num = 0

    while True:
        round_num += 1
        difficulty = random.choice(["easy", "medium"])
        text = random.choice(SENTENCES[difficulty])

        print(f"\n  Round {round_num}:")
        print(f"  \033[1;36m{text}\033[0m\n")

        start = time.time()
        typed = input("  > ")
        elapsed = time.time() - start

        if typed.strip().lower() == "quit":
            break

        wpm = (len(text.split()) / elapsed) * 60
        accuracy, _ = calculate_accuracy(text, typed)
        total_wpm.append(wpm)
        total_accuracy.append(accuracy)

        print(f"  WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}%")

    if total_wpm:
        avg_wpm = sum(total_wpm) / len(total_wpm)
        avg_acc = sum(total_accuracy) / len(total_accuracy)
        print(f"\n  Practice Summary:")
        print(f"  Rounds:       {round_num - 1}")
        print(f"  Average WPM:  {avg_wpm:.1f}")
        print(f"  Average Acc:  {avg_acc:.1f}%")


def main():
    while True:
        print(f"\n  {'=' * 40}")
        print(f"       TYPING SPEED TEST")
        print(f"  {'=' * 40}")
        print("  1. Easy (short sentences)")
        print("  2. Medium (longer sentences)")
        print("  3. Hard (technical paragraphs)")
        print("  4. Code (programming snippets)")
        print("  5. Practice Mode (continuous)")
        print("  6. High Scores")
        print("  7. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            run_test("easy")
        elif choice == "2":
            run_test("medium")
        elif choice == "3":
            run_test("hard")
        elif choice == "4":
            run_test("code")
        elif choice == "5":
            practice_mode()
        elif choice == "6":
            show_scores()
        elif choice == "7":
            print("  Keep typing! Goodbye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
