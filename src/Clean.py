import json
import shutil
from ctypes import Union
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json

class OrganizeFiles():
    """
    This class is used to organize files in a directory by
    moving files into directories based on extension.
    """
    def __init__(self):

        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extentions = {}
        for dir, ext in ext_dirs.items():
            for ext1 in ext:
                self.extentions[ext1] = dir

    def __call__(self, directory: Union[str, Path]):
        """ Organize files in directory by moving
         them into directories based on extension.
        """

        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory}Directory does not exist.")

        logger.info(f"Organizing files in {directory} ...")
        file_extension = []
        for file in directory.iterdir():

        # check file path is file or directory and ignore directories
            if file.is_dir():
              continue

        # ignore hidden files
            if file.name.startswith('.'):
                continue

        # move files
            file_extension.append(file.suffix)
            if file.suffix not in self.extentions:  # files that are not blong to file_type_des move to other
                DEST_DIR = directory / 'other'
            else:
                DEST_DIR = directory / self.extentions[file.suffix]
            logger.info(f"Moving {file} to {DEST_DIR} ...")
            DEST_DIR.mkdir(exist_ok=True)

            shutil.move(str(file), str(DEST_DIR))

if __name__ == "__main__":
    org_files = OrganizeFiles()
    org_files('/home/farshad/Downloads')
    logger.info('Done!')
