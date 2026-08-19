# 8. How the Nextflow workflow is constructed

PanPhyloFlow uses Nextflow DSL2 so that the workflow logic and the tool-specific processes remain separate.

## Entry workflow

`main.nf` performs four jobs:

1. reads the sample sheet;
2. chooses FASTA or GFF input handling;
3. chooses Panaroo or Roary;
4. connects the pangenome output to summary, phylogeny, and report processes.

## Modules

```text
modules/local/
├── prokka.nf
├── normalize_gff.nf
├── panaroo.nf
├── roary.nf
├── summarize_pangenome.nf
├── iqtree3.nf
└── build_report.nf
```

Each module has a narrow responsibility. That makes it possible to inspect or replace one analytical stage without rewriting the entire pipeline.

## Dataflow idea

```text
samplesheet
   │
   ▼
channel of (sample, genome)
   │
   ▼
PROKKA tasks run independently
   │
   ▼
channel of GFF files
   │
   ▼
collect for cohort-level pangenome analysis
   │
   ├──> summary
   └──> IQ-TREE
             │
             ▼
          report
```

This is why workflow managers are useful: the orchestration expresses dependencies, while each process remains a reproducible command-line analysis.
