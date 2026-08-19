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
    path 'report/*', emit: report

    script:
    """
    python ${projectDir}/bin/build_report.py \
        --summary-dir "${summary_dir}" \
        --tree-dir "${tree_dir}" \
        --engine "${engine}" \
        --core-threshold ${core_threshold} \
        --outdir report
    """

    stub:
    """
    mkdir -p report
    printf '<!doctype html><html><body><h1>PanPhyloFlow stub report</h1></body></html>\n' > report/index.html
    cp "${tree_dir}"/*.treefile report/core_genome.treefile 2>/dev/null || true
    """
}
