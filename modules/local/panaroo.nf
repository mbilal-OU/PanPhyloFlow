process PANAROO {
    label 'pangenome'

    conda 'bioconda::panaroo=1.8.0 bioconda::mafft'

    publishDir "${params.outdir}/02_pangenome", mode: 'copy', overwrite: true

    input:
    path gffs

    output:
    path 'panaroo', emit: results

    script:
    def gff_args = gffs.collect { it.toString() }.join(' ')
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
    """

    stub:
    """
    mkdir -p panaroo
    touch panaroo/gene_presence_absence_roary.csv
    touch panaroo/core_gene_alignment.aln
    touch panaroo/core_gene_alignment_filtered.aln
    """
}
