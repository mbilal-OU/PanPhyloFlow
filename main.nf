nextflow.enable.dsl=2

include { PROKKA } from './modules/local/prokka'
include { NORMALIZE_GFF } from './modules/local/normalize_gff'
include { PANAROO } from './modules/local/panaroo'
include { ROARY } from './modules/local/roary'
include { SUMMARIZE_PANGENOME } from './modules/local/summarize_pangenome'
include { IQTREE3 } from './modules/local/iqtree3'
include { BUILD_REPORT } from './modules/local/build_report'
include { RECORD_PROVENANCE } from './modules/local/record_provenance'

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
    ch_versions = Channel.empty()

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
        ch_versions = ch_versions.mix(PROKKA.out.versions)
    } else {
        NORMALIZE_GFF(samples_ch)
        gff_ch = NORMALIZE_GFF.out.gff
        ch_versions = ch_versions.mix(NORMALIZE_GFF.out.versions)
    }

    // Sort before the pangenome engine: .collect() preserves task-completion
    // order, which is nondeterministic across runs. Roary/Panaroo receive GFFs
    // in CLI order, so an unstable order changes column order (and therefore
    // checksums) of gene_presence_absence*.csv between identical runs.
    gff_list_ch = gff_ch.toSortedList().map { files ->
        if (files.size() < 2) {
            error "PanPhyloFlow requires at least two genomes"
        }
        files
    }

    if (params.pangenome == 'panaroo') {
        PANAROO(gff_list_ch)
        pangenome_dir_ch = PANAROO.out.results
        ch_versions = ch_versions.mix(PANAROO.out.versions)
    } else {
        ROARY(gff_list_ch)
        pangenome_dir_ch = ROARY.out.results
        ch_versions = ch_versions.mix(ROARY.out.versions)
    }

    SUMMARIZE_PANGENOME(
        pangenome_dir_ch,
        params.pangenome,
        params.core_threshold
    )
    ch_versions = ch_versions.mix(SUMMARIZE_PANGENOME.out.versions)

    IQTREE3(
        pangenome_dir_ch,
        params.pangenome
    )
    ch_versions = ch_versions.mix(IQTREE3.out.versions)

    BUILD_REPORT(
        SUMMARIZE_PANGENOME.out.summary,
        IQTREE3.out.tree,
        params.pangenome,
        params.core_threshold
    )
    ch_versions = ch_versions.mix(BUILD_REPORT.out.versions)

    // Machine-readable run provenance: effective parameters, tool versions,
    // workflow metadata. Written last so it reflects the executed run.
    def params_json = new groovy.json.JsonBuilder(params).toPrettyString()
    RECORD_PROVENANCE(
        ch_versions.collectFile(name: 'collated_versions.yml'),
        params_json
    )
}
