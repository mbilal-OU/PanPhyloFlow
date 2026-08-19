# 3. Building the pangenome

PanPhyloFlow supports two pangenome engines in v0.1.0.

## Roary — default

Roary is the default route in PanPhyloFlow. It provides the classical bacterial gene-family pangenome workflow, produces the familiar gene presence/absence matrix, and integrates naturally with Prokka-style GFF3 annotations.

The default identity setting is exposed through `--roary_identity` and the core prevalence definition through `--core_threshold`.

Roary is especially useful when you want:

- direct comparability with a large body of bacterial pangenome literature;
- transparent teaching of classical core/accessory gene-family analysis;
- familiar Roary output files for downstream scripts and visualization.

## Panaroo — alternative

Panaroo is available as an alternative engine. Its graph-based strategy is designed to reduce errors associated with annotation problems, fragmented gene calls and inconsistent gene boundaries.

Panaroo is therefore useful as a comparison route when you want to examine how a different inference strategy changes the reconstructed pangenome.

## Important parameter distinction

Panaroo's `--family_threshold` and Roary's `-i` identity setting are **not interchangeable knobs**. They belong to different pangenome inference strategies. PanPhyloFlow exposes them separately rather than presenting them as equivalent thresholds.

Likewise, `--core_threshold` controls the fraction of genomes required for a family to be classified as core. Changing that prevalence threshold does not rerun gene-family clustering.
