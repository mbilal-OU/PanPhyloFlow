nextflow.enable.dsl=2

include { PROKKA } from './modules/local/prokka'
include { VALIDATE_GFF } from './modules/local/validate_gff'
include { PANAROO } from './modules/local/panaroo'
include { ROARY } from './modules/local/roary'
include { SUMMARIZE_PANGENOME } from './modules/local/summarize_pangenome'
include { IQTREE3 } from './modules/local/iqtree3'
include { BUILD_REPORT } from './modules/local/build_report'

params.input              = null
params.input_type         = 'fasta'       // fasta | gff
params.outdir             = 'results'
params.pangenome          = 'roary'      // roary | panaroo
params.threads            = 4
params.core_threshold     = 0.95
params.panaroo_clean_mode = 'strict'
params.panaroo_family_threshold = 0.70
params.roary_identity     = 95
params.ufboot             = 1000
params.sh_alrt            = 1000

workflow {
    if (!params.input) {
        error "Missing --input samplesheet.csv"
    }

    if (!(params.input_type in ['fasta', 'gff'])) {
        error "--input_type must be 'fasta' or 'gff'"
    }

    if (!(params.pangenome in ['panaroo', 'roary'])) {
        error "--pangenome must be 'panaroo' or 'roary'"
    }

    if (!(params.panaroo_clean_mode in ['strict', 'moderate', 'sensitive'])) {
        error "--panaroo_clean_mode must be strict, moderate, or sensitive"
    }

    if (!(params.core_threshold > 0 && params.core_threshold <= 1)) {
        error "--core_threshold must be >0 and <=1"
    }

    if (!(params.panaroo_family_threshold > 0 && params.panaroo_family_threshold <= 1)) {
        error "--panaroo_family_threshold must be >0 and <=1"
    }

    if (!(params.roary_identity > 0 && params.roary_identity <= 100)) {
        error "--roary_identity must be >0 and <=100"
    }

    if (params.threads < 1) {
        error "--threads must be >=1"
    }

    if (params.ufboot < 1000 || params.sh_alrt < 1000) {
        error "--ufboot and --sh_alrt must each be >=1000"
    }

    def seen_samples = [] as Set

    samples_ch = Channel
        .fromPath(params.input, checkIfExists: true)
        .splitCsv(header: true)
        .map { row ->
            def sample = row.sample?.toString()?.trim()
            def source = params.input_type == 'fasta' ? row.genome : row.gff
            source = source?.toString()?.trim()

            if (!sample || !source) {
                error "Samplesheet requires columns 'sample,genome' for FASTA input or 'sample,gff' for GFF input"
            }

            if (!(sample ==~ /[A-Za-z0-9][A-Za-z0-9._-]*/)) {
                error "Invalid sample ID '${sample}'. Use only letters, numbers, '.', '_' and '-', and start with a letter or number."
            }

            if (!seen_samples.add(sample)) {
                error "Duplicate sample ID '${sample}' in samplesheet"
            }

            tuple(sample, file(source, checkIfExists: true))
        }

    if (params.input_type == 'fasta') {
        PROKKA(samples_ch)
        gff_ch = PROKKA.out.annotations.map { sample, gff, gbk, faa, ffn -> gff }
    } else {
        VALIDATE_GFF(samples_ch)
        gff_ch = VALIDATE_GFF.out.gff
    }

    gff_list_ch = gff_ch.collect().map { files ->
        if (files.size() < 2) {
            error "PanPhyloFlow requires at least two genomes"
        }
        files
    }

    if (params.pangenome == 'panaroo') {
        PANAROO(gff_list_ch)
        pangenome_dir_ch = PANAROO.out.results
    } else {
        ROARY(gff_list_ch)
        pangenome_dir_ch = ROARY.out.results
    }

    SUMMARIZE_PANGENOME(
        pangenome_dir_ch,
        params.pangenome,
        params.core_threshold
    )

    IQTREE3(
        pangenome_dir_ch,
        params.pangenome
    )

    BUILD_REPORT(
        SUMMARIZE_PANGENOME.out.summary,
        IQTREE3.out.tree,
        params.pangenome,
        params.core_threshold
    )
}
