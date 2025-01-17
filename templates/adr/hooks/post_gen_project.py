import os
import shutil
import json
import glob

destination_directory = "docs/modules/ROOT/pages/adr"
nav_file = "docs/modules/ROOT/partials/nav-adrs.adoc"
cookiecutter_json = "templates/adr/cookiecutter.json"

# Current directory is a directory where a cookiecutter template was rendered
current_directory = os.getcwd()

# Extract ADR number from the current directory name
adr_number = os.path.basename(current_directory)


# Find next free ADR number by scanning existing ADR files
def get_next_adr_number():
    adr_files = glob.glob(
        f"{os.path.dirname(current_directory)}/{destination_directory}/[0-9]*.adoc"
    )
    if not adr_files:
        return "0001"
    numbers = [int(os.path.basename(f).split("-")[0]) for f in adr_files]
    return f"{max(numbers) + 1:04d}"


# copytree copies all the contents from current and all nested directories
# from source folder to a destination folder.
shutil.copytree(
    current_directory,
    f"{os.path.dirname(current_directory)}/{destination_directory}",
    dirs_exist_ok=True,
)

# Update cookiecutter.json with next ADR number
next_number = get_next_adr_number()
try:
    json_path = f"{os.path.dirname(current_directory)}/{cookiecutter_json}"
    with open(json_path, "r") as f:
        config = json.load(f)
    config["adr_number"] = next_number
    with open(json_path, "w") as f:
        json.dump(config, f, indent=4)
except IOError as e:
    print(f"Error updating cookiecutter.json: {e}")


# Append xref to nav file
nav_path = f"{os.path.dirname(current_directory)}/{nav_file}"
try:
    with open(nav_path, "a") as f:
        f.write(f"\n** xref:adr/{adr_number}.adoc[]")
except IOError as e:
    print(f"Error appending to nav file: {e}")

# After copying the files we can remove the source directory
shutil.rmtree(current_directory)

print(
    f"====> New ADR document has been created: {destination_directory}/{adr_number}.adoc"
)
