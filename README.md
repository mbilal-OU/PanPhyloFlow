# PanPhyloFlow

[![Python tests](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/python-tests.yml)
[![Nextflow stub test](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/nextflow-stub.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/nextflow-stub.yml)
[![Docs](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/PanPhyloFlow/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**PanPhyloFlow** is a teaching-oriented, reproducible Nextflow workflow for classical microbial gene-family pangenomics and core-genome phylogeny.

Its central principle is simple: **the workflow should automate the analysis without hiding the biological decisions that define the result.**

Documentation site: `https://mbilal-ou.github.io/PanPhyloFlow/`

## Workflow

```text
Genome FASTA or compatible GFF3
        │
        ├── FASTA → Prokka annotation
        │
        ▼
Panaroo (default) or Roary
        │
        ├── gene presence/absence
        ├── core/accessory statistics
        ├── gene-frequency spectrum
        ├── core-prevalence sensitivity
        └── core-gene alignment
        │
        ▼
IQ-TREE 3
        │
        ├── ModelFinder
        ├── UFBoot
        └── SH-aLRT
        │
        ▼
Static HTML report + TSVs + figures + Newick tree
```

For Panaroo, PanPhyloFlow prefers `core_gene_alignment_filtered.aln` for phylogeny when Panaroo produces it, and falls back to `core_gene_alignment.aln` only when the filtered alignment is unavailable.

## Why this project exists

PanPhyloFlow is not intended to replace specialist pangenome packages. It connects them into an inspectable learning workflow and makes several choices explicit:

- annotation consistency;
- pangenome engine;
- clustering/family parameters;
- core prevalence threshold;
- core alignment used for phylogeny;
- phylogenetic support settings;
- cautious interpretation of pangenome size and frequency classes.

The tutorial in `docs/` explains not only *how* to run the workflow, but *what changes biologically when these analytical choices change*.

## Relationship to PanGenFlow

[`mbilal-OU/PanGenFlow`](https://github.com/mbilal-OU/PanGenFlow) is kept as a separate upstream project for genome acquisition, deduplication, ANI validation and quality control. PanPhyloFlow starts from analysis-ready genomes or compatible annotations and performs the downstream pangenome-to-phylogeny workflow.

```text
PanGenFlow (optional upstream preparation)
        ↓
analysis-ready microbial genomes
        ↓
PanPhyloFlow
        ↓
pangenome + phylogeny + report
```

## Current v0.1.0 scope

- Input: genome FASTA or Prokka-compatible GFF3
- Annotation: Prokka 1.15.6 for the FASTA route
- Pangenome: Panaroo 1.8.0 (default) or Roary 3.13.0
- Alignment: engine-generated core alignment; Panaroo filtered alignment preferred when available
- Phylogeny: IQ-TREE 3.1.3 with ModelFinder, UFBoot and SH-aLRT
- Reporting: summary tables, frequency plots, core-threshold sensitivity, descriptive accumulation and static HTML report
- Execution: Nextflow DSL2 with per-process Conda environments
- CI: Python unit tests plus a complete Nextflow `-stub-run` DAG test

### Why Prokka is still present

Prokka is in maintenance/sunset status and its maintainer recommends Bakta for modern annotation. PanPhyloFlow v0.1.0 retains Prokka because both Panaroo and especially the classical Roary workflow have strong compatibility with Prokka-style GFF3. A Bakta route with explicit compatibility validation is planned rather than silently assuming the formats are interchangeable.

## Quick start

### Requirements

- Java compatible with the selected Nextflow release
- Nextflow
- Conda/Miniconda/Miniforge or compatible solver

Check:

```bash
nextflow -version
conda --version
```

### FASTA input

Create `samples.csv`:

```csv
sample,genome
Genome_A,/absolute/path/Genome_A.fna
Genome_B,/absolute/path/Genome_B.fna
Genome_C,/absolute/path/Genome_C.fna
```

Run:

```bash
nextflow run main.nf \
  -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome panaroo \
  --threads 8 \
  --outdir results
```

### Pre-annotated GFF input

```csv
sample,gff
Genome_A,/absolute/path/Genome_A.gff
Genome_B,/absolute/path/Genome_B.gff
Genome_C,/absolute/path/Genome_C.gff
```

```bash
nextflow run main.nf \
  -profile conda \
  --input samples.csv \
  --input_type gff \
  --pangenome panaroo \
  --outdir results
```

For the Roary route, use Roary-compatible GFF3. Prokka-produced GFF3 is the safest v0.1.0 input.

## Test the workflow logic without bioinformatics software

Every process includes a lightweight stub. This checks channel wiring, branching and expected outputs without running the real tools:

```bash
nextflow run main.nf \
  -stub-run \
  --input tests/data/stub_samples.csv \
  --input_type fasta \
  --pangenome panaroo \
  --outdir stub_results
```

The same test is run automatically in GitHub Actions.

## Report output

Every real or stub workflow run generates a self-contained report directory under `05_report/`. The report builder is also tested automatically by the Python test suite. Generated report assets are intentionally not version-controlled.

## Key parameters

| Parameter | Default | Meaning |
|---|---:|---|
| `--pangenome` | `panaroo` | `panaroo` or `roary` |
| `--core_threshold` | `0.95` | Fraction of genomes required for a family to be treated as core |
| `--panaroo_clean_mode` | `strict` | Panaroo graph-cleaning mode |
| `--panaroo_family_threshold` | `0.70` | Panaroo protein-family identity threshold; not equivalent to Roary `-i` |
| `--roary_identity` | `95` | Roary minimum BLASTP percentage identity |
| `--threads` | `4` | CPUs per computational process |
| `--ufboot` | `1000` | IQ-TREE ultrafast-bootstrap replicates |
| `--sh_alrt` | `1000` | IQ-TREE SH-aLRT replicates |

Sample IDs may contain letters, numbers, `.`, `_` and `-`, and must start with a letter or number. Duplicate sample IDs are rejected.

## Results

```text
results/
├── 01_annotation/
├── 02_pangenome/
│   └── panaroo/ or roary/
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

## Scientific guardrails

PanPhyloFlow deliberately does **not** label a pangenome open or closed from a single accumulation trajectory. The default accumulation output is descriptive and uses one seeded genome order. Formal openness modelling should be performed as a separate, explicitly parameterized analysis with appropriate resampling and sampling assumptions.

Likewise, `core_threshold_sensitivity.png` changes only the prevalence definition of a core family. It does not rerun gene-family clustering at different sequence-identity thresholds.

Core-genome phylogeny is also not assumed to represent accessory-gene evolutionary history, and the Roary route does not automatically correct the core alignment for homologous recombination.

## Tutorial

Start at [`docs/index.md`](docs/index.md). The learning path covers:

1. biological scope;
2. input genomes and annotation;
3. pangenome construction;
4. core/accessory definitions;
5. core-genome phylogeny;
6. interpretation and failure modes;
7. running and resuming the workflow;
8. how the Nextflow DAG works;
9. scaling and current limitations.

## Development status

**v0.1.0 is a pre-release MVP.** Python analysis/report components are unit-tested and the workflow includes a complete stub-run test. A real end-to-end validation with the pinned Conda bioinformatics stack remains a release gate before declaring the workflow stable.

See [`ROADMAP.md`](ROADMAP.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). Users should also cite the underlying software actually used in an analysis; see [`REFERENCES.md`](REFERENCES.md).

## License

MIT. See [`LICENSE`](LICENSE).
