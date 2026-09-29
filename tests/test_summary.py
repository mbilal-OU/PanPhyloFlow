"""Tests for bin/summarize_pangenome.py, bin/build_report.py and bin/record_provenance.py.

Covers the happy paths plus the malformed/degenerate inputs that fail
loudly by design (empty tables, missing files, corrupt summaries).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SUMMARIZE = REPO / "bin" / "summarize_pangenome.py"
BUILD_REPORT = REPO / "bin" / "build_report.py"
RECORD_PROVENANCE = REPO / "bin" / "record_provenance.py"
TEST_TABLE = REPO / "tests" / "data" / "gene_presence_absence.csv"


def run_summarize(input_dir: Path, outdir: Path, engine: str = "panaroo",
                  core_threshold: str = "0.95") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SUMMARIZE),
         "--input-dir", str(input_dir),
         "--engine", engine,
         "--core-threshold", core_threshold,
         "--outdir", str(outdir)],
        capture_output=True, text=True,
    )


def stage_table(tmp_path: Path, engine: str) -> Path:
    """Copy the synthetic presence/absence table under the engine's filename."""
    input_dir = tmp_path / engine
    input_dir.mkdir()
    name = "gene_presence_absence.csv" if engine == "roary" else "gene_presence_absence_roary.csv"
    (input_dir / name).write_text(TEST_TABLE.read_text())
    return input_dir


def test_summary_script(tmp_path):
    input_dir = stage_table(tmp_path, "panaroo")
    outdir = tmp_path / "summary"
    result = run_summarize(input_dir, outdir)
    assert result.returncode == 0, result.stderr

    text = (outdir / "summary.tsv").read_text()
    assert "genomes\t4" in text
    assert "gene_families\t5" in text
    assert "core_gene_families\t2" in text
    assert "single_isolate_families\t2" in text
    assert (outdir / "figures" / "gene_frequency_spectrum.png").exists()
    assert (outdir / "core_threshold_scan.tsv").exists()
    assert (outdir / "INTERPRETATION_NOTES.txt").exists()


def test_summary_roary_engine_filename(tmp_path):
    """The roary branch reads gene_presence_absence.csv (no _roary suffix)."""
    input_dir = stage_table(tmp_path, "roary")
    outdir = tmp_path / "summary"
    result = run_summarize(input_dir, outdir, engine="roary")
    assert result.returncode == 0, result.stderr
    text = (outdir / "summary.tsv").read_text()
    assert "engine\troary" in text
    assert "genomes\t4" in text


def test_summary_missing_table_fails(tmp_path):
    input_dir = tmp_path / "empty"
    input_dir.mkdir()
    result = run_summarize(input_dir, tmp_path / "summary")
    assert result.returncode != 0
    assert "Could not find a presence/absence CSV" in result.stderr


def test_summary_empty_csv_fails(tmp_path):
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    (input_dir / "gene_presence_absence_roary.csv").write_text("")
    result = run_summarize(input_dir, tmp_path / "summary")
    assert result.returncode != 0
    assert "empty" in result.stderr.lower()


def test_summary_header_only_csv_fails(tmp_path):
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    (input_dir / "gene_presence_absence_roary.csv").write_text("Gene,Annotation,A\n")
    result = run_summarize(input_dir, tmp_path / "summary")
    assert result.returncode != 0
    assert "no gene families" in result.stderr.lower()


def test_summary_no_sample_columns_fails(tmp_path):
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    (input_dir / "gene_presence_absence_roary.csv").write_text(
        "Gene,Non-unique Gene name,Annotation\ng1,,hypothetical\n"
    )
    result = run_summarize(input_dir, tmp_path / "summary")
    assert result.returncode != 0
    assert "No isolate/sample columns" in result.stderr


def test_summary_core_threshold_boundary(tmp_path):
    """A family present in exactly the threshold fraction counts as core."""
    input_dir = tmp_path / "panaroo"
    input_dir.mkdir()
    (input_dir / "gene_presence_absence_roary.csv").write_text(
        "Gene,Annotation,A,B\ng1,x,a1,b1\ng2,x,a2,\n"
    )
    outdir = tmp_path / "summary"
    result = run_summarize(input_dir, outdir, core_threshold="0.5")
    assert result.returncode == 0, result.stderr
    text = (outdir / "summary.tsv").read_text()
    assert "genomes\t2" in text
    assert "gene_families\t2" in text
    assert "core_gene_families\t2" in text  # 2/2 and 1/2 both >= 0.5


def test_report_builder(tmp_path):
    input_dir = stage_table(tmp_path, "panaroo")
    summary = tmp_path / "summary"
    result = run_summarize(input_dir, summary)
    assert result.returncode == 0, result.stderr

    tree = tmp_path / "tree"
    tree.mkdir()
    (tree / "core_genome.treefile").write_text("(A:0.1,B:0.1,(C:0.05,D:0.05):0.05);\n")

    report = tmp_path / "report"
    completed = subprocess.run(
        [sys.executable, str(BUILD_REPORT),
         "--summary-dir", str(summary),
         "--tree-dir", str(tree),
         "--engine", "panaroo",
         "--core-threshold", "0.95",
         "--outdir", str(report)],
        capture_output=True, text=True, check=True,
    )
    assert completed.returncode == 0

    html = (report / "index.html").read_text()
    assert "PanPhyloFlow" in html
    assert "Core ≥95%" in html
    assert (report / "core_genome.treefile").exists()
    assert (report / "INTERPRETATION_NOTES.txt").exists()


def test_report_malformed_summary_fails(tmp_path):
    summary = tmp_path / "summary"
    (summary / "figures").mkdir(parents=True)
    (summary / "summary.tsv").write_text("this is not a summary table\nno tabs here\n")
    report = tmp_path / "report"
    completed = subprocess.run(
        [sys.executable, str(BUILD_REPORT),
         "--summary-dir", str(summary),
         "--tree-dir", str(summary),
         "--engine", "panaroo",
         "--core-threshold", "0.95",
         "--outdir", str(report)],
        capture_output=True, text=True,
    )
    assert completed.returncode != 0
    assert "summary.tsv" in completed.stderr


def test_scripts_expose_versions():
    for script in (SUMMARIZE, BUILD_REPORT, RECORD_PROVENANCE):
        completed = subprocess.run(
            [sys.executable, str(script), "--version"],
            capture_output=True, text=True,
        )
        assert completed.returncode == 0, script.name
        assert "0.2.0" in completed.stdout, script.name


def test_record_provenance(tmp_path):
    versions = tmp_path / "collated_versions.yml"
    versions.write_text('"PROKKA":\n    prokka: "1.15.6"\n')
    params = tmp_path / "params.json"
    params.write_text(json.dumps({"pangenome": "roary", "core_threshold": 0.95}))

    outdir = tmp_path / "prov"
    completed = subprocess.run(
        [sys.executable, str(RECORD_PROVENANCE),
         "--versions-file", str(versions),
         "--params-file", str(params),
         "--pipeline-version", "0.2.0",
         "--nextflow-version", "24.10.0",
         "--run-name", "test_run",
         "--session-id", "abc123",
         "--commit-id", "deadbee",
         "--command-line", "nextflow run main.nf",
         "--outdir", str(outdir)],
        capture_output=True, text=True,
    )
    assert completed.returncode == 0, completed.stderr

    text = (outdir / "provenance.yml").read_text()
    assert "name: PanPhyloFlow" in text
    assert "version: 0.2.0" in text
    assert "nextflow_version: 24.10.0" in text
    assert "commit_id: deadbee" in text
    assert '"pangenome": "roary"' in text
    assert 'prokka: "1.15.6"' in text
