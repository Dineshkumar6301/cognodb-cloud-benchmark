# cognodb-cloud-benchmark

Reproducible benchmark comparing CognoDB Cloud with other graph database platforms.

## Status

Core read benchmark implementation completed for:

- CognoDB Cloud
- Neo4j AuraDB
- Memgraph
- ArangoDB

FalkorDB connectivity was successfully verified, but the full benchmark dataset load was not completed because of intermittent TLS connection timeouts.

## Objective

This project benchmarks multiple graph database platforms using the same dataset, equivalent workloads, the same client environment, and documented resource configurations.

The goal is to measure graph database read performance under comparable workloads.

## Databases

- CognoDB Cloud
- Neo4j AuraDB
- Memgraph
- FalkorDB
- ArangoDB

## Dataset

The benchmark dataset contains:

- 43,824 Person nodes
- 150,000 TRUSTS relationships

The same benchmark dataset is used for the completed database comparisons.

## Benchmark Categories

- Data ingestion throughput
- 1-hop traversal latency
- 2-hop traversal latency
- 3-hop traversal latency
- Point lookup latency
- Indexed/filtered lookup latency
- Aggregation latency
- Concurrent mixed read/write throughput
- Observable resource footprint

## Completed Read Benchmark

The completed read benchmark uses 100 measured iterations per workload.

### Mean latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 269.87 ms | **54.26 ms** | 754.51 ms | 320.41 ms |
| Indexed lookup | 261.91 ms | **58.47 ms** | 754.29 ms | 305.81 ms |
| 1-hop traversal | N/A | N/A | 757.85 ms | **271.38 ms** |
| 2-hop traversal | N/A | N/A | 755.89 ms | **336.17 ms** |
| 3-hop traversal | N/A | N/A | **755.41 ms** | 3758.33 ms |
| Aggregation | 393.90 ms | **75.12 ms** | 770.94 ms | 312.37 ms |

N/A indicates that an equivalent result was not available in the corresponding existing benchmark result file.

### P50 latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 260.58 ms | **53.84 ms** | 753.88 ms | 274.99 ms |
| Indexed lookup | 261.59 ms | **54.00 ms** | 753.44 ms | 278.85 ms |
| 1-hop traversal | N/A | N/A | 752.20 ms | **263.23 ms** |
| 2-hop traversal | N/A | N/A | 752.54 ms | **266.33 ms** |
| 3-hop traversal | N/A | N/A | **754.60 ms** | 913.94 ms |
| Aggregation | 386.74 ms | **66.73 ms** | 768.20 ms | 278.06 ms |

### P95 latency

| Workload | CognoDB | Neo4j | Memgraph | ArangoDB |
|---|---:|---:|---:|---:|
| Point lookup | 263.73 ms | **56.68 ms** | 764.39 ms | 487.16 ms |
| Indexed lookup | 264.39 ms | **56.99 ms** | 760.24 ms | 404.52 ms |
| 1-hop traversal | N/A | N/A | 768.55 ms | **318.26 ms** |
| 2-hop traversal | N/A | N/A | 771.50 ms | **648.87 ms** |
| 3-hop traversal | N/A | N/A | **767.68 ms** | 14111.00 ms |
| Aggregation | 483.28 ms | **76.13 ms** | 784.51 ms | 422.59 ms |

## Fastest Database by Mean Latency

Based on the currently completed benchmark results:

| Workload | Fastest | Mean latency |
|---|---|---:|
| Point lookup | Neo4j | 54.26 ms |
| Indexed lookup | Neo4j | 58.47 ms |
| 1-hop traversal | ArangoDB | 271.38 ms |
| 2-hop traversal | ArangoDB | 336.17 ms |
| 3-hop traversal | Memgraph | 755.41 ms |
| Aggregation | Neo4j | 75.12 ms |

These results should be interpreted as benchmark measurements from the current test environment, not as universal performance claims about each database platform.

## ArangoDB Dataset Verification

The ArangoDB dataset was successfully loaded and verified:

- Person nodes: 43,824
- TRUSTS relationships: 150,000
- Graph exists: Yes
- Person collection exists: Yes
- TRUSTS collection exists: Yes

ArangoDB workload queries were also successfully executed for:

1. Point lookup
2. Indexed lookup
3. One-hop traversal
4. Two-hop traversal
5. Three-hop traversal
6. Aggregation

## ArangoDB Read Benchmark

100 measured iterations were completed successfully for each workload.

| Workload | P50 | P95 | Mean | Successful |
|---|---:|---:|---:|---:|
| Point lookup | 274.99 ms | 487.16 ms | 320.41 ms | 100 |
| Indexed lookup | 278.85 ms | 404.52 ms | 305.81 ms | 100 |
| 1-hop traversal | 263.23 ms | 318.26 ms | 271.38 ms | 100 |
| 2-hop traversal | 266.33 ms | 648.87 ms | 336.17 ms | 100 |
| 3-hop traversal | 913.94 ms | 14111.00 ms | 3758.33 ms | 100 |
| Aggregation | 278.06 ms | 422.59 ms | 312.37 ms | 100 |

The 3-hop ArangoDB workload shows substantially higher tail latency, with a P95 of approximately 14.11 seconds.

## FalkorDB Status

FalkorDB connection testing was successful:

```text
PING: True

FalkorDB connection successful.