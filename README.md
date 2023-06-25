# webp_converter

Convert all image files (or just a single file), in a directory to .webp format. 

## Usage

```bash
# Interactive mode
python3 webp_converter.py

# Non-interactive mode
python3 webp_converter.py <path> <delete original>
```

## Requirements

- Python 3.6+
- Pillow
- InquirerPy (only if using the interactive mode)

## Installation

```bash
git clone https://github.com/beauthebeau/webp-converter.git
cd webp-converter
pip3 install -r requirements.txt
```

## Run webp_converter anywhere

```bash
# Add the following line to your .bashrc or .zshrc
alias webp_converter="python3 <path to webp_converter.py>"
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
View licence in [LICENCE](LICENSE).

