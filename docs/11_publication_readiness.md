# 11. Publication readiness

PanPhyloFlow is being hardened as a scientific software release. The repository should not be treated as submission-ready merely because the workflow runs or the CI badges are green.

The publication target requires reviewers to be able to obtain the code and test data, install or deploy a clearly defined version, reproduce manuscript examples, inspect the analytical choices and understand the limitations of the outputs.

## Current release gates

Two GitHub issues are intentionally blocking a stable publication release:

- **Issue #2:** real end-to-end validation on accessioned bacterial genomes.
- **Issue #7:** broader publication hardening covering correctness, terminology, provenance, portability, testing, prior-art comparison and archival research objects.

## What must be demonstrated before submission

A publication release should provide all of the following:

1. at least one complete real-data analysis for each supported pangenome route;
2. independent cross-checks of PanPhyloFlow summaries against native Roary/Panaroo outputs;
3. reviewer-reproducible test input and expected output;
4. locked or immutable software environments and validated execution profiles;
5. machine-readable provenance including software versions and analysis parameters;
6. explicit documentation of how analytical choices affect interpretation;
7. a comparison with overlapping tools that makes the project's added value clear;
8. an archived release with persistent identifiers after the final project name is fixed.

## Publication thesis under evaluation

The defensible contribution is not simply that several command-line tools are connected together. Existing software already supports substantial parts of genome-to-pangenome-to-phylogeny analysis.

The publication version is therefore being developed around a stricter goal: **make consequential analytical choices visible, reproducible and auditable, and make method-dependent differences straightforward to inspect on the same input genomes.**

Features that do not strengthen correctness, reproducibility or this central contribution should not delay the validation work.
