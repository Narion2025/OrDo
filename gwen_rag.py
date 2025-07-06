import argparse
from pathlib import Path
import yaml
import chromadb
from chromadb.utils import embedding_functions

class GwenRAG:
    """Simple RAG utility to index and query YAML snippets."""

    def __init__(self, db_path: str = "gwen_chroma", collection: str = "gwen_yamls"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            collection_name=collection, embedding_function=self.embed_fn
        )

    def index_directory(self, directory: str) -> None:
        base = Path(directory)
        yaml_files = list(base.rglob("*.yaml"))
        for file in yaml_files:
            with open(file, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except Exception:
                    continue
            if isinstance(data, dict):
                for key, value in data.items():
                    snippet = yaml.dump({key: value}, allow_unicode=True)
                    doc_id = f"{file.name}-{key}"
                    self.collection.add(
                        documents=[snippet],
                        ids=[doc_id],
                        metadatas=[{"file": str(file), "section": key}],
                    )
            else:
                snippet = yaml.dump(data, allow_unicode=True)
                doc_id = file.name
                self.collection.add(
                    documents=[snippet], ids=[doc_id], metadatas=[{"file": str(file)}]
                )
        print(f"Indexed {len(yaml_files)} YAML files from {directory}.")

    def query(self, text: str, n_results: int = 3):
        result = self.collection.query(query_texts=[text], n_results=n_results)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        for doc, meta in zip(docs, metas):
            print("---")
            print(f"File: {meta.get('file')} | Section: {meta.get('section')}")
            print(doc)


def main():
    parser = argparse.ArgumentParser(description="GWEN YAML RAG")
    sub = parser.add_subparsers(dest="command", required=True)

    idx = sub.add_parser("index", help="Index a directory of YAML files")
    idx.add_argument("directory", help="Path to YAML directory")

    qry = sub.add_parser("query", help="Query indexed YAMLs")
    qry.add_argument("text", help="Query text")
    qry.add_argument("-n", type=int, default=3, help="Number of results")

    args = parser.parse_args()
    rag = GwenRAG()

    if args.command == "index":
        rag.index_directory(args.directory)
    elif args.command == "query":
        rag.query(args.text, args.n)


if __name__ == "__main__":
    main()
