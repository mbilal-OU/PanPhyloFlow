#!/usr/bin/env python3
"""Create descriptive microbial pangenome statistics and publication-friendly figures."""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

METADATA_COLUMNS = {
    "Gene",
    "Non-unique Gene name",
    "Annotation",
    "No. isolates",
    "No. sequences",
    "Avg sequences per isolate",
    "Genome Fragment",
    "Order within Fragment",
    "Accessory Fragment",
    "Accessory Order with Fragment",
    "QC",
    "Min group size nuc",
    "Max group size nuc",
    "Avg group size nuc",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True)
    p.add_argument("--engine", choices=["panaroo", "roary"], required=True)
    p.add_argument("--core-threshold", type=float, default=0.95)
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def locate_presence_absence(input_dir: Path, engine: str) -> Path:
    candidates = []
    if engine == "panaroo":
        candidates.extend([
            input_dir / "gene_presence_absence_roary.csv",
            input_dir / "gene_presence_absence.csv",
        ])
    else:
        candidates.append(input_dir / "gene_presence_absence.csv")

    for candidate in candidates:
        if candidate.exists() and candidate.stat().st_size > 0:
            return candidate
    raise FileNotFoundError(
        f"Could not find a presence/absence CSV in {input_dir}. Tried: "
        + ", ".join(str(x.name) for x in candidates)
    )


def presence_matrix(df: pd.DataFrame) -> tuple[list[str], np.ndarray]:
    sample_cols = [c for c in df.columns if c not in METADATA_COLUMNS]
    if not sample_cols:
        raise ValueError("No isolate/sample columns detected in gene_presence_absence CSV")

    block = df[sample_cols].fillna("").astype(str)
    matrix = block.apply(lambda col: col.str.strip().ne("")).to_numpy(dtype=bool)
    return sample_cols, matrix


def write_tsv(path: Path, rows: list[tuple[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["metric", "value"])
        writer.writerows(rows)


def descriptive_accumulation(matrix: np.ndarray, seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One reproducible random ordering; descriptive, not an openness estimator."""
    n_genes, n_genomes = matrix.shape
    order = list(range(n_genomes))
    random.Random(seed).shuffle(order)

    union = np.zeros(n_genes, dtype=bool)
    intersection = np.ones(n_genes, dtype=bool)
    pan = np.zeros(n_genomes, dtype=int)
    core = np.zeros(n_genomes, dtype=int)

    for i, col_idx in enumerate(order):
        col = matrix[:, col_idx]
        union |= col
        intersection &= col
        pan[i] = int(union.sum())
        core[i] = int(intersection.sum())

    return np.arange(1, n_genomes + 1), pan, core


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    figures = outdir / "figures"
    figures.mkdir(exist_ok=True)

    if not 0 < args.core_threshold <= 1:
        raise ValueError("--core-threshold must be >0 and <=1")

    csv_path = locate_presence_absence(input_dir, args.engine)
    df = pd.read_csv(csv_path, low_memory=False)
    sample_cols, matrix = presence_matrix(df)

    n_genomes = len(sample_cols)
    n_families = matrix.shape[0]
    if n_genomes < 1:
        raise ValueError("Presence/absence matrix contains no genomes")
    if n_families < 1:
        raise ValueError("Presence/absence matrix contains no gene families")

    isolates_per_family = matrix.sum(axis=1)
    freq = isolates_per_family / n_genomes

    configured_core = int((freq >= args.core_threshold).sum())
    accessory = int(n_families - configured_core)
    high_frequency = int((freq >= 0.95).sum())
    intermediate_frequency = int(((freq >= 0.15) & (freq < 0.95)).sum())
    rare_frequency = int((freq < 0.15).sum())
    singleton = int((isolates_per_family == 1).sum())

    if configured_core + accessory != n_families:
        raise RuntimeError("Internal count invariant failed: core + accessory != total gene families")
    if high_frequency + intermediate_frequency + rare_frequency != n_families:
        raise RuntimeError("Internal count invariant failed: frequency classes do not sum to total gene families")

    rows = [
        ("engine", args.engine),
        ("genomes", n_genomes),
        ("gene_families", n_families),
        ("core_threshold", args.core_threshold),
        ("core_gene_families", configured_core),
        ("accessory_gene_families", accessory),
        ("high_frequency_ge_95pct", high_frequency),
        ("intermediate_frequency_15_to_lt95pct", intermediate_frequency),
        ("rare_frequency_lt15pct", rare_frequency),
        ("single_isolate_families", singleton),
        ("core_fraction_of_pangenome", configured_core / n_families if n_families else math.nan),
    ]
    write_tsv(outdir / "summary.tsv", rows)

    gene_name = df["Gene"].astype(str) if "Gene" in df.columns else pd.Series([f"cluster_{i+1}" for i in range(n_families)])
    freq_df = pd.DataFrame({
        "gene_family": gene_name,
        "isolates": isolates_per_family,
        "frequency": freq,
    })
    freq_df.to_csv(outdir / "gene_frequency.tsv", sep="\t", index=False)

    scan_thresholds = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 1.00]
    scan = pd.DataFrame({
        "core_threshold": scan_thresholds,
        "core_gene_families": [int((freq >= t).sum()) for t in scan_thresholds],
    })
    scan.to_csv(outdir / "core_threshold_scan.tsv", sep="\t", index=False)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    labels = ["High frequency\n≥95%", "Intermediate\n15–<95%", "Rare\n<15%"]
    values = [high_frequency, intermediate_frequency, rare_frequency]
    bars = ax.bar(labels, values)
    ax.set_ylabel("Gene families")
    ax.set_title("Gene-family frequency classes")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, value, f"{value:,}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(figures / "pangenome_frequency_classes.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.hist(freq * 100, bins=np.arange(0, 102, 2))
    ax.set_xlabel("Genome frequency (%)")
    ax.set_ylabel("Gene families")
    ax.set_title("Gene-family frequency spectrum")
    fig.tight_layout()
    fig.savefig(figures / "gene_frequency_spectrum.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(scan["core_threshold"] * 100, scan["core_gene_families"], marker="o")
    ax.set_xlabel("Core prevalence threshold (%)")
    ax.set_ylabel("Core gene families")
    ax.set_title("Sensitivity to the core-gene prevalence definition")
    fig.tight_layout()
    fig.savefig(figures / "core_threshold_sensitivity.png", dpi=300)
    plt.close(fig)

    x, pan, core = descriptive_accumulation(matrix, seed=42)
    acc = pd.DataFrame({"genomes": x, "pangenome_families": pan, "strict_shared_families": core})
    acc.to_csv(outdir / "descriptive_accumulation.tsv", sep="\t", index=False)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(x, pan, label="Observed pangenome")
    ax.plot(x, core, label="Shared by all genomes added")
    ax.set_xlabel("Genomes added")
    ax.set_ylabel("Gene families")
    ax.set_title("Descriptive accumulation trajectory (seeded genome order)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(figures / "descriptive_accumulation.png", dpi=300)
    plt.close(fig)

    notes = outdir / "INTERPRETATION_NOTES.txt"
    notes.write_text(
        "\n".join([
            "PanPhyloFlow interpretation notes",
            "=================================",
            "",
            "1. 'Core' in summary.tsv means presence in at least the configured --core_threshold fraction of genomes.",
            "2. High/intermediate/rare bins are descriptive frequency classes: >=95%, 15-<95%, and <15%, respectively. They are not statistical pangenome partitions.",
            "3. core_threshold_sensitivity.png changes only the prevalence definition of core genes. It does NOT rerun gene clustering at different sequence-identity thresholds.",
            "4. descriptive_accumulation.png uses one seeded random genome order and must not be used alone to infer whether a pangenome is biologically open or closed.",
            "5. Sampling, genome quality, annotation consistency, taxonomic scope, and clustering parameters can all alter pangenome estimates.",
            "",
        ])
    )


if __name__ == "__main__":
    main()
