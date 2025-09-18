import sys
import os
import argparse
from epub2txt import epub2txt
import pyttsx3
import subprocess
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB

def convert_text_to_mp3(text, path, artist, album_title, track_title):
    temp_wav_path = path.replace('.mp3', '_temp.wav')

    print(f"Synthesizing audio to '{temp_wav_path}'...")
    engine = pyttsx3.init()
    engine.save_to_file(text, temp_wav_path)
    engine.runAndWait()
    print(f"Successfully saved intermediate WAV: '{temp_wav_path}'")


    print(f"Converting '{temp_wav_path}' to MP3 at '{path}'...")
    command = [
        "ffmpeg",
        '-i', temp_wav_path,      # Input file
        '-acodec', 'libmp3lame',  # Use the LAME MP3 encoder for high compatibility
        '-b:a', '192k',          # Set audio bitrate to 192 kbps
        '-y',                    # Overwrite output file if it exists
        path                     # Output file path
    ]

    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Conversion successful.")

    os.remove(temp_wav_path)
    print(f"Removed temporary file: '{temp_wav_path}'")

    print(f"Tagging '{path}' with metadata...")
    print(f"  - Artist: {artist}")
    print(f"  - Album: {album_title}")
    print(f"  - Track: {track_title}")

    audio = MP3(path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception as e:
        print(e)

    audio.tags.add(TPE1(encoding=3, text=artist))
    audio.tags.add(TALB(encoding=3, text=album_title))
    audio.tags.add(TIT2(encoding=3, text=track_title))

    audio.save()
    print("Tagging successful.")



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
        if num_parts != 1:
            print(f"\n--- Processing Part {part_num}/{num_parts} ---")
        start_index = i * words_per_part
        end_index = start_index + words_per_part
        if end_index >= total_words:
            end_index = total_words - 1
        chunk_of_words = words[start_index:end_index]
        text_part = " ".join(chunk_of_words)

        if num_parts == 1:
            part_filename = f"{base_path}"
        else:
            part_filename = f"{base_path}_part_{part_num}"

        part_filename = f"{part_filename}{extension}"

        artist = "DemensDeum epub2mp3"
        album_title = os.path.splitext(os.path.basename(base_path))[0]
        track_title = os.path.splitext(os.path.basename(part_filename))[0]

        convert_text_to_mp3(text_part, part_filename, artist, album_title, track_title)

    print("\nAll tasks completed successfully.")

if __name__ == "__main__":
    main()
