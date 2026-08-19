# 7. Running the complete workflow

## Minimal command — Roary default

```bash
nextflow run main.nf -profile conda \
  --input samples.csv \
  --input_type fasta
```

Roary is the default pangenome engine. You can also state it explicitly with `--pangenome roary`.

## Resume an interrupted run

```bash
nextflow run main.nf -resume -profile conda \
  --input samples.csv \
  --input_type fasta
```

## Set Roary parameters explicitly

```bash
nextflow run main.nf -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome roary \
  --roary_identity 95 \
  --core_threshold 0.95
```

## Compare against Panaroo

```bash
nextflow run main.nf -profile conda \
  --input samples.csv \
  --input_type fasta \
  --pangenome panaroo \
  --panaroo_clean_mode strict \
  --panaroo_family_threshold 0.70 \
  --core_threshold 0.95
```

## Test workflow wiring without the bioinformatics stack

```bash
nextflow run main.nf -stub-run -profile ci \
  --input tests/data/stub_samples.csv \
  --input_type fasta \
  --outdir stub_results
```

Stub mode replaces each heavy command with a minimal dummy command while preserving the same process dependencies and output shapes. It is intended for workflow-development testing, not biological validation.

## Recommended first real test

Start with a small, taxonomically coherent set of well-assembled bacterial genomes. Run the default Roary route first, then run Panaroo on the same samples if you want an engine comparison. Confirm that annotation, pangenome construction, core alignment, phylogeny and report generation all complete before scaling to hundreds or thousands of genomes.
