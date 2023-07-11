import argparse
import fileinput
import logging
import re
from pathlib import Path
from PIL import Image

target_format = "webp"

def replace_references(image_path, source_code_dir):
    image_name = image_path.name
    webp_image_name = image_name[:image_name.rfind(".")] + "." + target_format

    for file in Path(source_code_dir).rglob("*.*"):
        if file.suffix not in [".html", ".css", ".js", ".ts", ".tsx", ".java", ".kt", ".xml", ".json"]:
            continue

        with fileinput.FileInput(file, inplace=True) as f:

            for line in f:
                replaced_line = re.sub(r"\b" + re.escape(image_name) + r"\b", webp_image_name, line)
                print(replaced_line, end='')


def to_format(source, is_directory, delete_original, source_code_dir=None):
    if is_directory:
        for file in source.iterdir():
            to_format(file, file.is_dir(), delete_original)
        return

    elif source.suffix == f".{target_format}":
        return

    elif source.suffix not in [".jpg", ".jpeg", ".png", ".webp"]:
        logging.warning(f"Skipping {source.name} as it is not a supported image format")

    else:

        logging.info(f"Converting {source.name} to {target_format} format...")
        image = Image.open(source)

        if target_format == "jpeg":
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])  # Paste while using the alpha channel as a mask
                background.save(source.with_suffix(f".{target_format}"), format=target_format, quality=80, optimize=True)
            else:
                image.save(source.with_suffix(f".{target_format}"), format=target_format, quality=80, optimize=True)



        image.save(source.with_suffix(f".{target_format}"), format=target_format)
        logging.info("> Conversion successful!")
        logging.info(f"> Size before conversion: {source.stat().st_size / 1000:.2f} KB")
        logging.info(f"> Size after conversion: {source.with_suffix(f'.{target_format}').stat().st_size / 1000:.2f} KB")
        saved_percentage = 100 - (source.with_suffix(f".{target_format}").stat().st_size / source.stat().st_size * 100)
        logging.info(f"> Space saved: {saved_percentage:.2f}%")
        logging.info("")

        if delete_original:
            logging.info(f"> Deleting {source.name}")
            source.unlink()

        if source_code_dir:
            logging.info(f"> Replacing references to {source.name} with {source.with_suffix(f'.{target_format}').name}...")
            replace_references(source, source_code_dir)
            logging.info("> Replacement complete")
            logging.info("")


def convert_images_to_format(source, delete_original, source_code_dir=None):
    if source.is_dir():
        for file in source.iterdir():
            to_format(file, file.is_dir(), delete_original, source_code_dir)
    else:
        to_format(source, source.is_dir(), delete_original, source_code_dir)


def main():
    parser = argparse.ArgumentParser(description="Mass convert images to a different format")
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
    parser.add_argument(
        "--format", "-f",
        help="The target format, images will be converted to this format",
        choices=["webp", "jpeg", "png"],
        default="webp"
    )

    parser.add_argument(
        "--no-confirm", "-n",
        help="Don't ask for confirmation once the command has been sent",
        action="store_true"
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

    if args.format:
        global target_format
        target_format = args.format

    if not args.no_confirm:
        confirmation = input(f"Are you sure you want to convert images in '{source_path.resolve()}' to the {target_format} format? [Y/n] ")
        if confirmation.lower() not in ["y", "yes", ""]:
            logging.info("Conversion aborted")
            return

    print()
    logging.info("Converting images to webp format...")
    convert_images_to_format(source_path, args.delete_original, args.source_code_dir)
    logging.info("Conversion completed successfully")


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s")
    logging.getLogger().setLevel(logging.INFO)
    main()

    print("Done")
