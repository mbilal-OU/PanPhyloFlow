# 2. Inputs and annotation

PanPhyloFlow accepts either genome FASTA files or pre-annotated GFF3 files.

## FASTA route

For FASTA input, each genome is annotated independently with Prokka. Standardized annotation matters because inconsistent gene calling can look like biological presence/absence variation.

```text
Genome_A.fna ─┐
Genome_B.fna ─┼─> Prokka ─> comparable GFF files
Genome_C.fna ─┘
```

!!! note "Why Prokka in v0.1.0?"
    Prokka is now in maintenance/sunset status and its maintainer recommends Bakta for new annotation workflows. PanPhyloFlow retains Prokka in the first release because Panaroo explicitly supports Prokka-style GFF3 and Roary has long-standing compatibility with Prokka output. A future Bakta route should be added only after its downstream compatibility is tested explicitly.

## GFF route

Use `--input_type gff` when genomes have already been annotated consistently.

For the Roary route, Prokka-compatible GFF is recommended in v0.1.0.

## Sample identifiers

Sample IDs must be unique and may contain letters, numbers, `.`, `_` and `-`. They must begin with a letter or number. Restricting identifiers avoids ambiguous filenames and shell/path problems in downstream command-line tools.

PanPhyloFlow requires at least two genomes, although biologically meaningful pangenome analysis generally requires a larger, deliberately sampled collection.
