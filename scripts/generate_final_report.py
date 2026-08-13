import json
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
OUT = ROOT / "results" / "FINAL_BENCHMARK_REPORT.md"


FILES = {
    "CognoDB": RAW / "cognodb_read_benchmark.json",
    "Neo4j": RAW / "neo4j_read_benchmark.json",
    "Memgraph": RAW / "memgraph_read_benchmark.json",
    "ArangoDB": RAW / "arangodb_read_benchmark.json",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(data):
    """
    Normalize the different JSON formats used by the benchmark scripts.
    """
    if "results" in data and isinstance(data["results"], dict):
        source = data["results"]
    elif "workloads" in data and isinstance(data["workloads"], dict):
        source = data["workloads"]
    else:
        source = data

    result = {}

    aliases = {
        "point_lookup": "Point lookup",
        "indexed_lookup": "Indexed lookup",
        "one_hop_traversal": "1-hop traversal",
        "two_hop_traversal": "2-hop traversal",
        "three_hop_traversal": "3-hop traversal",
        "aggregation": "Aggregation",
    }

    for key, value in source.items():
        name = aliases.get(key, key)

        if not isinstance(value, dict):
            continue

        if "mean_ms" not in value:
            continue

        result[name] = {
            "mean_ms": value.get("mean_ms"),
            "p50_ms": value.get("p50_ms"),
            "p95_ms": value.get("p95_ms"),
            "successful": value.get(
                "successful",
                value.get("successful_iterations", value.get("iterations")),
            ),
            "failed": value.get(
                "failed",
                value.get("failed_iterations", 0),
            ),
        }

    return result


def fmt(value):
    if value is None:
        return "N/A"
    return f"{value:.2f} ms"


def main():
    databases = {}

    for name, path in FILES.items():
        if path.exists():
            databases[name] = normalize(load_json(path))

    workloads = [
        "Point lookup",
        "Indexed lookup",
        "1-hop traversal",
        "2-hop traversal",
        "3-hop traversal",
        "Aggregation",
    ]

    lines = []

    lines.append("# CognoDB Cloud Graph Database Benchmark")
    lines.append("")
    lines.append(
        "Final read benchmark comparison using the completed raw benchmark "
        "result files in `results/raw/`."
    )
    lines.append("")
    lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("## Benchmark Scope")
    lines.append("")
    lines.append("- Dataset: 43,824 Person nodes")
    lines.append("- Relationships: 150,000 TRUSTS relationships")
    lines.append("- Measured iterations: 100 per completed workload")
    lines.append("- Metrics: mean, P50, P95 latency")
    lines.append("")
    lines.append(
        "Results represent measurements from the current benchmark environment "
        "and should not be interpreted as universal database rankings."
    )
    lines.append("")

    lines.append("## Mean Latency")
    lines.append("")
    lines.append("| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |")
    lines.append("|---|---:|---:|---:|---:|")

    for workload in workloads:
        row = [workload]

        for db in ["CognoDB", "Neo4j", "Memgraph", "ArangoDB"]:
            value = databases.get(db, {}).get(workload, {}).get("mean_ms")
            row.append(fmt(value))

        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    lines.append("## P50 Latency")
    lines.append("")
    lines.append("| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |")
    lines.append("|---|---:|---:|---:|---:|")

    for workload in workloads:
        row = [workload]

        for db in ["CognoDB", "Neo4j", "Memgraph", "ArangoDB"]:
            value = databases.get(db, {}).get(workload, {}).get("p50_ms")
            row.append(fmt(value))

        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    lines.append("## P95 Latency")
    lines.append("")
    lines.append("| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |")
    lines.append("|---|---:|---:|---:|---:|")

    for workload in workloads:
        row = [workload]

        for db in ["CognoDB", "Neo4j", "Memgraph", "ArangoDB"]:
            value = databases.get(db, {}).get(workload, {}).get("p95_ms")
            row.append(fmt(value))

        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    lines.append("## Fastest Database by Mean Latency")
    lines.append("")

    for workload in workloads:
        candidates = []

        for db in databases:
            value = databases[db].get(workload, {}).get("mean_ms")

            if value is not None:
                candidates.append((value, db))

        if candidates:
            value, db = min(candidates)
            lines.append(f"- **{workload}: {db} — {value:.2f} ms**")
        else:
            lines.append(f"- **{workload}: No comparable result available**")

    lines.append("")

    lines.append("## Completed Databases")
    lines.append("")
    lines.append("- CognoDB Cloud")
    lines.append("- Neo4j AuraDB")
    lines.append("- Memgraph")
    lines.append("- ArangoDB")
    lines.append("")

    lines.append("## FalkorDB")
    lines.append("")
    lines.append(
        "FalkorDB connection testing succeeded, but the full dataset benchmark "
        "was not completed because the client encountered intermittent TLS "
        "handshake connection timeouts."
    )
    lines.append("")
    lines.append(
        "FalkorDB is therefore excluded from the numerical comparison until a "
        "successful full benchmark run is completed."
    )
    lines.append("")

    lines.append("## Important Findings")
    lines.append("")
    lines.append(
        "Neo4j produced the lowest observed mean latency for point lookup, "
        "indexed lookup, and aggregation."
    )
    lines.append(
        "ArangoDB produced the lowest observed mean latency for the available "
        "1-hop and 2-hop traversal comparisons."
    )
    lines.append(
        "Memgraph produced the lowest observed mean latency for the available "
        "3-hop traversal comparison."
    )
    lines.append("")
    lines.append(
        "These findings describe this benchmark environment only."
    )
    lines.append("")

    lines.append("## Limitations")
    lines.append("")
    lines.append(
        "Equivalent traversal results are not currently available in the "
        "CognoDB and Neo4j result files for all traversal workloads."
    )
    lines.append(
        "The benchmark does not yet contain completed comparable measurements "
        "for concurrent mixed read/write throughput or observable resource "
        "footprint."
    )
    lines.append(
        "FalkorDB requires a successful full benchmark run before it can be "
        "included in the numerical comparison."
    )
    lines.append("")

    lines.append("## Raw Results")
    lines.append("")
    lines.append("The source JSON files are stored under:")
    lines.append("")
    lines.append("```text")
    lines.append("results/raw/")
    lines.append("```")
    lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Final report created:")
    print(OUT)


if __name__ == "__main__":
    main()