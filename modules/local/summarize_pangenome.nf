process SUMMARIZE_PANGENOME {
    label 'reporting'

    conda 'conda-forge::python=3.12 conda-forge::pandas=2.* conda-forge::numpy=1.* conda-forge::matplotlib=3.*'

    publishDir "${params.outdir}/03_summary", mode: 'copy', overwrite: true

    input:
    path pangenome_dir
    val engine
    val core_threshold

    output:
    path 'summary', emit: summary
    path 'versions.yml', emit: versions

    script:
    """
    python ${projectDir}/bin/summarize_pangenome.py \
        --input-dir "${pangenome_dir}" \
        --engine "${engine}" \
        --core-threshold ${core_threshold} \
        --outdir summary

    script_version=\$(python ${projectDir}/bin/summarize_pangenome.py --version 2>/dev/null || echo "unknown")
    printf '"SUMMARIZE_PANGENOME":\n    summarize_pangenome: "%s"\n' "\${script_version}" > versions.yml
    """

    stub:
    """
    mkdir -p summary/figures
    cat > summary/summary.tsv <<'TSV'
metric	value
engine	${engine}
genomes	2
gene_families	3
core_threshold	${core_threshold}
core_gene_families	2
accessory_gene_families	1
persistent_ge_95pct	2
shell_15_to_lt95pct	1
cloud_lt15pct	0
single_isolate_families	1
core_fraction_of_pangenome	0.6667
TSV
    touch summary/gene_frequency.tsv
    touch summary/core_threshold_scan.tsv
    touch summary/descriptive_accumulation.tsv
    touch summary/INTERPRETATION_NOTES.txt
    touch summary/figures/pangenome_frequency_classes.png
    touch summary/figures/gene_frequency_spectrum.png
    touch summary/figures/core_threshold_sensitivity.png
    touch summary/figures/descriptive_accumulation.png
    printf '"SUMMARIZE_PANGENOME":\n    summarize_pangenome: "stub"\n' > versions.yml
    """
}
