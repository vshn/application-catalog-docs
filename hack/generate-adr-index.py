#!/usr/bin/python
import re
from pathlib import Path


def extract_variables(file_path):
    variables = {}
    try:
        with open(file_path, "r") as f:
            content = f.read()
            # Extract variables like :variable_name: value
            pattern = r":(\w+):\s*(.*)"
            matches = re.finditer(pattern, content)
            for match in matches:
                variables[match.group(1)] = match.group(2).strip()

            # Extract title (first line starting with '= ')
            title_match = re.search(r"^=\s(.+)$", content, re.MULTILINE)
            if title_match:
                variables["title"] = title_match.group(1)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return variables


def generate_index(adr_dir, output_file):
    # Find all .adoc files
    adr_files = sorted(
        [f for f in Path(adr_dir).glob("*.adoc") if f.name != "index.adoc"]
    )

    # Generate index content
    content = """= ADR Index
:navtitle: ADRs

[cols="1,2,1,1,1,1"]
|===
|Number |Title |Author |Owner |Status |Date

"""

    for adr_file in adr_files:
        vars = extract_variables(adr_file)
        if vars:
            number = adr_file.stem
            title = vars.get("title", "Untitled")
            author = vars.get("adr_author", "")
            owner = vars.get("adr_owner", "")
            status = vars.get("adr_status", "")
            date = vars.get("adr_date", "")

            content += f"|xref:adr/{number}.adoc[{number}] |{title} |{author} |{owner} |{status} |{date}\n"

    content += "|===\n"

    # Write the index file
    with open(output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    base_dir = "docs/modules/ROOT/pages/adr"
    output_file = f"{base_dir}/index.adoc"
    generate_index(base_dir, output_file)
