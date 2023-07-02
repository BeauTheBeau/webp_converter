import argparse
import logging
from pathlib import Path
from PIL import Image

total_original_size = 0
total_saved_space = 0
total_converted_files = 0


def to_webp(source, delete_original):
    if source.suffix == ".webp":
        return

    elif source.suffix not in [".jpg", ".jpeg", ".png"]:
        logging.warning(f"Skipping {source.name} because it is not a jpg, jpeg, or png file")

    else:
        logging.info(f"Converting {source.name} to webp")
        image = Image.open(source)
        webp_path = source.with_suffix(".webp")
        image.save(webp_path)

        logging.info("Conversion complete")
        logging.info("Size before conversion: %.2f KB", source.stat().st_size / 1000)
        logging.info("Size after conversion: %.2f KB", webp_path.stat().st_size / 1000)
        logging.info(
            "Space saved: %.2f%%",
            (100 - (webp_path.stat().st_size / source.stat().st_size * 100))
        )

        if delete_original:
            logging.info(f"Deleting {source.name}")
            source.unlink()

        global total_original_size
        global total_saved_space
        global total_converted_files

        total_original_size += source.stat().st_size
        total_saved_space += webp_path.stat().st_size
        total_converted_files += 1

    print()


def convert_images_to_webp(source, delete_original):
    if source.is_dir():
        for file in source.iterdir():
            convert_images_to_webp(file, delete_original)
    else:
        to_webp(source, delete_original)


def main():
    parser = argparse.ArgumentParser(description="Convert images to webp format")
    parser.add_argument("path", help="File or directory to convert")
    parser.add_argument(
        "--delete-original",
        action="store_true",
        help="Delete original files after conversion"
    )
    args = parser.parse_args()

    source_path = Path(args.path)
    if not source_path.exists():
        logging.error("Invalid file or directory path")
        return

    print(f"Are you sure you want to convert images in '{source_path.resolve()}' to webp format?")
    confirmation = input("Type 'yes' to confirm: ")
    if confirmation.lower() != "yes":
        logging.info("Conversion canceled")
        return

    logging.info("Converting images to webp format...")
    convert_images_to_webp(source_path, args.delete_original)
    logging.info("Conversion completed successfully")

    logging.info("Total original size: %.2f KB", total_original_size / 1000)
    logging.info("Total size after conversion: %.2f KB", total_saved_space / 1000)
    logging.info("Total space saved: %.2f%%", (100 - (total_saved_space / total_original_size * 100)))
    logging.info("Total converted files: %d", total_converted_files)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
