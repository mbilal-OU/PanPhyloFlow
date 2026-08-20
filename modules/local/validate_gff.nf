process VALIDATE_GFF {
    tag "$sample"
    label 'annotation'

    conda 'conda-forge::python=3.12'

    publishDir "${params.outdir}/00_input_validation", mode: 'copy', overwrite: true, pattern: '*_validation.tsv'

    input:
    tuple val(sample), path(gff)

    output:
    path "${sample}.gff", emit: gff
    path "${sample}_validation.tsv", emit: validation

    script:
    """
    python ${projectDir}/bin/validate_gff.py \
        --input "${gff}" \
        --output "${sample}.gff" \
        --summary "${sample}_validation.tsv"
    """

    stub:
    """
    cp "${gff}" "${sample}.gff"
    printf 'metric\tvalue\nstatus\tstub\n' > "${sample}_validation.tsv"
    """
}
