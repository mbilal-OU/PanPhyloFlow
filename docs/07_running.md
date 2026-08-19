# 7. Running the complete workflow

## Minimal command

```bash
nextflow run main.nf -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome panaroo
```

## Resume an interrupted run

```bash
nextflow run main.nf -resume -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome panaroo
```

## Compare against Roary

```bash
nextflow run main.nf -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome roary \
  --roary_identity 95 \
  --core_threshold 0.95
```

## Test workflow wiring without the bioinformatics stack

```bash
nextflow run main.nf -stub-run \
  --input tests/data/stub_samples.csv \
  --input_type fasta \
  --pangenome panaroo \
  --outdir stub_results
```

Stub mode replaces each heavy command with a minimal dummy command while preserving the same process dependencies and output shapes. It is intended for workflow-development testing, not biological validation.

## Recommended first real test

Start with a small, taxonomically coherent set of well-assembled bacterial genomes. Confirm that annotation, pangenome construction, core alignment, phylogeny and report generation all complete before scaling to hundreds or thousands of genomes.
