# 9. Scaling and current limits

## What v0.1.0 is meant for

The first release is intentionally aimed at small-to-moderate bacterial genome collections on a local Linux/WSL workstation or a single compute node.

## What becomes difficult at large scale

As genome count and taxonomic breadth increase, runtime, memory, annotation inconsistencies, graph complexity, and the probability of an extremely small core can increase substantially.

A successful run is not automatically a biologically sensible comparison.

## Planned scaling features

Future releases can add:

- Slurm and institutional HPC profiles;
- genome QC with completeness/contamination filtering;
- GTDB-Tk metadata integration;
- PIRATE and PPanGGOLiN routes;
- true clustering-parameter reruns rather than prevalence-only sensitivity;
- accessory-gene PCA and tree/matrix visualization;
- formal pangenome openness models with resampling;
- optional recombination-aware phylogenetic preprocessing;
- container profiles and locked environments.
