# Contributing to PanPhyloFlow

PanPhyloFlow welcomes reproducible bug reports, documentation improvements and scientifically justified workflow changes.

## Before opening a pull request

1. Keep each change focused on one purpose.
2. Run the Python tests with `pytest -q`.
3. Run the Nextflow DAG test with `nextflow run main.nf -stub-run --input tests/data/stub_samples.csv --input_type fasta --pangenome panaroo --outdir stub_results`.
4. Do not change default biological thresholds without explaining the scientific reason and expected effect.
5. Update documentation when a parameter, output file or interpretation changes.

## Scientific changes

Changes involving gene-family clustering, annotation, core definitions, phylogenetic inference or openness modelling should include a primary-method reference or software documentation link and a concise explanation of assumptions.

## Code style

- Keep Nextflow processes narrow and modular.
- Prefer explicit inputs and outputs over hidden filesystem dependencies.
- Keep Python analysis deterministic where practical.
- Do not silently convert or reinterpret biological thresholds between different pangenome engines.

## Reporting bugs

Include the PanPhyloFlow version, Nextflow version, profile, operating system, command used, and the relevant `.nextflow.log` excerpt. Do not upload sensitive or restricted datasets.
