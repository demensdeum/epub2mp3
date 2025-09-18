# EPUB to Audiobook Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple Python command-line tool to convert `.epub` files into `.mp3` audiobooks. 🔊

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [License](#-license)

---

## 🎯 About The Project

This script provides a quick and easy way to turn your e-books into audio files. It uses `epub2txt` to extract the text content from an EPUB file and then leverages `pyttsx3` to synthesize that text into speech, saving it as an MP3 file.

**Built With:**
* [Python](https://www.python.org/)
* [epub2txt](https://pypi.org/project/epub2txt/)
* [pyttsx3](https://pypi.org/project/pyttsx3/)
* [FFmpeg](https://ffmpeg.org/)
* [mutagen](https://pypi.org/project/mutagen/)

---

## 🚀 Getting Started

Follow these steps to get the script running on your local machine.

### **Prerequisites**
You need to have **Python** and **pip** installed. You will also need to install the required Python libraries.

### **Installation**
1.  Clone the repository or download the script to a local directory.
2.  Install the required packages using pip:
    ```sh
    pip install epub2txt pyttsx3 mutagen
    ```
3. Install FFmpeg and add to PATH
---

## 💻 Usage

Run the script from your terminal, providing the path to the input `.epub` file and the desired name for the output `.mp3` file.

**Command:**
```sh
python your_script_name.py <path_to_epub_file> <output_mp3_path>
```

---

**Example:**
The following source code is an **example** command. For full **license** details, please see the `LICENSE` file.
```sh
# This is an example command.
python epub_converter.py "example_book.epub" "example_audiobook.mp3"
```

---

## 📜 License

Distributed under the MIT License. See the `LICENSE` file for more information. This **license** permits reuse, modification, and distribution, making this an open-source **example** of an EPUB converter.
