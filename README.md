# PanPhyloFlow

[![Python tests](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/python-tests.yml)
[![Nextflow stub test](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/nextflow-stub.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/nextflow-stub.yml)
[![Docs](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**PanPhyloFlow** is a reproducible, teaching-oriented Nextflow workflow for classical microbial gene-family pangenomics and core-genome phylogenomics.

**Roary is the default pangenome engine.** Panaroo is available as an alternative route for comparison or graph-aware pangenome reconstruction.

> **Goal:** automate a genome → pangenome → phylogeny analysis without hiding the biological and analytical choices that shape the result.

<p align="center">
  <img src="docs/assets/panphyloflow_workflow.svg" alt="PanPhyloFlow workflow" width="100%">
</p>

Documentation: **https://mbilal-ou.github.io/PanPhyloFlow/**

---

## Background

Microbial pangenome results are not determined by genome sequences alone. Sampling, assembly quality, annotation consistency, gene-family inference, clustering thresholds, core-frequency definitions and phylogenetic choices can all change the apparent architecture of a pangenome.

PanPhyloFlow makes those choices visible. It connects established tools into a modular workflow while keeping intermediate files, parameters and interpretations inspectable.

The project is intended for researchers, students and instructors who want a workflow that is both **runnable** and **explainable**.

## Questions PanPhyloFlow helps you ask

1. **What is the core and accessory gene content of this genome set?**
2. **How sensitive are core-gene counts to the prevalence threshold used to define “core”?**
3. **What evolutionary relationships are recovered from the core-genome alignment?**
4. **How do Roary and Panaroo compare when applied to the same analysis-ready genomes?**
5. **Which conclusions are biological observations, and which depend on analysis settings?**

## Inputs

PanPhyloFlow starts from **analysis-ready microbial genomes or compatible GFF3 annotations**.

| Input mode | Samplesheet columns | What happens |
|---|---|---|
| FASTA | `sample,genome` | genomes are annotated with Prokka, then passed to the pangenome engine |
| GFF3 | `sample,gff` | compatible annotations pass directly to pangenome analysis |

Example FASTA samplesheet:

```csv
sample,genome
Genome_A,/absolute/path/Genome_A.fna
Genome_B,/absolute/path/Genome_B.fna
Genome_C,/absolute/path/Genome_C.fna
```

For the **default Roary route**, Prokka-style GFF3 is the safest v0.1.0 input format.

## Pipeline overview

PanPhyloFlow is implemented as a modular Nextflow DSL2 workflow. Each major stage has defined inputs, outputs and software environments.

| Stage | Tool / logic | Main output |
|---|---|---|
| Annotation | Prokka | standardized GFF3 annotations |
| Pangenome | **Roary (default)** | gene presence/absence matrix + core alignment |
| Alternative pangenome | Panaroo | graph-cleaned pangenome + core alignment |
| Summary | PanPhyloFlow Python utilities | core/accessory statistics, threshold sensitivity, plots |
| Phylogeny | IQ-TREE 3 | model-selected core-genome tree with support values |
| Reporting | PanPhyloFlow report builder | HTML report, tables, figures and Newick tree |

For Panaroo analyses, PanPhyloFlow prefers `core_gene_alignment_filtered.aln` for phylogeny when that file is produced; otherwise it falls back to the standard core alignment.

## Repository structure

```text
PanPhyloFlow/
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── LICENSE
├── ROADMAP.md
├── SECURITY.md
├── bin/                         # summary + report utilities
├── docs/                        # tutorial/documentation site
│   └── assets/                  # workflow artwork and documentation assets
├── examples/                    # example samplesheets
├── modules/local/               # Nextflow process modules
├── tests/                       # unit + stub-test fixtures
├── main.nf                      # workflow orchestration
├── nextflow.config              # defaults, resources and profiles
└── mkdocs.yml                   # documentation site configuration
```

## Quick start

### Requirements

- Nextflow
- Java compatible with your selected Nextflow release
- Conda, Miniforge, Miniconda or a compatible solver

```bash
nextflow -version
conda --version
```

### Run the default Roary workflow

Because Roary is the default, `--pangenome roary` is optional:

```bash
nextflow run main.nf \
  -profile conda \
  --input samples.csv \
  --input_type fasta \
  --threads 8 \
  --outdir results
```

Equivalent explicit command:

```bash
nextflow run main.nf \
  -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome roary \
  --roary_identity 95 \
  --core_threshold 0.95 \
  --threads 8 \
  --outdir results
```

### Use Panaroo instead

```bash
nextflow run main.nf \
  -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome panaroo \
  --panaroo_clean_mode strict \
  --panaroo_family_threshold 0.70 \
  --core_threshold 0.95 \
  --outdir results_panaroo
```

### Resume an interrupted run

```bash
nextflow run main.nf -resume \
  -profile conda \
  --input samples.csv \
  --input_type fasta \
  --outdir results
```

## Key parameters

| Parameter | Default | Meaning |
|---|---:|---|
| `--pangenome` | `roary` | pangenome engine: `roary` or `panaroo` |
| `--roary_identity` | `95` | Roary minimum BLASTP percentage identity (`-i`) |
| `--core_threshold` | `0.95` | fraction of genomes required for a family to be treated as core |
| `--panaroo_clean_mode` | `strict` | Panaroo graph-cleaning mode |
| `--panaroo_family_threshold` | `0.70` | Panaroo family threshold; **not equivalent** to Roary `-i` |
| `--threads` | `4` | CPUs requested per computational process |
| `--ufboot` | `1000` | IQ-TREE ultrafast-bootstrap replicates |
| `--sh_alrt` | `1000` | IQ-TREE SH-aLRT replicates |

Panaroo and Roary thresholds are intentionally exposed separately because they belong to different inference strategies and should not be treated as interchangeable settings.

## Outputs

```text
results/
├── 01_annotation/
├── 02_pangenome/
│   └── roary/ or panaroo/
├── 03_summary/
│   └── summary/
├── 04_phylogeny/
│   └── tree/
├── 05_report/
│   ├── index.html
│   ├── figures/
│   ├── core_genome.treefile
│   └── *.tsv
├── execution_trace.tsv
├── nextflow_report.html
├── timeline.html
└── dag.html
```

The final report is designed to bring the principal statistics, figures and phylogeny into one inspectable output while leaving native Roary/Panaroo files available for downstream analysis.

## Interpretation guardrails

PanPhyloFlow deliberately avoids several common overinterpretations:

- a single descriptive accumulation trajectory is **not** used to declare a pangenome definitively open or closed;
- changing `--core_threshold` changes the **prevalence definition of core**, not the underlying gene-family clustering;
- a core-genome tree is not assumed to represent accessory-gene evolutionary history;
- accessory presence alone is not automatically interpreted as horizontal gene transfer;
- Roary and Panaroo results are not expected to be numerically identical because their inference strategies differ.

## Validation status

**v0.1.0 remains a pre-release.**

Validated so far:

- Python summary/report unit tests pass in GitHub Actions;
- the complete Nextflow DAG passes stub-mode CI for **both Roary and Panaroo**;
- the MkDocs documentation site builds and deploys successfully.

Still required before the first stable release:

- real end-to-end execution with a small, taxonomically coherent bacterial genome set using the pinned bioinformatics environments;
- comparison of generated summary values against native Roary/Panaroo outputs;
- confirmation of tree/report outputs on real data.

See **[validation/release gate issue #2](https://github.com/mbilal-OU/PanPhyloFlow/issues/2)** and [`docs/10_validation.md`](docs/10_validation.md).

## Test workflow wiring without the bioinformatics stack

```bash
nextflow run main.nf \
  -stub-run \
  -profile ci \
  --input tests/data/stub_samples.csv \
  --input_type fasta \
  --outdir stub_results
```

Stub mode validates workflow wiring and output contracts. It is **not** a substitute for biological validation.

## Documentation and learning path

The documentation is structured as a tutorial rather than only a command reference:

1. Biological scope
2. Inputs and annotation
3. Pangenome construction
4. Core-threshold definitions
5. Core-genome phylogeny
6. Interpretation and failure modes
7. Running and resuming
8. Nextflow workflow anatomy
9. Scaling and current limits
10. Validation strategy

Start at [`docs/index.md`](docs/index.md) or visit the documentation site.

## Optional companion: PanGenFlow

**PanGenFlow is not required to use PanPhyloFlow.**

If you still need to **download genomes, deduplicate records, perform ANI-based validation, or carry out upstream genome QC**, the separate [PanGenFlow](https://github.com/mbilal-OU/PanGenFlow) project can be used first. PanPhyloFlow itself begins from analysis-ready genomes or annotations.

## Current scope and roadmap

PanPhyloFlow intentionally starts narrow: classical bacterial pangenome analysis, core-genome phylogeny and interpretation. Planned extensions are tracked in [`ROADMAP.md`](ROADMAP.md), including broader annotation support and additional validation/examples.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). Users should also cite the underlying software used in their analysis; see [`REFERENCES.md`](REFERENCES.md).

## License

MIT. See [`LICENSE`](LICENSE).
