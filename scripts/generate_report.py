import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "raw"
OUTPUT = ROOT / "results" / "FINAL_BENCHMARK_REPORT.md"

FILES = {
    "CognoDB": RESULTS / "cognodb_read_benchmark.json",
    "Neo4j": RESULTS / "neo4j_read_benchmark.json",
    "Memgraph": RESULTS / "memgraph_read_benchmark.json",
    "ArangoDB": RESULTS / "arangodb_read_benchmark.json",
}

WORKLOADS = {
    "Point lookup": "point_lookup",
    "Indexed lookup": "indexed_lookup",
    "1-hop traversal": "one_hop",
    "2-hop traversal": "two_hop",
    "3-hop traversal": "three_hop",
    "Aggregation": "aggregation",
}


def load_database(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_result(data, workload_key, display_name):
    if workload_key in data:
        return data[workload_key]

    if "workloads" in data:
        if display_name in data["workloads"]:
            return data["workloads"][display_name]

    if "results" in data:
        if display_name in data["results"]:
            return data["results"][display_name]

    return None


data = {}

for name, path in FILES.items():
    if path.exists():
        data[name] = load_database(path)


lines = []

lines.append("# CognoDB Cloud Graph Database Benchmark")
lines.append("")
lines.append(
    "Final read benchmark comparison generated automatically from "
    "the completed raw benchmark result files in `results/raw/`."
)
lines.append("")
lines.append(
    f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
lines.append("")

lines.append("## Benchmark Scope")
lines.append("")
lines.append("- Dataset: 43,824 Person nodes")
lines.append("- Relationships: 150,000 TRUSTS relationships")
lines.append("- Measured iterations: 100 per completed workload")
lines.append("- Metrics: mean, P50, P95 latency")
lines.append("")
lines.append(
    "Results represent measurements from the current benchmark "
    "environment and should not be interpreted as universal database rankings."
)
lines.append("")


def make_table(metric, title):
    lines.append(f"## {title}")
    lines.append("")
    lines.append(
        "| Workload | "
        + " | ".join(data.keys())
        + " |"
    )
    lines.append(
        "|---|"
        + "|".join(["---:" for _ in data])
        + "|"
    )

    for display_name, workload_key in WORKLOADS.items():
        row = [display_name]

        for db in data:
            result = get_result(
                data[db],
                workload_key,
                display_name,
            )

            if result:
                row.append(f"{result[metric]:.2f} ms")
            else:
                row.append("N/A")

        lines.append("| " + " | ".join(row) + " |")

    lines.append("")


make_table("mean_ms", "Mean Latency")
make_table("p50_ms", "P50 Latency")
make_table("p95_ms", "P95 Latency")


lines.append("## Fastest Database by Mean Latency")
lines.append("")

for display_name, workload_key in WORKLOADS.items():
    values = []

    for db in data:
        result = get_result(
            data[db],
            workload_key,
            display_name,
        )

        if result:
            values.append(
                (db, result["mean_ms"])
            )

    if values:
        fastest_db, fastest_value = min(
            values,
            key=lambda x: x[1],
        )

        lines.append(
            f"- **{display_name}: {fastest_db} - "
            f"{fastest_value:.2f} ms**"
        )

lines.append("")

lines.append("## Completed Databases")
lines.append("")

for db in data:
    lines.append(f"- {db}")

lines.append("")

lines.append("## FalkorDB")
lines.append("")
lines.append(
    "FalkorDB connection testing succeeded, but the full dataset "
    "benchmark was not completed because of intermittent TLS handshake "
    "connection timeouts."
)
lines.append("")
lines.append(
    "FalkorDB is therefore excluded from the numerical comparison until "
    "a successful full benchmark run is completed."
)
lines.append("")

lines.append("## Important Findings")
lines.append("")

for display_name, workload_key in WORKLOADS.items():
    values = []

    for db in data:
        result = get_result(
            data[db],
            workload_key,
            display_name,
        )

        if result:
            values.append(
                (db, result["mean_ms"])
            )

    if values:
        fastest_db, fastest_value = min(
            values,
            key=lambda x: x[1],
        )

        lines.append(
            f"- **{display_name}: {fastest_db} "
            f"({fastest_value:.2f} ms mean latency)**"
        )

lines.append("")
lines.append(
    "These findings describe this benchmark environment only."
)
lines.append("")

lines.append("## Limitations")
lines.append("")
lines.append(
    "The benchmark currently reports completed read workloads. "
    "Concurrent mixed read/write throughput and observable resource "
    "footprint are not included in the numerical comparison."
)
lines.append("")
lines.append(
    "FalkorDB requires a successful full benchmark run before it can "
    "be included in the numerical comparison."
)
lines.append("")

lines.append("## Raw Results")
lines.append("")
lines.append(
    "The source JSON files are stored under:"
)
lines.append("")
lines.append("```text")
lines.append("results/raw/")
lines.append("```")
lines.append("")


OUTPUT.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print(f"Report generated: {OUTPUT}")


