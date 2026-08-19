process BUILD_REPORT {
    label 'reporting'

    conda 'conda-forge::python=3.12'

    publishDir "${params.outdir}/05_report", mode: 'copy', overwrite: true

    input:
    path summary_dir
    path tree_dir
    val engine
    val core_threshold

    output:
    path 'index.html', emit: index
    path 'figures', emit: figures
    path '*.tsv', emit: tables
    path '*.treefile', optional: true, emit: treefile
    path 'INTERPRETATION_NOTES.txt', emit: notes

    script:
    """
    python ${projectDir}/bin/build_report.py \
        --summary-dir "${summary_dir}" \
        --tree-dir "${tree_dir}" \
        --engine "${engine}" \
        --core-threshold ${core_threshold} \
        --outdir .
    """

    stub:
    """
    mkdir -p figures
    printf '<!doctype html><html><body><h1>PanPhyloFlow stub report</h1></body></html>\n' > index.html
    printf '(Genome_A:0.1,Genome_B:0.1);\n' > core_genome.treefile
    touch summary.tsv gene_frequency.tsv core_threshold_scan.tsv descriptive_accumulation.tsv
    touch INTERPRETATION_NOTES.txt
    touch figures/stub.png
    """
}
