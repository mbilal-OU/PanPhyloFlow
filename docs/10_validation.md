# 10. Validation strategy

PanPhyloFlow separates **workflow validation** from **biological validation**.

## What CI currently validates

GitHub Actions checks that:

- the Python summary/report tests pass;
- the complete Nextflow DAG executes in `-stub-run` mode;
- both the Roary and Panaroo branches satisfy the expected process/output contracts;
- the documentation site builds successfully.

A weekly scheduled job additionally runs the real (non-stub) Roary route on a
tiny real dataset — the first 200 kb of two RefSeq *E. coli* genomes in
`examples/smoke/` — with the genuine conda tool stack (Prokka, Roary,
IQ-TREE). It guards against conda-solve drift and tool breakage that stub
mode cannot see. It is a regression smoke test, not biological validation:
the dataset is truncated and the cohort is too small for inference.

These tests are important because they detect broken channel wiring, invalid output declarations, reporting regressions and configuration errors.

## What stub testing cannot prove

Stub mode does not execute Prokka, Roary, Panaroo or IQ-TREE on biological data. It therefore cannot prove that:

- the partially pinned conda specifications solve correctly on every platform;
- real GFF3 annotations behave as expected across diverse bacterial genomes;
- reported counts match native pangenome outputs on real datasets;
- a real core alignment is phylogenetically appropriate;
- runtime and memory estimates are adequate for a given dataset.

## Stable-release gate

Before the first stable release, PanPhyloFlow should be run end to end on a small, taxonomically coherent bacterial cohort.

Recommended checks:

1. run FASTA → Prokka → **Roary** → summary → IQ-TREE → report;
2. repeat the same cohort with Panaroo;
3. compare summary counts with native engine outputs;
4. verify that Panaroo's filtered core alignment is preferred when available;
5. inspect the final tree, report, figures and TSVs;
6. record software versions, Nextflow version, runtime and peak memory;
7. publish the accession list or a small reproducible example dataset.

The current release-gate task is tracked in [GitHub issue #2](https://github.com/mbilal-OU/PanPhyloFlow/issues/2).

### Release-gate validation performed (2026-09-28/29)

The gate above was executed on six RefSeq Complete *E. coli* genomes
(K-12 MG1655, K-12 W3110, Sakai O157:H7, UTI89, ED1a, CFT073; accession list
in `examples/real_data/accessions.tsv`):

- **Roary route:** Prokka 1.15.6 → Roary 3.13.0 → summary → IQ-TREE 3.1.3 →
  HTML report completed. Summary counts match Roary's native
  `summary_statistics.txt` exactly (3233 core families at 95%, 8570 total).
  The core-genome tree recovers K-12 monophyly (100/100) with Sakai as sister
  (100/100).
- **Panaroo route:** Panaroo 1.8.0 on the same cohort completed (3365 core
  families, 7902 total). The non-empty filtered core alignment was selected
  for phylogeny as designed; the tree agrees with the Roary tree on K-12
  monophyly and Sakai placement.

Nextflow 26.04.6 on a 2-CPU / 7.7 GB Linux VM with reduced process resources;
repo defaults were not exercised. Per-task runtime and peak memory are in the
run's `execution_trace.tsv`. This was a correctness gate, not a benchmark.

## Provenance is recorded automatically

Every run — stub or real — writes `provenance/provenance.yml` into the output
directory. It records the pipeline version, Nextflow version, git commit,
run/session IDs, the exact command line, the effective parameters, and the
per-process tool versions captured from each stage's conda environment. Keep
this file alongside any published result so the analysis can be traced back to
exact software builds.
