# 10. Validation strategy

PanPhyloFlow separates **workflow validation** from **biological validation**.

## What CI currently validates

GitHub Actions checks that:

- the Python summary/report tests pass;
- the complete Nextflow DAG executes in `-stub-run` mode;
- both the Roary and Panaroo branches satisfy the expected process/output contracts;
- the documentation site builds successfully.

These tests are important because they detect broken channel wiring, invalid output declarations, reporting regressions and configuration errors.

## What stub testing cannot prove

Stub mode does not execute Prokka, Roary, Panaroo or IQ-TREE on biological data. It therefore cannot prove that:

- the pinned environments solve correctly on every platform;
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
