from game_harness.harness.runtime import run_game
from game_harness.trace.logger import setup_loagging


def main() -> None:
    print("Hello from game-harness!")
    print("===============================")

    try:
        setup_loagging()
        run_game()
    except KeyboardInterrupt:
        print("\nGame exited.")

    print("===============================")
