process ROARY {
    label 'pangenome'

    conda 'bioconda::roary=3.13.0 bioconda::mafft=7.*'

    publishDir "${params.outdir}/02_pangenome", mode: 'copy', overwrite: true

    input:
    path gffs

    output:
    path 'roary', emit: results
    path 'versions.yml', emit: versions

    script:
    // Quote each GFF path: sample IDs cannot contain spaces today, but the
    // engine must not depend on that remaining true forever.
    def gff_args = gffs.collect { "\"${it.toString()}\"" }.join(' ')
    def core_percent = Math.round(params.core_threshold * 100) as int
    """
    roary \
        -f roary \
        -e \
        --mafft \
        -p ${task.cpus} \
        -i ${params.roary_identity} \
        -cd ${core_percent} \
        ${gff_args}

    roary_version=\$(roary -v 2>/dev/null | head -n 1 || echo "unknown")
    mafft_version=\$(mafft --version 2>/dev/null | head -n 1 || echo "unknown")
    printf '"ROARY":\n    roary: "%s"\n    mafft: "%s"\n' "\${roary_version}" "\${mafft_version}" > versions.yml
    """

    stub:
    """
    mkdir -p roary
    touch roary/gene_presence_absence.csv
    touch roary/core_gene_alignment.aln
    printf '"ROARY":\n    roary: "stub"\n    mafft: "stub"\n' > versions.yml
    """
}
