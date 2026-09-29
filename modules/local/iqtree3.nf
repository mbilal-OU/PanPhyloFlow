process IQTREE3 {
    label 'phylogeny'

    conda 'bioconda::iqtree=3.1.3'

    publishDir "${params.outdir}/04_phylogeny", mode: 'copy', overwrite: true

    input:
    path pangenome_dir
    val engine

    output:
    path 'tree', emit: tree
    path 'versions.yml', emit: versions

    script:
    """
    alignment="${pangenome_dir}/core_gene_alignment.aln"

    if [ "${engine}" = "panaroo" ] && [ -s "${pangenome_dir}/core_gene_alignment_filtered.aln" ]; then
        alignment="${pangenome_dir}/core_gene_alignment_filtered.aln"
    fi

    if [ ! -s "\$alignment" ]; then
        echo "ERROR: no usable core-gene alignment was produced by ${engine}." >&2
        echo "Check the pangenome output and core threshold before phylogenetic inference." >&2
        exit 1
    fi

    mkdir -p tree

    iqtree3 \
        -s "\$alignment" \
        -m MFP \
        -B ${params.ufboot} \
        --alrt ${params.sh_alrt} \
        -T ${task.cpus} \
        --prefix tree/core_genome

    iqtree_version=\$(iqtree3 --version 2>/dev/null | head -n 1 || echo "unknown")
    printf '"IQTREE3":\n    iqtree: "%s"\n' "\${iqtree_version}" > versions.yml
    """

    stub:
    """
    mkdir -p tree
    printf '(Genome_A:0.1,Genome_B:0.1);\n' > tree/core_genome.treefile
    touch tree/core_genome.iqtree tree/core_genome.log
    printf '"IQTREE3":\n    iqtree: "stub"\n' > versions.yml
    """
}
