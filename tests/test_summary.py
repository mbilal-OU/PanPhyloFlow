from pathlib import Path
import subprocess
import sys


def test_summary_script(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    source = repo / "tests" / "data" / "gene_presence_absence.csv"
    (input_dir / "gene_presence_absence_roary.csv").write_text(source.read_text())

    outdir = tmp_path / "summary"
    subprocess.run([
        sys.executable,
        str(repo / "bin" / "summarize_pangenome.py"),
        "--input-dir", str(input_dir),
        "--engine", "panaroo",
        "--core-threshold", "0.95",
        "--outdir", str(outdir),
    ], check=True)

    text = (outdir / "summary.tsv").read_text()
    assert "genomes\t4" in text
    assert "gene_families\t5" in text
    assert "core_gene_families\t2" in text
    assert "single_isolate_families\t2" in text
    assert (outdir / "figures" / "gene_frequency_spectrum.png").exists()
    assert (outdir / "core_threshold_scan.tsv").exists()


def test_report_builder(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    source = repo / "tests" / "data" / "gene_presence_absence.csv"
    (input_dir / "gene_presence_absence_roary.csv").write_text(source.read_text())

    summary = tmp_path / "summary"
    subprocess.run([
        sys.executable,
        str(repo / "bin" / "summarize_pangenome.py"),
        "--input-dir", str(input_dir),
        "--engine", "panaroo",
        "--core-threshold", "0.95",
        "--outdir", str(summary),
    ], check=True)

    tree = tmp_path / "tree"
    tree.mkdir()
    (tree / "core_genome.treefile").write_text("(A:0.1,B:0.1,(C:0.05,D:0.05):0.05);\n")

    report = tmp_path / "report"
    subprocess.run([
        sys.executable,
        str(repo / "bin" / "build_report.py"),
        "--summary-dir", str(summary),
        "--tree-dir", str(tree),
        "--engine", "panaroo",
        "--core-threshold", "0.95",
        "--outdir", str(report),
    ], check=True)

    html = (report / "index.html").read_text()
    assert "PanPhyloFlow" in html
    assert "Core ≥95%" in html
    assert (report / "core_genome.treefile").exists()
