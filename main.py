import argparse
import fileinput
import logging
import re
from pathlib import Path
from PIL import Image


def replace_references(image_path, source_code_dir):
    image_name = image_path.name
    webp_image_name = image_name[:image_name.rfind(".")] + ".webp"

    for file in Path(source_code_dir).rglob("*.*"):
        with fileinput.FileInput(file, inplace=True) as f:
            for line in f:
                replaced_line = re.sub(r"\b" + re.escape(image_name) + r"\b", webp_image_name, line)
                print(replaced_line, end='')


def to_webp(source, is_directory, delete_original, source_code_dir=None):
    if is_directory:
        for file in source.iterdir():
            to_webp(file, file.is_dir(), delete_original)
        return

    elif source.suffix == ".webp":
        return

    elif source.suffix not in [".jpg", ".jpeg", ".png"]:
        logging.warning(f"Skipping {source.name} as it is not a supported image format")

    else:
        logging.info(f"Converting {source.name} to webp format...")
        image = Image.open(source)
        image.save(source.with_suffix(".webp"))

        logging.info("> Conversion successful!")
        logging.info(f"> Size before conversion: {source.stat().st_size / 1000:.2f} KB")
        logging.info(f"> Size after conversion: {source.with_suffix('.webp').stat().st_size / 1000:.2f} KB")
        saved_percentage = 100 - (source.with_suffix('.webp').stat().st_size / source.stat().st_size * 100)
        logging.info(f"> Space saved: {saved_percentage:.2f}%")
        logging.info("")

        if delete_original:
            logging.info(f"> Deleting {source.name}")
            source.unlink()

        if source_code_dir:
            logging.info(f"> Replacing references to {source.name} with webp image path")
            replace_references(source, source_code_dir)
            logging.info("> Replacement complete")
            logging.info("")


def convert_images_to_webp(source, delete_original, source_code_dir=None):
    if source.is_dir():
        for file in source.iterdir():
            to_webp(file, file.is_dir(), delete_original, source_code_dir)
    else:
        to_webp(source, source.is_dir(), delete_original, source_code_dir)


def main():
    parser = argparse.ArgumentParser(description="Convert images to webp format")
    parser.add_argument("path", help="File or directory to convert")
    parser.add_argument(
        "--delete-original", "-d",
        action="store_true",
        help="Delete original files after conversion"
    )
    parser.add_argument(
        "--source-code-dir", "-s",
        help="Directory containing source code files for reference replacement"
    )
    args = parser.parse_args()

    # If --help or -h is passed, print help message and exit
    if args.path in ["--help", "-h"]:
        parser.print_help()
        return

    source_path = Path(args.path)
    if not source_path.exists():
        logging.error("Invalid file or directory path")
        return

    confirmation = input(f"Are you sure you want to convert images in '{source_path.resolve()}' to webp format? [Y/n] ")
    if confirmation.lower() not in ["y", "yes", ""]:
        logging.info("Conversion aborted")
        return

    print()
    logging.info("Converting images to webp format...")
    convert_images_to_webp(source_path, args.delete_original, args.source_code_dir)
    logging.info("Conversion completed successfully")


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s")
    logging.getLogger().setLevel(logging.INFO)
    main()

    print("Done")
