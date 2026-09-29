# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Machine-readable run provenance: every run now writes `provenance/provenance.yml`
  with the pipeline version, Nextflow version, git commit, run/session IDs,
  command line, effective parameters, and per-process tool versions
  (`versions.yml` collected from each stage).
- `--version` flags on `bin/summarize_pangenome.py`, `bin/build_report.py` and
  `bin/record_provenance.py`.
- Stub-mode coverage for the pre-annotated GFF3 input branch, with shared
  output-contract assertions (`tests/assert_stub_results.sh`) checking all five
  result stages, stub summary values, the Newick tree, and the provenance record.
- Expanded Python tests: Roary filename branch, empty/missing/malformed
  presence-absence tables, single-genome and threshold-boundary cases, strict
  summary parsing, and provenance generation.
- Pinned Python test dependencies (`tests/requirements.txt`).
- `examples/README.md` explaining the samplesheet templates.
- Real-data validation evidence: `examples/real_data/` with the accession
  manifest of the six RefSeq Complete *E. coli* genomes used for the
  end-to-end release-gate runs (2026-09-28/29), and the outcome documented in
  `docs/10_validation.md`.
- Weekly real-data smoke test (`.github/workflows/real-data-smoke.yml`):
  runs the genuine Roary route on a tiny real *E. coli* subset
  (`examples/smoke/`) with micromamba-built conda environments, guarding
  against solve drift and tool breakage. First green run still pending review.

### Changed
- **Version 0.2.0 (unreleased).** The 0.1.0 pre-release shipped with Panaroo as
  the default engine; the default is now Roary. The version bump records that
  behavior change so citations are unambiguous. `CITATION.cff`,
  `nextflow.config` and this changelog are kept in sync.
- Pangenome inputs are now sorted (`toSortedList()`) before Roary/Panaroo, so
  identical runs produce identical column order and checksums in
  `gene_presence_absence*.csv`.
- GFF3 inputs are now published to `01_annotation/`, matching the FASTA route.
- Tightened conda specifications (`mafft=7.*`, `pandas=2.*`, `numpy=1.*`,
  `matplotlib=3.*`); conda environments now resolve with mamba.
- GFF3 engine arguments are individually quoted.
- `summarize_pangenome.py` now fails fast on empty or header-only
  presence/absence tables instead of emitting a degenerate summary.
- `build_report.py` now strictly parses `summary.tsv` and fails on corruption
  instead of rendering a silently wrong report.
- matplotlib uses the headless-safe `Agg` backend explicitly.
- Removed the inert `maxRetries` setting (it only applies to the `retry`
  error strategy; this workflow uses `terminate`).
- CI pins Nextflow to the documented minimum version (24.10.0).

### Fixed
- README results tree now lists `INTERPRETATION_NOTES.txt` and the
  `provenance/` directory, both of which are published outputs.

## [0.1.0] - 2026-08-19 (pre-release MVP)

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

[Unreleased]: https://github.com/mbilal-OU/PanPhyloFlow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mbilal-OU/PanPhyloFlow/releases/tag/v0.1.0
