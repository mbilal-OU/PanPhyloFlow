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
    path 'versions.yml', emit: versions

    script:
    """
    python ${projectDir}/bin/build_report.py \
        --summary-dir "${summary_dir}" \
        --tree-dir "${tree_dir}" \
        --engine "${engine}" \
        --core-threshold ${core_threshold} \
        --outdir .

    script_version=\$(python ${projectDir}/bin/build_report.py --version 2>/dev/null || echo "unknown")
    printf '"BUILD_REPORT":\n    build_report: "%s"\n' "\${script_version}" > versions.yml
    """

    stub:
    // The stub still stages the declared inputs, so copy them through: this
    // keeps the stub DAG honest about the SUMMARIZE -> BUILD_REPORT contract
    // instead of fabricating disconnected outputs.
    """
    mkdir -p figures
    cp "${summary_dir}/summary.tsv" summary.tsv
    cp "${summary_dir}/gene_frequency.tsv" gene_frequency.tsv
    cp "${summary_dir}/core_threshold_scan.tsv" core_threshold_scan.tsv
    cp "${summary_dir}/descriptive_accumulation.tsv" descriptive_accumulation.tsv
    cp "${summary_dir}/INTERPRETATION_NOTES.txt" INTERPRETATION_NOTES.txt
    printf '(Genome_A:0.1,Genome_B:0.1);\n' > core_genome.treefile
    touch figures/stub.png
    printf '<!doctype html><html><body><h1>PanPhyloFlow stub report</h1></body></html>\n' > index.html
    printf '"BUILD_REPORT":\n    build_report: "stub"\n' > versions.yml
    """
}
