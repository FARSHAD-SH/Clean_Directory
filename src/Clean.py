import shutil
from pathlib import Path
import json
from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles():
    """
    This class is used to organize files in a directory by
    moving files into directories based on extension.
    """
    def __init__(self, directory) -> None:

        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory}Directory does not exist.")

        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extentions = {}
        for dir, ext in ext_dirs.items():
            for ext1 in ext:
                self.extentions[ext1] = dir

        # print(self.extentions)



    def __call__(self):
        """ Organize files in directory by moving
         them into directories based on extension.
        """
        logger.info(f"Organizing files in {self.directory} ...")

        file_extension = []
        for file in self.directory.iterdir():

        # check file path is file or directory and ignore directories
            if file.is_dir():
              continue

        # ignore hidden files
            if file.name.startswith('.'):
                continue

        # move files
            file_extension.append(file.suffix)
            if file.suffix not in self.extentions:  # files that are not blong to file_type_des move to other
                DEST_DIR = self.directory / 'other'
            else:
                DEST_DIR = self.directory / self.extentions[file.suffix]
            logger.info(f"Moving {file} to {DEST_DIR} ...")
            DEST_DIR.mkdir(exist_ok=True)

            shutil.move(str(file), str(DEST_DIR))


if __name__ == "__main__":
    org_files = OrganizeFiles('/home/farshad/Downloads')
    org_files()
    logger.info('Done!')