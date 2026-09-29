# Smoke-test samples: first 200 kb of two RefSeq *E. coli* K-12 genomes.
#
# - MG1655_first200kb.fna: GCF_000005845.2 (ASM584v2), K-12 substr. MG1655
# - W3110_first200kb.fna:  GCF_000010245.2 (ASM1024v1), K-12 substr. W3110
#
# These are real RefSeq sequence truncated to a 200 kb subset — enough for
# Prokka to annotate and for Roary to build a small pangenome, so the weekly
# CI job exercises the REAL tool stack (not stubs) in minutes. This is a
# regression smoke test, not a biological validation cohort; see
# examples/real_data/ for the full validation cohort and docs/10_validation.md
# for the release-gate results.
