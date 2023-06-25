import os
import sys
from pathlib import Path
from PIL import Image


def to_webp(source, is_directory, delete_original):

    if is_directory:
        for file in source.iterdir():
            to_webp(file, file.is_dir(), delete_original)
        return

    elif source.suffix == ".webp":
        return

    elif source.suffix not in [".jpg", ".jpeg", ".png"]:
        print(f"Skipping {source.name} because it is not a jpg, jpeg, or png file")

    else:
        print(f"Converting {source.name} to webp")
        image = Image.open(source)
        image.save(source.with_suffix(".webp"))

        print("Conversion complete")
        print("Size before conversion: ", str(source.stat().st_size / 1000),  "KB")
        print("Size after conversion:", source.with_suffix(".webp").stat().st_size / 1000, "KB")
        print("Space saved: %.2f%%" % (100 - (source.with_suffix(".webp").stat().st_size / source.stat().st_size * 100)))
        print()

        if delete_original:
            print(f"Deleting {source.name}")
            source.unlink()

    return


def ask_questions():
    from InquirerPy import inquirer

    print("Select a file or directory")
    print("If you select a directory, all files in the directory will be converted to webp")

    path = inquirer.filepath(
        message="Select a file or directory",
        only_files=False,
        invalid_message="Please select a valid file",
        transformer=lambda result: result if not result else Path(result).name,
    ).execute()

    delete_original = inquirer.confirm(
        message="Delete original files?",
        default=False,
    ).execute()

    return [path, delete_original]


def main():
    if len(sys.argv) == 1:
        path, delete_original = ask_questions()
    elif len(sys.argv) == 2:
        path = sys.argv[1]
        delete_original = False
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        delete_original = sys.argv[2] == "True"
    else:
        print("Too many arguments")
        return

    to_webp(Path(path), Path(path).is_dir(), delete_original)
    print("Done")


if __name__ == '__main__':
    main()
