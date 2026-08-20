#!/usr/bin/env python3
"""Validate Roary/Panaroo-compatible GFF3 input before pangenome inference.

The validator is intentionally conservative. It does not rewrite biological
annotations. It verifies the minimum structural properties expected by the
current PanPhyloFlow GFF route and copies the validated file unchanged.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path

IUPAC_DNA = set("ACGTRYSWKMBDHVN.-?")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--summary", required=True)
    return p.parse_args()


def parse_attributes(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in text.split(";"):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def validate(path: Path) -> dict[str, int]:
    if not path.exists():
        raise ValueError(f"GFF3 file does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"GFF3 file is empty: {path}")

    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()

    first_content = next((x.strip() for x in lines if x.strip()), "")
    if first_content != "##gff-version 3":
        raise ValueError("GFF input must begin with the '##gff-version 3' directive")

    try:
        fasta_index = next(i for i, line in enumerate(lines) if line.strip() == "##FASTA")
    except StopIteration as exc:
        raise ValueError(
            "GFF input must contain an embedded FASTA section ('##FASTA'); "
            "the current Roary/Panaroo route expects sequence-bearing GFF3 input"
        ) from exc

    feature_lines = lines[:fasta_index]
    fasta_lines = lines[fasta_index + 1 :]

    cds_count = 0
    feature_contigs: set[str] = set()
    cds_ids: set[str] = set()

    for line_no, line in enumerate(feature_lines, start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 9:
            raise ValueError(f"Malformed GFF3 feature at line {line_no}: expected 9 columns")
        seqid, _, feature_type, start, end, score, strand, phase, attributes = fields
        feature_contigs.add(seqid)

        try:
            start_i = int(start)
            end_i = int(end)
        except ValueError as exc:
            raise ValueError(f"Invalid coordinates at line {line_no}") from exc
        if start_i < 1 or end_i < start_i:
            raise ValueError(f"Invalid coordinate interval at line {line_no}: {start}-{end}")
        if strand not in {"+", "-", ".", "?"}:
            raise ValueError(f"Invalid strand value at line {line_no}: {strand}")
        if phase not in {"0", "1", "2", "."}:
            raise ValueError(f"Invalid phase value at line {line_no}: {phase}")
        if score != ".":
            try:
                float(score)
            except ValueError as exc:
                raise ValueError(f"Invalid score value at line {line_no}: {score}") from exc

        if feature_type == "CDS":
            cds_count += 1
            attrs = parse_attributes(attributes)
            cds_id = attrs.get("ID")
            if not cds_id:
                raise ValueError(f"CDS feature at line {line_no} is missing a GFF3 ID attribute")
            if cds_id in cds_ids:
                raise ValueError(f"Duplicate CDS ID '{cds_id}' at line {line_no}")
            cds_ids.add(cds_id)

    if cds_count == 0:
        raise ValueError("GFF input contains no CDS features")

    fasta_ids: set[str] = set()
    current_id: str | None = None
    sequence_chunks: list[str] = []
    total_bases = 0

    def finish_record(record_id: str | None, chunks: list[str]) -> int:
        if record_id is None:
            return 0
        sequence = "".join(chunks).replace(" ", "").upper()
        if not sequence:
            raise ValueError(f"Embedded FASTA record '{record_id}' has no sequence")
        invalid = sorted(set(sequence) - IUPAC_DNA)
        if invalid:
            shown = "".join(invalid[:10])
            raise ValueError(f"Embedded FASTA record '{record_id}' contains invalid DNA symbols: {shown}")
        return len(sequence)

    for offset, line in enumerate(fasta_lines, start=fasta_index + 2):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            total_bases += finish_record(current_id, sequence_chunks)
            header = stripped[1:].strip()
            current_id = header.split()[0] if header else ""
            if not current_id:
                raise ValueError(f"Empty FASTA identifier at line {offset}")
            if current_id in fasta_ids:
                raise ValueError(f"Duplicate FASTA identifier '{current_id}' at line {offset}")
            fasta_ids.add(current_id)
            sequence_chunks = []
        else:
            if current_id is None:
                raise ValueError(f"Sequence found before a FASTA header at line {offset}")
            if re.search(r"\s", stripped):
                stripped = re.sub(r"\s+", "", stripped)
            sequence_chunks.append(stripped)

    total_bases += finish_record(current_id, sequence_chunks)

    if not fasta_ids:
        raise ValueError("Embedded FASTA section contains no records")

    missing_contigs = sorted(feature_contigs - fasta_ids)
    if missing_contigs:
        preview = ", ".join(missing_contigs[:5])
        suffix = " ..." if len(missing_contigs) > 5 else ""
        raise ValueError(
            "Feature seqids are missing from the embedded FASTA: " + preview + suffix
        )

    return {
        "cds_features": cds_count,
        "feature_contigs": len(feature_contigs),
        "fasta_records": len(fasta_ids),
        "fasta_bases": total_bases,
    }


def write_summary(path: Path, metrics: dict[str, int]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["metric", "value"])
        writer.writerow(["status", "validated"])
        for key, value in metrics.items():
            writer.writerow([key, value])


def main() -> None:
    args = parse_args()
    src = Path(args.input)
    dst = Path(args.output)
    summary = Path(args.summary)

    metrics = validate(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    write_summary(summary, metrics)


if __name__ == "__main__":
    main()
