from benchmark.config import (
    NODES_FILE,
    EDGES_FILE,
    RESULTS_DIR,
    RANDOM_SEED,
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    DATABASES,
    NODE_LABEL,
    RELATIONSHIP_TYPE,
)


print("Benchmark configuration")
print("-----------------------")

print("Nodes file:", NODES_FILE)
print("Nodes file exists:", NODES_FILE.exists())

print("Edges file:", EDGES_FILE)
print("Edges file exists:", EDGES_FILE.exists())

print("Results directory:", RESULTS_DIR)

print("Random seed:", RANDOM_SEED)

print("Warm-up iterations:", WARMUP_ITERATIONS)

print("Measured iterations:", MEASURED_ITERATIONS)

print("Databases:", ", ".join(DATABASES))

print("Node label:", NODE_LABEL)

print("Relationship type:", RELATIONSHIP_TYPE)