import os
import shutil

destination_directory = "docs/modules/ROOT/pages/adr"
nav_file = "docs/modules/ROOT/partials/nav-adrs.adoc"

# Current directory is a directory where a cookiecutter template was rendered
current_directory = os.getcwd()

# Extract ADR number from the current directory name
adr_number = os.path.basename(current_directory)

# copytree copies all the contents from current and all nested directories
# from source folder to a destination folder.
shutil.copytree(
    current_directory,
    f"{os.path.dirname(current_directory)}/{destination_directory}",
    dirs_exist_ok=True,
)

# Append xref to nav file
nav_path = f"{os.path.dirname(current_directory)}/{nav_file}"
try:
    with open(nav_path, "a") as f:
        f.write(f"\n** xref:adr/{adr_number}.adoc[]")
except IOError as e:
    print(f"Error appending to nav file: {e}")

# After copying the files we can remove the source directory
shutil.rmtree(current_directory)
