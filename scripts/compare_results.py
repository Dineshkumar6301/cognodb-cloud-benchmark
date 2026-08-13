import json
from pathlib import Path

RESULTS = Path("results/raw")

FILES = {
    "Cognodb": RESULTS / "cognodb_read_benchmark.json",
    "Neo4j": RESULTS / "neo4j_read_benchmark.json",
    "Memgraph": RESULTS / "memgraph_read_benchmark.json",
    "ArangoDB": RESULTS / "arangodb_read_benchmark.json",
}

WORKLOADS = {
    "Point lookup": "point_lookup",
    "Indexed lookup": "indexed_lookup",
    "1-hop traversal": "one_hop_traversal",
    "2-hop traversal": "two_hop_traversal",
    "3-hop traversal": "three_hop_traversal",
    "Aggregation": "aggregation",
}

data = {}

for db, path in FILES.items():
    with open(path, "r", encoding="utf-8") as f:
        data[db] = json.load(f)


def get_result(db, workload):
    result = data[db]
    lower_key = WORKLOADS[workload]

    # Cognodb / Neo4j format
    if lower_key in result:
        return result[lower_key]

    # Memgraph format
    if "workloads" in result:
        if workload in result["workloads"]:
            return result["workloads"][workload]

    # ArangoDB format
    if "results" in result:
        if workload in result["results"]:
            return result["results"][workload]

    return None


print()
print("DATABASE READ BENCHMARK COMPARISON")
print("=" * 110)

header = f"{'Workload':<22}"
for db in data:
    header += f"{db:<18}"
print(header)
print("-" * 110)

for workload in WORKLOADS:
    row = f"{workload:<22}"

    for db in data:
        item = get_result(db, workload)

        if item:
            row += f"{item['mean_ms']:.2f} ms".ljust(18)
        else:
            row += "N/A".ljust(18)

    print(row)


print()
print("P50 LATENCY")
print("=" * 110)

for workload in WORKLOADS:
    values = []

    for db in data:
        item = get_result(db, workload)

        if item:
            values.append((db, item["p50_ms"]))

    values.sort(key=lambda x: x[1])

    print()
    print(workload)

    for rank, (db, value) in enumerate(values, 1):
        print(f"{rank}. {db:<15} {value:.2f} ms")


print()
print("P95 LATENCY")
print("=" * 110)

for workload in WORKLOADS:
    values = []

    for db in data:
        item = get_result(db, workload)

        if item:
            values.append((db, item["p95_ms"]))

    values.sort(key=lambda x: x[1])

    print()
    print(workload)

    for rank, (db, value) in enumerate(values, 1):
        print(f"{rank}. {db:<15} {value:.2f} ms")


print()
print("FASTEST DATABASE BY MEAN LATENCY")
print("=" * 110)

for workload in WORKLOADS:
    values = []

    for db in data:
        item = get_result(db, workload)

        if item:
            values.append((db, item["mean_ms"]))

    values.sort(key=lambda x: x[1])

    if values:
        fastest_db, fastest_value = values[0]
        print(
            f"{workload:<22} "
            f"{fastest_db:<15} "
            f"{fastest_value:.2f} ms"
        )


print()
print("=" * 110)
print("Comparison completed successfully.")