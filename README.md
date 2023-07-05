# webp_converter

Convert all image files (or just a single file), in a directory and its subdirectories, to .webp format, which is 25-34%
smaller than .jpg and .png files<sup>[1](#footnote1)</sup>.

## Usage

```bash
main.py [-h] [--delete-original]
      [--source-code-dir SOURCE_CODE_DIR]
      path
```

### Example

```bash
webp_converter ~/Pictures --delete-original --source-code-dir ~/Documents/Projects
```

## Requirements

- Python 3.6+
- Pillow~=9.5.0

## Installation

### If on Linux

Option 1: Download from GitHub Releases

```bash
wget https://github.com/BeauTheBeau/webp_converter/releases/download/v1.0.0/webp_converter-v1.0.0
chmod +x webp_converter-v1.0.0
sudo mv webp_converter-v1.0.0 /usr/local/bin/webp_converter
```

Option 2: Clone the repository

```bash
git clone
cd webp_converter
sudo ln -s $(pwd)/webp_converter.py /usr/local/bin/webp_converter 
```

### If on Windows or macOS

We don't currently have executables for Windows or macOS, but you can still use the script by cloning the repository and
running it with Python. Refer to the [Requirements](#requirements) section for information on what you need to install.

```bash 
git clone https://github.com/BeauTheBeau/webp_converter.git
cd webp_converter
python3 webp_converter.py -h
```


## What's next?

- [X] Automatically replace references to the original image files in code
    - [ ] Allow the user to exclude/include certain file extensions
    - [ ] Allow the user to exclude/include certain directories
    - [ ] Allow the user to exclude/include certain files
    - [ ] Allow the user to use RegEx for all of the above
        - [ ] Complete with validation!

- [ ] Add support for converting to other image formats
    - [ ] .png
    - [ ] .jpg
    - [ ] .jpeg
    - [ ] .gif

## License

[MIT](https://choosealicense.com/licenses/mit/)

View licence in [LICENCE](LICENSE).

## Footnotes

<a id="footnote1" name="footnote1">1</a>: [Google Developers - WebP](https://developers.google.com/speed/webp)


