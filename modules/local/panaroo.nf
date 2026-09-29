process PANAROO {
    label 'pangenome'

    conda 'bioconda::panaroo=1.8.0 bioconda::mafft=7.*'

    publishDir "${params.outdir}/02_pangenome", mode: 'copy', overwrite: true

    input:
    path gffs

    output:
    path 'panaroo', emit: results
    path 'versions.yml', emit: versions

    script:
    // Quote each GFF path: sample IDs cannot contain spaces today, but the
    // engine must not depend on that remaining true forever.
    def gff_args = gffs.collect { "\"${it.toString()}\"" }.join(' ')
    """
    mkdir -p panaroo

    panaroo \
        -i ${gff_args} \
        -o panaroo \
        --clean-mode ${params.panaroo_clean_mode} \
        --remove-invalid-genes \
        --alignment core \
        --aligner mafft \
        --core_threshold ${params.core_threshold} \
        --family_threshold ${params.panaroo_family_threshold} \
        --threads ${task.cpus}

    panaroo_version=\$(panaroo --version 2>/dev/null | head -n 1 || echo "unknown")
    mafft_version=\$(mafft --version 2>/dev/null | head -n 1 || echo "unknown")
    printf '"PANAROO":\n    panaroo: "%s"\n    mafft: "%s"\n' "\${panaroo_version}" "\${mafft_version}" > versions.yml
    """

    stub:
    """
    mkdir -p panaroo
    touch panaroo/gene_presence_absence_roary.csv
    touch panaroo/core_gene_alignment.aln
    touch panaroo/core_gene_alignment_filtered.aln
    printf '"PANAROO":\n    panaroo: "stub"\n    mafft: "stub"\n' > versions.yml
    """
}
