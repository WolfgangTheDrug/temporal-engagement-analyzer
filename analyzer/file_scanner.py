import os
import re
from typing import List

class FileScanner:
    FOLDER_PATTERN = re.compile(r"^\d{2}.*")

    def __init__(self, root_path: str):
        self.root_path = root_path

    def get_json_files(self) -> List[str]:
        json_files = []

        for entry in os.scandir(self.root_path):
            if entry.is_dir() and self.FOLDER_PATTERN.match(entry.name):
                json_files.extend(self._get_json_files_from_dir(entry.path))

        return json_files

    def _get_json_files_from_dir(self, directory: str) -> List[str]:
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(".json")
        ]