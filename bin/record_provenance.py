#!/usr/bin/env python3
"""Write a machine-readable PanPhyloFlow run-provenance record.

Combines per-process tool versions (collated by Nextflow), the effective
pipeline parameters, and workflow metadata into a single provenance.yml.
Written with the standard library only so the reporting environment needs
nothing beyond Python.
"""

from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

__version__ = "0.2.0"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--versions-file", required=True,
                   help="Collated versions.yml produced by ch_versions.collectFile()")
    p.add_argument("--params-file", required=True,
                   help="JSON file with the effective Nextflow params")
    p.add_argument("--pipeline-version", required=True)
    p.add_argument("--nextflow-version", required=True)
    p.add_argument("--run-name", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--commit-id", default="unknown")
    p.add_argument("--command-line", default="")
    p.add_argument("--outdir", required=True)
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p.parse_args()


def indent_block(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else "" for line in text.splitlines())


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    versions_text = Path(args.versions_file).read_text(encoding="utf-8").strip()
    params = json.loads(Path(args.params_file).read_text(encoding="utf-8"))
    params_text = json.dumps(params, indent=2, sort_keys=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # command_line is embedded as a YAML literal block; backslashes are safe
    # there, but a trailing backslash-newline edge is avoided by rstrip.
    document = "\n".join([
        "# PanPhyloFlow run provenance (machine-readable).",
        "# Generated automatically at the end of every workflow run.",
        "pipeline:",
        "  name: PanPhyloFlow",
        f"  version: {args.pipeline_version}",
        "  repository: https://github.com/mbilal-OU/PanPhyloFlow",
        "execution:",
        f"  nextflow_version: {args.nextflow_version}",
        f"  run_name: {args.run_name}",
        f"  session_id: {args.session_id}",
        f"  commit_id: {args.commit_id}",
        f"  timestamp_utc: {timestamp}",
        "  command_line: |",
        indent_block(args.command_line.rstrip(), 4),
        "parameters_json: |",
        indent_block(params_text, 2),
        "software_versions:",
        indent_block(versions_text, 2) if versions_text else "  (none recorded)",
        "",
    ])

    (outdir / "provenance.yml").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
