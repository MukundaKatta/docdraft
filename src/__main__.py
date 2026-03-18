"""CLI for docdraft."""
import sys, json, argparse
from .core import Docdraft

def main():
    parser = argparse.ArgumentParser(description="DocDraft — AI Legal Document Generator. Generate NDAs, contracts, and legal documents from plain English.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Docdraft()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.generate(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"docdraft v0.1.0 — DocDraft — AI Legal Document Generator. Generate NDAs, contracts, and legal documents from plain English.")

if __name__ == "__main__":
    main()
