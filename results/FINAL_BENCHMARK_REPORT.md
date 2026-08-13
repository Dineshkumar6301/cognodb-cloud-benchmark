# CognoDB Cloud Graph Database Benchmark

Final read benchmark comparison generated automatically from the completed raw benchmark result files in `results/raw/`.

Report generated: 2026-08-13 20:28:46

## Benchmark Scope

- Dataset: 43,824 Person nodes
- Relationships: 150,000 TRUSTS relationships
- Measured iterations: 100 per completed workload
- Metrics: mean, P50, P95 latency

Results represent measurements from the current benchmark environment and should not be interpreted as universal database rankings.

## Mean Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 256.16 ms | 54.26 ms | 754.51 ms | 320.41 ms |
| Indexed lookup | 260.61 ms | 58.47 ms | 754.29 ms | 305.81 ms |
| 1-hop traversal | 255.16 ms | 60.44 ms | 757.85 ms | 271.38 ms |
| 2-hop traversal | 284.03 ms | 57.70 ms | 755.89 ms | 336.17 ms |
| 3-hop traversal | 307.98 ms | 61.96 ms | 755.41 ms | 3758.33 ms |
| Aggregation | 376.22 ms | 75.12 ms | 770.94 ms | 312.37 ms |

## P50 Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 254.95 ms | 53.84 ms | 753.88 ms | 274.99 ms |
| Indexed lookup | 255.67 ms | 54.00 ms | 753.44 ms | 278.85 ms |
| 1-hop traversal | 253.72 ms | 53.35 ms | 752.20 ms | 263.23 ms |
| 2-hop traversal | 254.49 ms | 53.63 ms | 752.54 ms | 266.33 ms |
| 3-hop traversal | 259.19 ms | 54.24 ms | 754.60 ms | 913.94 ms |
| Aggregation | 381.00 ms | 66.73 ms | 768.20 ms | 278.06 ms |

## P95 Latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 266.12 ms | 56.68 ms | 764.39 ms | 487.16 ms |
| Indexed lookup | 260.00 ms | 56.99 ms | 760.24 ms | 404.52 ms |
| 1-hop traversal | 266.36 ms | 59.78 ms | 768.55 ms | 318.26 ms |
| 2-hop traversal | 334.19 ms | 58.54 ms | 771.50 ms | 648.87 ms |
| 3-hop traversal | 477.72 ms | 59.46 ms | 767.68 ms | 14111.00 ms |
| Aggregation | 404.83 ms | 76.13 ms | 784.51 ms | 422.59 ms |

## Fastest Database by Mean Latency

- **Point lookup: Neo4j - 54.26 ms**
- **Indexed lookup: Neo4j - 58.47 ms**
- **1-hop traversal: Neo4j - 60.44 ms**
- **2-hop traversal: Neo4j - 57.70 ms**
- **3-hop traversal: Neo4j - 61.96 ms**
- **Aggregation: Neo4j - 75.12 ms**

## Completed Databases

- CognoDB
- Neo4j
- Memgraph
- ArangoDB

## FalkorDB

FalkorDB connection testing succeeded, but the full dataset benchmark was not completed because of intermittent TLS handshake connection timeouts.

FalkorDB is therefore excluded from the numerical comparison until a successful full benchmark run is completed.

## Important Findings

- **Point lookup: Neo4j (54.26 ms mean latency)**
- **Indexed lookup: Neo4j (58.47 ms mean latency)**
- **1-hop traversal: Neo4j (60.44 ms mean latency)**
- **2-hop traversal: Neo4j (57.70 ms mean latency)**
- **3-hop traversal: Neo4j (61.96 ms mean latency)**
- **Aggregation: Neo4j (75.12 ms mean latency)**

These findings describe this benchmark environment only.

## Limitations

The benchmark currently reports completed read workloads. Concurrent mixed read/write throughput and observable resource footprint are not included in the numerical comparison.

FalkorDB requires a successful full benchmark run before it can be included in the numerical comparison.

## Raw Results

The source JSON files are stored under:

```text
results/raw/
```
