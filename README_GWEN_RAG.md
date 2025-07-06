# GWEN – Dynamischer YAML-Kontext via RAG

Dieses Modul stellt ein einfaches Retrieval-Augmented-Generation (RAG) Setup für GWEN bereit. YAML-Dateien werden in einer Vektor-Datenbank (ChromaDB) abgelegt und können kontextabhängig abgefragt werden.

## Installation

```bash
pip install -r requirements_ordo.txt
```

## Nutzung

1. **YAML-Dateien indexieren**
   ```bash
   python gwen_rag.py index /pfad/zu/yaml_dateien
   ```
   Alle YAML-Dateien im angegebenen Verzeichnis werden segmentiert und in ChromaDB gespeichert.

2. **Abfrage stellen**
   ```bash
   python gwen_rag.py query "Wie funktioniert der Drift-Check?"
   ```
   Es werden die relevantesten YAML-Snippets ausgegeben.

Die Vektordatenbank wird persistent im Ordner `gwen_chroma` gespeichert.
