import argparse

from lib.keyword_search import (
    search_command, 
    build_command, 
    tf_command, 
    idf_command, 
    tfidf_command,
    bm25_idf_command,
    )

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Build movie index")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    tf_parser = subparsers.add_parser("tf", help="Display term frequency for a term in a document")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="A term to display term frequency for")

    idf_parser = subparsers.add_parser("idf", help="Display inverse document frequency for a term")
    idf_parser.add_argument("term", type=str, help="A term to display inverse document frequency for")

    tfidf_parser = subparsers.add_parser("tfidf", help="Display TF-IDF value for a term in a document")
    tfidf_parser.add_argument("doc_id", type=int, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="A term to display TF-IDF value for")

    bm25idf_parser = subparsers.add_parser("bm25idf", help="Display BM25 IDF value for a term in a document")
    bm25idf_parser.add_argument("term", type=str, help="A term to display BM25 IDF value for")

    args = parser.parse_args()
    
    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search_command(args.query, 5)
            for movie in results:
                print(f"{movie["id"]}. {movie["title"]}")
        case "build":
            build_command()
        case "tf":
            print(tf_command(args.doc_id, args.term))
        case "idf":
            idf = idf_command(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "tfidf":
            tf_idf = tfidf_command(args.doc_id, args.term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}")
        case "bm25idf":
            bm25_idf = bm25_idf_command(args.term)
            print(f"BM25 IDF score of '{args.term}': {bm25_idf:.2f}")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()