# PanPhyloFlow roadmap

## v0.1 - Foundation

- FASTA/GFF input
- standardized Prokka annotation
- Panaroo and Roary
- core/accessory summaries
- core-prevalence sensitivity
- Panaroo filtered core alignment preference
- core-gene phylogeny with IQ-TREE 3
- HTML report
- introductory tutorial
- CI stub testing

## v0.2 - Publication hardening

No new biological analysis feature should take priority over correctness and reproducibility in this phase.

- fail-fast GFF3 validation for pre-annotated input
- method-neutral frequency terminology
- expanded unit and workflow tests
- real end-to-end validation on accessioned bacterial genomes
- native-output cross-checks for Roary and Panaroo
- machine-readable run provenance and software-version capture
- locked/immutable software environments
- validated Docker and Apptainer/Singularity execution
- validated Slurm execution profile
- clean-run and `-resume` reproducibility tests
- stable test input plus expected output for reviewers

## v0.3 - Comparative analysis

- formal same-input Roary/Panaroo comparison mode
- engine-comparison report
- explicit core-prevalence sensitivity workflow
- separate clustering-parameter sensitivity workflows
- optional Bakta annotation route after compatibility validation
- evaluate PIRATE and PPanGGOLiN only if they add a clearly justified comparison question

## v0.4 - Analysis depth

- accessory gene-content ordination
- tree + presence/absence visualization
- rarefied/resampled pangenome curves
- formal open/closed model module with explicit sampling assumptions
- genome QC summary
- richer biological interpretation helpers without causal overstatement

## v1.0 - Stable publication release

- stable CLI and samplesheet schema
- real end-to-end validated test datasets
- reproducibility benchmark across supported execution profiles
- hosted and verified documentation site
- complete citation/provenance output
- archived software release with DOI
- WorkflowHub registration for the manuscript workflow
- manuscript examples reproducible from public test inputs and expected outputs

The v1.0 tag should not be created merely because the feature list is complete. It should be created only after the publication gate and real-data validation gate are closed.
