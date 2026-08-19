# 3. Building the pangenome

PanPhyloFlow supports two engines in v0.1.0.

## Panaroo — default

Panaroo uses a graph-based strategy designed to reduce errors arising from annotation problems and fragmented gene calls. It is the default route.

## Roary — classical route

Roary remains useful for teaching, comparison with historical analyses, and compatibility with large amounts of existing bacterial pangenome literature.

## Important parameter distinction

Panaroo's `--family_threshold` and Roary's `-i` identity setting are **not interchangeable knobs**. They belong to different inference strategies. PanPhyloFlow therefore exposes them separately.
