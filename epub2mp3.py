import sys
from epub2txt import epub2txt
import pyttsx3

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_text.py <path_to_epub_file> <output_mp3_path>")
        sys.exit(1)

    epub_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        print(f"Converting epub to text")
        text_content = epub2txt(epub_path)
        engine = pyttsx3.init()
        print(f"Synthesizing mp3")
        engine.save_to_file(text_content, output_path)
        engine.runAndWait()
        print(f"Successfully converted '{epub_path}' to '{output_path}'")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
