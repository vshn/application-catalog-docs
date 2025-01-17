import os
import shutil

destination_directory = "docs/modules/ROOT/pages/service"

# Current directory is a directory where a cookiecutter template was rendered
current_directory = os.getcwd()

# Move the entire current directory to the destination directory
shutil.move(
    current_directory, f"{os.path.dirname(current_directory)}/{destination_directory}"
)
