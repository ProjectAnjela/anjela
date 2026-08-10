"""Command-line entry point for Anjela."""

from .core import Anjela
from .providers import EchoProvider


def main() -> None:
    assistant = Anjela(EchoProvider())
    print("Anjela MVP. Напиши 'exit' для выхода.")

    while True:
        try:
            text = input("ты> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if text.strip().lower() in {"exit", "quit"}:
            break

        try:
            print(f"Анжела> {assistant.ask(text)}")
        except ValueError as exc:
            print(f"Анжела> {exc}")


if __name__ == "__main__":
    main()
