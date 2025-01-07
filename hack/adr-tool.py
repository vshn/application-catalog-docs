#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path

EXCLUDED_FILES = ("index.adoc", "working-with.adoc")


def validate_adr_status(status):
    valid_statuses = [
        "speculative",
        "draft",
        "accepted",
        "rejected",
        "implemented",
        "obsolete",
    ]

    if not status or status.lower() not in valid_statuses:
        return False
    return True


def extract_variables(file_path):
    variables = {}
    try:
        with open(file_path, "r") as f:
            content = f.read()
            pattern = r":(\w+):\s*(.*)"
            matches = re.finditer(pattern, content)
            for match in matches:
                variables[match.group(1)] = match.group(2).strip()

            title_match = re.search(r"^=\s(.+)$", content, re.MULTILINE)
            if title_match:
                variables["title"] = title_match.group(1)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return variables


def generate_index(adr_dir, output_file):
    adr_files = sorted(
        [f for f in Path(adr_dir).glob("*.adoc") if f.name not in EXCLUDED_FILES]
    )

    content = """= ADR Index
:navtitle: ADRs

[cols="3,1,1,1"]
|===
|Title |Status |Date |Updated

"""

    for adr_file in adr_files:
        vars = extract_variables(adr_file)
        filename = Path(adr_file).stem
        if vars:
            status = vars.get("adr_status", "")
            date = vars.get("adr_date", "")
            updated = vars.get("adr_upd_date", "")
            tags = vars.get("adr_tags", "")

            content += f"|xref:adr/{filename}.adoc[]\n\n`{tags}`\n|{status} |{date} |{updated}\n"

    content += "|===\n"

    with open(output_file, "w") as f:
        f.write(content)


def validate_adrs(adr_dir):
    adr_files = sorted(
        [f for f in Path(adr_dir).glob("*.adoc") if f.name not in EXCLUDED_FILES]
    )
    has_errors = False

    for adr_file in adr_files:
        vars = extract_variables(adr_file)
        status = vars.get("adr_status", "")

        if not validate_adr_status(status):
            print(f"Error: Invalid status '{status}' in {adr_file}")
            has_errors = True

    return has_errors


def main():
    parser = argparse.ArgumentParser(description="ADR Index Generator and Validator")
    parser.add_argument(
        "command",
        choices=["generate", "validate"],
        help="Command to execute (generate index or validate ADRs)",
    )
    # Add optional files argument for pre-commit compatibility
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to process (ignored, for pre-commit hook compatibility)",
    )
    args = parser.parse_args()

    base_dir = "docs/modules/ROOT/pages/adr"
    output_file = f"{base_dir}/index.adoc"

    if args.command == "generate":
        generate_index(base_dir, output_file)
        print(f"Generated index at {output_file}")
    elif args.command == "validate":
        has_errors = validate_adrs(base_dir)
        if has_errors:
            sys.exit(1)
        print("All ADR statuses are valid")


if __name__ == "__main__":
    main()
