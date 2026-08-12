from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Dataset
DATA_DIR = PROJECT_ROOT / "data" / "benchmark"

NODES_FILE = DATA_DIR / "nodes_enriched.csv"
EDGES_FILE = DATA_DIR / "edges.csv"


# Results
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"

RESULTS_FILE = RESULTS_DIR / "results.csv"


# Benchmark configuration
RANDOM_SEED = 42

WARMUP_ITERATIONS = 20

MEASURED_ITERATIONS = 100


# Database names
DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
    "arangodb",
]


# Graph model
NODE_LABEL = "Person"
RELATIONSHIP_TYPE = "TRUSTS"