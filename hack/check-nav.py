#!/usr/bin/env python3
import os
import sys

# Define the paths
pages_dir = "docs/modules/ROOT/pages"
nav_file = "docs/modules/ROOT/partials/nav.adoc"
additional_nav_file = "docs/modules/ROOT/partials/nav-adrs.adoc"


def extract_links(nav_path):
    try:
        with open(nav_path, "r") as f:
            nav_content = f.read()
    except FileNotFoundError:
        print(f"Navigation file not found: {nav_path}")
        sys.exit(1)
    links = []
    for line in nav_content.splitlines():
        if "xref:" in line:
            start = line.find("xref:") + len("xref:")
            end = line.find("[")
            if start != -1 and end != -1:
                link = line[start:end].strip()
                links.append(link)
    return links


def main():
    # Get the list of all files in the pages directory
    pages_files = []
    for root, dirs, files in os.walk(pages_dir):
        for file in files:
            if file.endswith(".adoc"):
                relative_path = os.path.relpath(os.path.join(root, file), pages_dir)
                pages_files.append(relative_path)

    # Extract links from both navigation files
    nav_links = extract_links(nav_file)
    nav_links += extract_links(additional_nav_file)

    error_found = False

    # Check for missing files in the navigation
    missing_in_nav = set(pages_files) - set(nav_links)
    if missing_in_nav:
        print("Files missing in navigation:")
        for file in missing_in_nav:
            print(f"  - {file}")
        error_found = True
    else:
        print("All files are included in the navigation.")

    # Check for broken links in the navigation
    broken_links = set(nav_links) - set(pages_files)
    if broken_links:
        print("Broken links in navigation:")
        for link in broken_links:
            print(f"  - {link}")
        error_found = True
    else:
        print("No broken links in the navigation.")

    if error_found:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
