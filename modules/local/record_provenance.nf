process RECORD_PROVENANCE {
    label 'reporting'

    conda 'conda-forge::python=3.12'

    publishDir "${params.outdir}/provenance", mode: 'copy', overwrite: true

    input:
    path collated_versions
    val params_json

    output:
    path 'provenance.yml', emit: provenance

    script:
    // params_json is written via a quoted heredoc so arbitrary parameter
    // values (paths with spaces, quotes) cannot break shell parsing.
    """
    cat > params.json <<'PANPHYLOFLOW_PARAMS_EOF'
    ${params_json}
    PANPHYLOFLOW_PARAMS_EOF

    python ${projectDir}/bin/record_provenance.py \
        --versions-file "${collated_versions}" \
        --params-file params.json \
        --pipeline-version "${workflow.manifest.version}" \
        --nextflow-version "${workflow.nextflow.version}" \
        --run-name "${workflow.runName}" \
        --session-id "${workflow.sessionId}" \
        --commit-id "${workflow.commitId ?: 'unknown (not a git checkout or commit unavailable)'}" \
        --command-line "${workflow.commandLine ?: ''}" \
        --outdir .
    """

    stub:
    """
    printf 'pipeline:\\n  name: PanPhyloFlow\\n  version: stub\\n' > provenance.yml
    """
}
