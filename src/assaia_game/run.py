import sys

from assaia_game.setup.build import build_cli_game


def build_and_run() -> None:
    engine = build_cli_game()
    engine.run()


def main() -> None:
    try:
        build_and_run()
    except KeyboardInterrupt as ki:
        print("\nGame Aborted.", file=sys.stderr)
        raise SystemExit(130) from ki


if __name__ == "__main__":
    main()
