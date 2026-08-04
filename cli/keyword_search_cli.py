import argparse
import json
import string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    with open("data/movies.json", "r") as file:
        data = json.load(file)

    results = []
    for movie in data["movies"]:
        removal_table = str.maketrans("","",string.punctuation)
        query = args.query.lower().translate(removal_table)
        title = movie["title"].lower().translate(removal_table)
        if query in title and len(results) < 5:
            results.append(movie)

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            for i, result in enumerate(results):
                print(f"{i+1}. {result["title"]}")
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()