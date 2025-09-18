import sys
import os
import argparse
from epub2txt import epub2txt
import pyttsx3

def convert_text_to_mp3(text, path):
    print(f"Synthesizing audio to '{path}'...")
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, path)
        engine.runAndWait()
        print(f"Successfully saved part: '{path}'")
    except Exception as e:
        print(f"Error during synthesis for '{path}': {e}")


def main():
    WORDS_PER_MINUTE = 150

    parser = argparse.ArgumentParser(
        description="Convert an EPUB file to an MP3 audiobook.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("epub_path", help="Path to the input EPUB file.")
    parser.add_argument("output_path", help="Path for the output MP3 file.\nIf --parts is used, this is the base name for the files (e.g., 'my_book.mp3').")
    parser.add_argument(
        "--parts",
        nargs='?',
        const=4500,
        default=None,
        type=int,
        metavar="WORDS",
        help=f"Split the audiobook into parts. If used without a value, defaults to 4500 words (~30 mins)."
    )

    args = parser.parse_args()

    print(f"Converting '{args.epub_path}' to text...")
    text_content = epub2txt(args.epub_path)
    print("Text extraction successful.")

    words = text_content.split()
    total_words = len(words)
    words_per_part = total_words

    if args.parts is not None:
        words_per_part = args.parts
        if words_per_part <= 0:
            print("Error: The value for --parts must be a positive number.")
            sys.exit(1)

    total_words = len(words)
    num_parts = int(total_words / words_per_part)

    print(f"Text has {total_words} words, splitting into {num_parts} parts of up to {words_per_part} words each.")

    base_path, extension = os.path.splitext(args.output_path)
    if not extension:
        extension = ".mp3"

    for i in range(num_parts):
        part_num = i + 1
        print(f"\n--- Processing Part {part_num}/{num_parts} ---")
        start_index = i * words_per_part
        end_index = start_index + words_per_part
        if end_index >= total_words:
            end_index = total_words - 1
        chunk_of_words = words[start_index:end_index]
        text_part = " ".join(chunk_of_words)

        if num_parts == 1:
            part_filename = f"{base_path}{extension}"
        else:
            part_filename = f"{base_path}_part_{part_num}{extension}"
        convert_text_to_mp3(text_part, part_filename)

    print("\nAll tasks completed successfully.")

if __name__ == "__main__":
    main()
