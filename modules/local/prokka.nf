process PROKKA {
    tag "$sample"
    label 'annotation'

    conda 'bioconda::prokka=1.15.6'

    publishDir "${params.outdir}/01_annotation", mode: 'copy', overwrite: true

    input:
    tuple val(sample), path(genome)

    output:
    tuple val(sample),
          path("${sample}.gff"),
          path("${sample}.gbk"),
          path("${sample}.faa"),
          path("${sample}.ffn"), emit: annotations
    path 'versions.yml', emit: versions

    script:
    """
    prokka \
        --outdir prokka_out \
        --prefix "${sample}" \
        --cpus ${task.cpus} \
        --force \
        "${genome}"

    cp "prokka_out/${sample}.gff" "${sample}.gff"
    cp "prokka_out/${sample}.gbk" "${sample}.gbk"
    cp "prokka_out/${sample}.faa" "${sample}.faa"
    cp "prokka_out/${sample}.ffn" "${sample}.ffn"

    prokka_version=\$(prokka --version 2>/dev/null | head -n 1 || echo "unknown")
    printf '"PROKKA":\n    prokka: "%s"\n' "\${prokka_version}" > versions.yml
    """

    stub:
    """
    printf '##gff-version 3\n##FASTA\n>${sample}\nATGAAATAG\n' > "${sample}.gff"
    printf 'LOCUS       ${sample}\n' > "${sample}.gbk"
    printf '>${sample}_gene1\nMK\n' > "${sample}.faa"
    printf '>${sample}_gene1\nATGAAA\n' > "${sample}.ffn"
    printf '"PROKKA":\n    prokka: "stub"\n' > versions.yml
    """
}
