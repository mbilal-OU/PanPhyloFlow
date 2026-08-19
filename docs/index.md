# Learn microbial pangenomics with PanPhyloFlow

PanPhyloFlow is both a workflow and a learning path. The goal is to understand what each stage contributes to the final biological interpretation rather than treating pangenome reconstruction as a black box.

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

## Mental model

A microbial pangenome is not merely the union of genes in a set of genomes. The observed pangenome depends on the sampled population, genome quality, annotation, homology/orthology inference, clustering parameters and the prevalence thresholds used to define categories.

PanPhyloFlow exposes those decisions so that learners can see which quantities are biological observations and which are analysis-defined summaries.

## Where genomes can come from

PanPhyloFlow starts with analysis-ready FASTA genomes or compatible GFF3 annotations. If you need an upstream genome-acquisition and quality-control workflow, the separate [PanGenFlow](https://github.com/mbilal-OU/PanGenFlow) project can be used before PanPhyloFlow.
