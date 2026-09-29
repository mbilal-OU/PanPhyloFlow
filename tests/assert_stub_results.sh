#!/usr/bin/env bash
# Shared stub-run assertions for CI: verify the full DAG's output contracts,
# not just that the run finished. Usage: assert_stub_results.sh <outdir>
set -euo pipefail

OUTDIR="${1:?usage: assert_stub_results.sh <outdir>}"
fail() { echo "ASSERT FAILED: $*" >&2; exit 1; }

# All five result stages plus provenance must exist
for stage in 01_annotation 02_pangenome 03_summary 04_phylogeny 05_report provenance; do
    [ -d "$OUTDIR/$stage" ] || fail "missing stage directory $stage"
done

# Report contract
[ -f "$OUTDIR/05_report/index.html" ] || fail "missing 05_report/index.html"
[ -f "$OUTDIR/05_report/INTERPRETATION_NOTES.txt" ] || fail "missing INTERPRETATION_NOTES.txt"
[ -f "$OUTDIR/05_report/core_genome.treefile" ] || fail "missing core_genome.treefile"
grep -q '^(Genome_A:0.1,Genome_B:0.1);' "$OUTDIR/05_report/core_genome.treefile" \
    || fail "unexpected stub treefile content"
[ -f "$OUTDIR/05_report/summary.tsv" ] || fail "missing 05_report/summary.tsv"

# Stub summary values must match the stub contract in summarize_pangenome.nf
grep -q '^genomes[[:space:]]\+2$' "$OUTDIR/05_report/summary.tsv" || fail "stub summary: genomes != 2"
grep -q '^gene_families[[:space:]]\+3$' "$OUTDIR/05_report/summary.tsv" || fail "stub summary: gene_families != 3"
grep -q '^core_gene_families[[:space:]]\+2$' "$OUTDIR/05_report/summary.tsv" || fail "stub summary: core_gene_families != 2"

# Provenance contract: every stubbed process contributes a versions record
[ -f "$OUTDIR/provenance/provenance.yml" ] || fail "missing provenance/provenance.yml"
grep -q 'name: PanPhyloFlow' "$OUTDIR/provenance/provenance.yml" || fail "provenance missing pipeline name"

# Pangenome engine outputs
if [ -d "$OUTDIR/02_pangenome/roary" ]; then
    [ -f "$OUTDIR/02_pangenome/roary/gene_presence_absence.csv" ] || fail "missing roary presence/absence csv"
    [ -f "$OUTDIR/02_pangenome/roary/core_gene_alignment.aln" ] || fail "missing roary core alignment"
elif [ -d "$OUTDIR/02_pangenome/panaroo" ]; then
    [ -f "$OUTDIR/02_pangenome/panaroo/gene_presence_absence_roary.csv" ] || fail "missing panaroo presence/absence csv"
    [ -f "$OUTDIR/02_pangenome/panaroo/core_gene_alignment.aln" ] || fail "missing panaroo core alignment"
else
    fail "no engine output directory under 02_pangenome"
fi

echo "OK: stub assertions passed for $OUTDIR"
