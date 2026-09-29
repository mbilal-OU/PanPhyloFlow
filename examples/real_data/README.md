# Real-data validation cohort

This directory documents the bacterial genome cohort used for PanPhyloFlow's
real-data release-gate validation (GitHub issue #2).

- `accessions.tsv` — six RefSeq **Complete Genome** *Escherichia coli*
  assemblies (K-12 MG1655, K-12 W3110, Sakai O157:H7, UTI89, ED1a, CFT073),
  downloaded 2026-09-28 via NCBI `datasets` CLI v18.38.0. Columns: sample,
  accession, assembly name, strain, file name, size (bp), contig count,
  download date, source.

To reproduce the validation cohort, download the accessions with the NCBI
datasets CLI and build a samplesheet:

```bash
datasets download genome accession --inputfile accessions.txt --include genome
```

then point `--input` at a `sample,genome` CSV of the extracted FASTAs.

## Validation outcome (2026-09-28/29)

Both required routes ran end-to-end on this cohort with no repository edits:

- **Roary route** (FASTA → Prokka 1.15.6 → Roary 3.13.0 → summary →
  IQ-TREE 3.1.3 → HTML report): 3233 core gene families (summary count matches
  Roary's own `summary_statistics.txt` exactly), 8570 total families; core
  alignment 19 MB; IQ-TREE `-m MFP -B 1000 --alrt 1000`; tree recovers K-12
  monophyly at 100/100 ultrafast-bootstrap / 100 SH-aLRT, Sakai sister at
  100/100.
- **Panaroo route** (same cohort, Panaroo 1.8.0): 3365 core families, 7902
  total; the filtered core alignment (`core_gene_alignment_filtered.aln`,
  non-empty) was selected for phylogeny as designed; tree agrees with the
  Roary tree on K-12 monophyly and Sakai placement.

Nextflow 26.04.6 / Temurin JRE 17 on Linux; reduced process resources
(validation VM had 2 CPUs / 7.7 GB RAM). Full per-task metrics are in the
run's `execution_trace.tsv`; this summary is descriptive, not a benchmark.
