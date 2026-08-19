# Changelog

## Unreleased

- Made **Roary** the default pangenome engine across code, configuration and documentation.
- Reframed PanGenFlow as an optional upstream genome-preparation companion rather than a dependency.
- Added the PanPhyloFlow workflow figure and refreshed README/documentation structure.
- Added an explicit validation-strategy chapter and stable-release gate.

## 0.1.0 — pre-release MVP

- Nextflow DSL2 orchestration.
- FASTA → Prokka annotation route.
- Pre-annotated GFF route.
- Panaroo default pangenome engine.
- Roary comparison route.
- Automated gene-frequency and core-threshold summaries.
- Descriptive accumulation trajectory with interpretation warning.
- IQ-TREE 3 core-genome phylogeny.
- Prefer Panaroo filtered core alignment when available.
- Static HTML report.
- Tutorial documentation.
- Parameter and sample-ID validation.
- Python unit tests.
- Full Nextflow DAG stub tests for Panaroo and Roary branches.
- GitHub Actions, issue templates, contribution guidance and citation metadata.
