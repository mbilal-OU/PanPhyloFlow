process ROARY {
    label 'pangenome'

    conda 'bioconda::roary=3.13.0 bioconda::mafft'

    publishDir "${params.outdir}/02_pangenome", mode: 'copy', overwrite: true

    input:
    path gffs

    output:
    path 'roary', emit: results

    script:
    def gff_args = gffs.collect { it.toString() }.join(' ')
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
    """

    stub:
    """
    mkdir -p roary
    touch roary/gene_presence_absence.csv
    touch roary/core_gene_alignment.aln
    """
}
