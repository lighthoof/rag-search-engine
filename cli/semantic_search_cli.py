import argparse
from lib.semantic_search import SemanticSearch
from lib.semantic_functions import verify_model, embed_text, verify_embeddings, embed_query_text, search

def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("verify", help="Verify semantic model")
    subparsers.add_parser("verify_embeddings", help="Verify movie data embeddings")

    embed_parser = subparsers.add_parser("embed_text", help="Get an embedding for a string")
    embed_parser.add_argument("text", type=str, help="Text to get the embedding for")

    embed_parser = subparsers.add_parser("embed_query", help="Get an embedding for a query")
    embed_parser.add_argument("query", type=str, help="Query to get the embedding for")

    search_parser = subparsers.add_parser("search", help="Run search for a query")
    search_parser.add_argument("query", type=str, help="Query for search to run on")
    search_parser.add_argument("--limit", type=int, help="Number of top results to show")

    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case "verify_embeddings":
            verify_embeddings()
        case "embed_query":
            embed_query_text(args.query)
        case "search":
            results = search(args.query,args.limit)
            for i, result in zip(range(len(results)),results):
                print(f"{i+1}. {result['title']} (score: {result['score']:.4f})\n\t{result['description']}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()