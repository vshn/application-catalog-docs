import os
import shutil

destination_directory = "docs/modules/ROOT/pages/service"

# Current directory is a directory where a cookiecutter template was rendered
current_directory = os.getcwd()

# copytree copies all the contents from current and all nested directories
# from source folder to a destination folder.
shutil.copytree(
    current_directory,
    f"{os.path.dirname(current_directory)}/{destination_directory}",
    dirs_exist_ok=True,
)

# After copying the files we can remove the source directory
shutil.rmtree(current_directory)
