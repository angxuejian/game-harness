from game_harness.harness.runtime import run_game

def main() -> None:
    print("Hello from game-harness!")
    print("===============================")

    try:
        run_game()
    except KeyboardInterrupt:
        print("\nGame exited.")

    print("===============================")
