# CognoDB Cloud Graph Database Benchmark

Final read benchmark comparison using the completed raw benchmark result files in `results/raw/`.

Report generated: 2026-08-13 19:49:39

## Benchmark Scope

- Dataset: 43,824 Person nodes
- Relationships: 150,000 TRUSTS relationships
- Measured iterations: 100 per completed workload
- Metrics: mean, P50, P95 latency

Results represent measurements from the current benchmark environment and should not be interpreted as universal database rankings.

## Mean Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 269.87 ms | 54.26 ms | 754.51 ms | 320.41 ms |
| Indexed lookup | 261.91 ms | 58.47 ms | 754.29 ms | 305.81 ms |
| 1-hop traversal | N/A | N/A | 757.85 ms | 271.38 ms |
| 2-hop traversal | N/A | N/A | 755.89 ms | 336.17 ms |
| 3-hop traversal | N/A | N/A | 755.41 ms | 3758.33 ms |
| Aggregation | 393.90 ms | 75.12 ms | 770.94 ms | 312.37 ms |

## P50 Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 260.58 ms | 53.84 ms | 753.88 ms | 274.99 ms |
| Indexed lookup | 261.59 ms | 54.00 ms | 753.44 ms | 278.85 ms |
| 1-hop traversal | N/A | N/A | 752.20 ms | 263.23 ms |
| 2-hop traversal | N/A | N/A | 752.54 ms | 266.33 ms |
| 3-hop traversal | N/A | N/A | 754.60 ms | 913.94 ms |
| Aggregation | 386.74 ms | 66.73 ms | 768.20 ms | 278.06 ms |

## P95 Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 263.73 ms | 56.68 ms | 764.39 ms | 487.16 ms |
| Indexed lookup | 264.39 ms | 56.99 ms | 760.24 ms | 404.52 ms |
| 1-hop traversal | N/A | N/A | 768.55 ms | 318.26 ms |
| 2-hop traversal | N/A | N/A | 771.50 ms | 648.87 ms |
| 3-hop traversal | N/A | N/A | 767.68 ms | 14111.00 ms |
| Aggregation | 483.28 ms | 76.13 ms | 784.51 ms | 422.59 ms |

## Fastest Database by Mean Latency

- **Point lookup: Neo4j — 54.26 ms**
- **Indexed lookup: Neo4j — 58.47 ms**
- **1-hop traversal: ArangoDB — 271.38 ms**
- **2-hop traversal: ArangoDB — 336.17 ms**
- **3-hop traversal: Memgraph — 755.41 ms**
- **Aggregation: Neo4j — 75.12 ms**

## Completed Databases

- CognoDB Cloud
- Neo4j AuraDB
- Memgraph
- ArangoDB

## FalkorDB

FalkorDB connection testing succeeded, but the full dataset benchmark was not completed because the client encountered intermittent TLS handshake connection timeouts.

FalkorDB is therefore excluded from the numerical comparison until a successful full benchmark run is completed.

## Important Findings

Neo4j produced the lowest observed mean latency for point lookup, indexed lookup, and aggregation.
ArangoDB produced the lowest observed mean latency for the available 1-hop and 2-hop traversal comparisons.
Memgraph produced the lowest observed mean latency for the available 3-hop traversal comparison.

These findings describe this benchmark environment only.

## Limitations

Equivalent traversal results are not currently available in the CognoDB and Neo4j result files for all traversal workloads.
The benchmark does not yet contain completed comparable measurements for concurrent mixed read/write throughput or observable resource footprint.
FalkorDB requires a successful full benchmark run before it can be included in the numerical comparison.

## Raw Results

The source JSON files are stored under:

```text
results/raw/
```
