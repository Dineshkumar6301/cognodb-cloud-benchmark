\# Cognodb Cloud Benchmark Report



\## 1. Overview



This project benchmarks graph/database workloads across multiple cloud database platforms using the same benchmark dataset and workload definitions.



Databases successfully benchmarked:



\- Cognodb

\- Neo4j

\- Memgraph

\- ArangoDB



FalkorDB was connection-tested successfully but could not be completed as a comparable benchmark because graph operations intermittently experienced TLS connection timeouts.



\## 2. Benchmark Dataset



The benchmark dataset contains:



\- 43,824 Person nodes

\- 150,000 TRUSTS relationships



The same logical dataset and workload categories were used across the completed database benchmarks.



\## 3. Workloads



The read benchmark measured:



1\. Point lookup

2\. Indexed lookup

3\. 1-hop traversal

4\. 2-hop traversal

5\. 3-hop traversal

6\. Aggregation



Each completed benchmark used 100 measured iterations.



The completed benchmarks reported 100 successful iterations and 0 failed iterations for their workloads.



\## 4. P50 Latency Results



Lower latency is better.



| Workload | Cognodb | Neo4j | Memgraph | ArangoDB |

|---|---:|---:|---:|---:|

| Point lookup | 260.58 ms | 53.84 ms | 753.88 ms | 274.99 ms |

| Indexed lookup | 261.59 ms | 54.00 ms | 753.44 ms | 278.85 ms |

| 1-hop traversal | 259.36 ms | 53.35 ms | 752.20 ms | 263.23 ms |

| 2-hop traversal | 259.34 ms | 53.63 ms | 752.54 ms | 266.33 ms |

| 3-hop traversal | 263.28 ms | 54.24 ms | 754.61 ms | 913.94 ms |

| Aggregation | 386.74 ms | 66.73 ms | 768.20 ms | 278.06 ms |



\## 5. P95 Latency Results



Lower latency is better.



| Workload | Cognodb | Neo4j | Memgraph | ArangoDB |

|---|---:|---:|---:|---:|

| Point lookup | 263.73 ms | 56.68 ms | 764.39 ms | 487.16 ms |

| Indexed lookup | 264.39 ms | 56.99 ms | 760.24 ms | 404.52 ms |

| 1-hop traversal | 261.98 ms | 59.78 ms | 768.55 ms | 318.26 ms |

| 2-hop traversal | 264.44 ms | 58.54 ms | 771.50 ms | 648.87 ms |

| 3-hop traversal | 489.80 ms | 59.46 ms | 767.68 ms | 14,111.00 ms |

| Aggregation | 483.28 ms | 76.13 ms | 784.51 ms | 422.59 ms |



\## 6. Results Analysis



\### Neo4j



Neo4j achieved the lowest measured latency across all six workloads.



Its P50 latency remained approximately 53–67 ms, while P95 remained approximately 57–76 ms.



This makes Neo4j the fastest database in this particular benchmark environment and workload configuration.



\### Cognodb



Cognodb showed consistent latency for point lookups and graph traversals.



Most P50 values were approximately 259–263 ms.



The 3-hop traversal had a higher P95 of approximately 490 ms, while aggregation had a P50 of approximately 387 ms.



Cognodb therefore demonstrated relatively stable performance across the graph traversal workloads.



\### ArangoDB



ArangoDB performed competitively for 1-hop traversal and aggregation.



The 1-hop traversal P50 was approximately 263 ms and aggregation P50 was approximately 278 ms.



However, 3-hop traversal showed significant tail latency:



\- P50: 913.94 ms

\- P95: 14,111.00 ms

\- Mean: 3,758.33 ms



This is the largest latency outlier among the completed benchmarks.



\### Memgraph



Memgraph successfully completed the benchmark workload, but measured latency was substantially higher in this environment.



P50 latency was approximately 752–768 ms across the tested workloads.



The results indicate that Memgraph was slower than the other three completed platforms under this particular benchmark configuration.



\## 7. Overall Ranking



Based primarily on P50 latency:



1\. \*\*Neo4j\*\* — fastest overall

2\. \*\*Cognodb\*\* — consistent middle-range performance

3\. \*\*ArangoDB\*\* — competitive on several workloads but affected by 3-hop tail latency

4\. \*\*Memgraph\*\* — highest typical latency among the four completed platforms



\## 8. FalkorDB Status



FalkorDB connection testing succeeded.



However, graph loading and graph queries intermittently failed with SSL/TLS handshake timeouts.



Because the benchmark dataset could not be reliably loaded and verified, FalkorDB is excluded from the performance ranking.



This should be reported as an infrastructure/connectivity limitation rather than as a performance result.



\## 9. Benchmark Limitations



The results represent this specific benchmark environment and configuration.



They should not be interpreted as universal performance rankings for the database products.



Factors that can influence the results include:



\- Cloud region

\- Network latency

\- Instance size

\- Database configuration

\- Index configuration

\- Query implementation

\- Connection overhead

\- Dataset characteristics

\- Cloud service load



\## 10. Conclusion



The benchmark successfully evaluated four database platforms using the same logical graph dataset and six read workloads.



Neo4j produced the lowest latency across the measured workloads.



Cognodb showed stable performance across most graph operations.



ArangoDB was competitive for shallow traversal and aggregation but showed a substantial 3-hop tail-latency outlier.



Memgraph completed the workloads successfully but showed higher latency in this environment.



FalkorDB could not be included in the final performance comparison because of intermittent TLS connection failures during graph operations.



The benchmark therefore provides a reproducible comparison of the four successfully completed platforms while clearly documenting the FalkorDB limitation.

