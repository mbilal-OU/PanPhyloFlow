process NORMALIZE_GFF {
    tag "$sample"

    input:
    tuple val(sample), path(gff)

    output:
    path "${sample}.gff", emit: gff

    script:
    """
    cp "${gff}" "${sample}.gff"
    """

    stub:
    """
    cp "${gff}" "${sample}.gff"
    """
}
