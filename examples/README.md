# Examples

The CSV files in this directory are **samplesheet templates**, not runnable
examples: they show the required columns and placeholder paths.

- `samples_fasta.csv` — FASTA input mode (`sample,genome`). Genomes are
  annotated with Prokka before pangenome analysis.
- `samples_gff.csv` — pre-annotated GFF3 input mode (`sample,gff`). Use
  Prokka-style GFF3 for the default Roary route.

Copy one, replace the placeholder paths with absolute paths to your own
genomes, and run:

```bash
nextflow run main.nf -profile conda \
  --input samples_fasta.csv \
  --input_type fasta \
  --outdir results
```

Sample IDs must start with a letter or number and contain only letters,
numbers, `.`, `_` and `-`. At least two genomes are required.
