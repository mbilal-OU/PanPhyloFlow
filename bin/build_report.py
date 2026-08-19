#!/usr/bin/env python3
"""Build a compact static HTML report from PanPhyloFlow outputs."""

from __future__ import annotations

import argparse
import html
import shutil
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--summary-dir", required=True)
    p.add_argument("--tree-dir", required=True)
    p.add_argument("--engine", required=True)
    p.add_argument("--core-threshold", type=float, required=True)
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def read_summary(path: Path) -> dict[str, str]:
    result = {}
    lines = path.read_text().splitlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        key, value = line.split("\t", 1)
        result[key] = value
    return result


def fmt_int(value: str) -> str:
    try:
        return f"{int(float(value)):,}"
    except Exception:
        return html.escape(value)


def main():
    args = parse_args()
    summary_dir = Path(args.summary_dir)
    tree_dir = Path(args.tree_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    figures_out = outdir / "figures"
    figures_out.mkdir(exist_ok=True)
    for src in (summary_dir / "figures").glob("*.png"):
        shutil.copy2(src, figures_out / src.name)

    treefile = next(tree_dir.glob("*.treefile"), None)
    if treefile:
        shutil.copy2(treefile, outdir / "core_genome.treefile")

    for extra in ["summary.tsv", "gene_frequency.tsv", "core_threshold_scan.tsv", "descriptive_accumulation.tsv", "INTERPRETATION_NOTES.txt"]:
        src = summary_dir / extra
        if src.exists():
            shutil.copy2(src, outdir / extra)

    s = read_summary(summary_dir / "summary.tsv")
    core_pct = float(args.core_threshold) * 100

    cards = [
        ("Genomes", fmt_int(s.get("genomes", "NA"))),
        ("Gene families", fmt_int(s.get("gene_families", "NA"))),
        (f"Core ≥{core_pct:g}%", fmt_int(s.get("core_gene_families", "NA"))),
        ("Accessory", fmt_int(s.get("accessory_gene_families", "NA"))),
        ("Singleton families", fmt_int(s.get("single_isolate_families", "NA"))),
    ]

    card_html = "".join(
        f'<div class="card"><div class="metric">{html.escape(label)}</div><div class="value">{value}</div></div>'
        for label, value in cards
    )

    tree_section = (
        '<p><a href="core_genome.treefile">Download the maximum-likelihood tree (Newick)</a></p>'
        if treefile else '<p>Tree file not found.</p>'
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PanPhyloFlow report</title>
<style>
:root {{ --ink:#172033; --muted:#5a6578; --line:#dfe4ec; --panel:#f6f8fb; }}
body {{ margin:0; font-family:Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; color:var(--ink); background:white; }}
main {{ max-width:1100px; margin:0 auto; padding:44px 24px 72px; }}
h1 {{ font-size:42px; letter-spacing:-0.03em; margin-bottom:8px; }}
h2 {{ margin-top:44px; border-bottom:1px solid var(--line); padding-bottom:10px; }}
p {{ line-height:1.65; }}
.sub {{ color:var(--muted); margin-top:0; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:14px; margin:28px 0; }}
.card {{ border:1px solid var(--line); border-radius:14px; padding:18px; background:var(--panel); }}
.metric {{ color:var(--muted); font-size:13px; }}
.value {{ font-size:28px; font-weight:700; margin-top:8px; }}
.figure {{ border:1px solid var(--line); border-radius:14px; padding:16px; margin:18px 0; }}
.figure img {{ width:100%; height:auto; display:block; }}
.note {{ padding:16px 18px; border-left:4px solid #7a8799; background:var(--panel); }}
a {{ color:#174ea6; }}
code {{ background:#eef1f5; padding:2px 5px; border-radius:4px; }}
</style>
</head>
<body><main>
<h1>PanPhyloFlow</h1>
<p class="sub">Microbial pangenome and core-phylogeny report · engine: <strong>{html.escape(args.engine)}</strong></p>
<div class="grid">{card_html}</div>

<h2>Frequency structure</h2>
<div class="figure"><img src="figures/pangenome_frequency_classes.png" alt="Pangenome frequency classes"></div>
<div class="figure"><img src="figures/gene_frequency_spectrum.png" alt="Gene-family frequency spectrum"></div>

<h2>Core-definition sensitivity</h2>
<p>This analysis changes the <em>prevalence threshold used to call a family core</em>. It does not rerun sequence clustering at different homology thresholds.</p>
<div class="figure"><img src="figures/core_threshold_sensitivity.png" alt="Core threshold sensitivity"></div>

<h2>Accumulation trajectory</h2>
<p>The curve below is descriptive and uses one reproducible seeded genome order. It is intentionally <strong>not</strong> labelled as an open/closed pangenome test.</p>
<div class="figure"><img src="figures/descriptive_accumulation.png" alt="Descriptive pangenome accumulation"></div>

<h2>Core-genome phylogeny</h2>
<p>IQ-TREE 3 was run on the core-gene alignment with ModelFinder, ultrafast bootstrap support, and SH-aLRT support.</p>
{tree_section}

<h2>Interpretation guardrails</h2>
<div class="note">
<p>Gene-family counts are analysis-dependent. Taxonomic breadth, genome completeness, contamination, annotation consistency, sampling, gene-family clustering, and core-prevalence thresholds can all change the observed pangenome.</p>
<p>Use the report as a reproducible summary of the chosen analysis—not as evidence that the inferred categories are immutable biological properties.</p>
</div>

<h2>Files</h2>
<p><a href="summary.tsv">Summary TSV</a> · <a href="gene_frequency.tsv">Gene-frequency table</a> · <a href="core_threshold_scan.tsv">Core-threshold scan</a> · <a href="descriptive_accumulation.tsv">Accumulation data</a></p>
</main></body></html>
"""

    (outdir / "index.html").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
