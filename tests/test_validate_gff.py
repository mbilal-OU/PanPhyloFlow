from pathlib import Path
import subprocess
import sys

import pytest


def run_validator(repo: Path, tmp_path: Path, text: str):
    src = tmp_path / "input.gff"
    dst = tmp_path / "validated.gff"
    summary = tmp_path / "validation.tsv"
    src.write_text(text)
    result = subprocess.run(
        [
            sys.executable,
            str(repo / "bin" / "validate_gff.py"),
            "--input", str(src),
            "--output", str(dst),
            "--summary", str(summary),
        ],
        capture_output=True,
        text=True,
    )
    return result, dst, summary


def valid_gff() -> str:
    return """##gff-version 3
contig1\ttest\tCDS\t1\t9\t.\t+\t0\tID=cds1;product=test
##FASTA
>contig1
ATGAAATAG
"""


def test_valid_gff_is_copied_and_summarized(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    result, dst, summary = run_validator(repo, tmp_path, valid_gff())
    assert result.returncode == 0, result.stderr
    assert dst.read_text() == valid_gff()
    text = summary.read_text()
    assert "status\tvalidated" in text
    assert "cds_features\t1" in text
    assert "fasta_records\t1" in text


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "contig1\ttest\tCDS\t1\t9\t.\t+\t0\tID=cds1\n##FASTA\n>contig1\nATGAAATAG\n",
            "##gff-version 3",
        ),
        (
            "##gff-version 3\ncontig1\ttest\tCDS\t1\t9\t.\t+\t0\tID=cds1\n",
            "##FASTA",
        ),
        (
            "##gff-version 3\ncontig1\ttest\tgene\t1\t9\t.\t+\t.\tID=gene1\n##FASTA\n>contig1\nATGAAATAG\n",
            "no CDS",
        ),
        (
            "##gff-version 3\ncontig1\ttest\tCDS\t1\t9\t.\t+\t0\tproduct=test\n##FASTA\n>contig1\nATGAAATAG\n",
            "missing a GFF3 ID",
        ),
        (
            "##gff-version 3\ncontigX\ttest\tCDS\t1\t9\t.\t+\t0\tID=cds1\n##FASTA\n>contig1\nATGAAATAG\n",
            "missing from the embedded FASTA",
        ),
    ],
)
def test_invalid_gff_fails_fast(tmp_path, text, expected):
    repo = Path(__file__).resolve().parents[1]
    result, dst, summary = run_validator(repo, tmp_path, text)
    assert result.returncode != 0
    assert expected in result.stderr
    assert not dst.exists()
    assert not summary.exists()
