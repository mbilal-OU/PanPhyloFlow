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

Pre-annotated files are no longer staged blindly. Before pangenome inference, PanPhyloFlow checks that each file:

- begins with the GFF3 version 3 directive;
- contains at least one CDS feature;
- provides a unique `ID` attribute for each CDS;
- includes an embedded `##FASTA` section with non-empty DNA sequences;
- has no duplicate embedded FASTA identifiers;
- uses feature sequence IDs that are present in the embedded FASTA section.

The validator does not alter gene calls or rewrite biological annotations. A passing file is copied unchanged into the workflow and a small validation summary is written to `00_input_validation/`.

For the current Roary route, Prokka-compatible sequence-bearing GFF3 remains the safest input. Passing the structural validator does not prove that files produced by different annotation pipelines are scientifically comparable. Users should still avoid mixing annotation strategies without a justified validation study.

## Sample identifiers

Sample IDs must be unique and may contain letters, numbers, `.`, `_` and `-`. They must begin with a letter or number. Restricting identifiers avoids ambiguous filenames and shell/path problems in downstream command-line tools.

PanPhyloFlow requires at least two genomes for the software path to execute, although biologically meaningful pangenome analysis generally requires a larger, deliberately sampled collection. A publication analysis should justify its taxonomic scope and sampling design rather than treating the software minimum as a biological recommendation.
