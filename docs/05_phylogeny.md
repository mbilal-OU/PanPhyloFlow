# 5. From core genes to a phylogeny

Both supported pangenome routes are configured to generate a core-gene alignment.

```text
core-gene alignment
        │
        ▼
    IQ-TREE 3
        │
        ├── ModelFinder
        ├── UFBoot
        └── SH-aLRT
        │
        ▼
core_genome.treefile
```

## Which Panaroo alignment is used?

When Panaroo produces `core_gene_alignment_filtered.aln`, PanPhyloFlow uses that file for IQ-TREE because Panaroo recommends the filtered alignment for core-genome phylogeny. If the filtered file is absent, the workflow falls back to `core_gene_alignment.aln`.

The Roary route uses `core_gene_alignment.aln` generated with `-e --mafft`.

## Interpretation

The resulting tree represents sequence evolution in the aligned core regions. It should not automatically be treated as equivalent to a tree based on accessory gene content.

The current Roary route also does not automatically mask or model homologous recombination. For datasets in which recombination is important, recombination-aware preprocessing should be considered before interpreting the tree as a clonal history.
