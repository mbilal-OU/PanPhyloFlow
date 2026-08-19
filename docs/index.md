# Learn microbial pangenomics with PanPhyloFlow

PanPhyloFlow is both a workflow and a learning path. It uses **Roary as the default pangenome engine**, with Panaroo available as an alternative, and connects pangenome reconstruction to core-genome phylogeny and interpretable reporting.

![PanPhyloFlow workflow](assets/panphyloflow_workflow.svg)

## What you will learn

PanPhyloFlow is designed to make the analysis decisions visible rather than treating pangenome reconstruction as a black box. The documentation focuses on four recurring questions:

1. What is biological variation and what is analysis-defined?
2. How do annotation, clustering and prevalence thresholds affect the pangenome?
3. How is the core alignment converted into a phylogeny?
4. Which conclusions are safe, and which require additional validation?

## Learning path

1. [The biological question](01_concepts.md)
2. [Inputs and annotation](02_inputs_annotation.md)
3. [Building the pangenome](03_pangenome.md)
4. [Core versus accessory is a definition](04_core_thresholds.md)
5. [From core genes to a phylogeny](05_phylogeny.md)
6. [Reading the output without overclaiming](06_interpretation.md)
7. [Running the complete workflow](07_running.md)
8. [How the Nextflow workflow is constructed](08_nextflow_anatomy.md)
9. [Scaling and current limits](09_scaling_and_limits.md)
10. [Validation strategy](10_validation.md)

## Mental model

A microbial pangenome is not merely the union of genes in a set of genomes. The observed pangenome depends on the sampled population, genome quality, annotation, homology/orthology inference, clustering parameters and the prevalence thresholds used to define categories.

PanPhyloFlow exposes those decisions so that learners can distinguish biological observations from analysis-defined summaries.

## Input genomes

PanPhyloFlow starts with analysis-ready FASTA genomes or compatible GFF3 annotations. If genome acquisition, deduplication, ANI validation or upstream QC is still required, the separate [PanGenFlow](https://github.com/mbilal-OU/PanGenFlow) repository can be used optionally before PanPhyloFlow.
