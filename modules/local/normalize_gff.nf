process NORMALIZE_GFF {
    tag "$sample"

    // NOTE: this stage currently stages user-supplied GFF3 files unchanged so
    // that downstream processes receive uniformly named inputs. It does not
    // yet validate GFF3 structure; GFF validation is tracked separately and a
    // malformed file will fail inside the pangenome engine with its own
    // error. Prefer the FASTA route (Prokka) for guaranteed-compatible input.
    publishDir "${params.outdir}/01_annotation", mode: 'copy', overwrite: true

    input:
    tuple val(sample), path(gff)

    output:
    path "${sample}.gff", emit: gff
    path 'versions.yml', emit: versions

    script:
    """
    cp "${gff}" "${sample}.gff"
    printf '"NORMALIZE_GFF":\n    note: "input staging only; no external tool executed"\n' > versions.yml
    """

    stub:
    """
    cp "${gff}" "${sample}.gff"
    printf '"NORMALIZE_GFF":\n    note: "input staging only; no external tool executed"\n' > versions.yml
    """
}
