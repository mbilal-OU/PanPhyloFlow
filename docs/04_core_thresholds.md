# 4. Core versus accessory is a definition

The workflow defaults to:

```text
--core_threshold 0.95
```

This means a gene family is called core when it occurs in at least 95% of analysed genomes.

That is not the same as a strict 100% core.

## Why scan the threshold?

PanPhyloFlow creates `core_threshold_scan.tsv` and a sensitivity plot for thresholds from 50% to 100%.

This answers:

> How dependent is my reported core size on the prevalence definition?

It does **not** answer:

> What happens if I change the gene-family sequence-clustering identity?

The latter requires rerunning the pangenome reconstruction and is intentionally kept separate.
