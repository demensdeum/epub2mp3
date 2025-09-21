import gradio as gr
import subprocess
import os
import uuid
import shutil
import glob

ORIGINAL_SCRIPT_NAME = "epub2mp3.py"

def convert_epub(epub_file, artist, album, track, offset, end, parts):
    if not epub_file:
        yield "Error: No file was uploaded.", None
        return

    session_id = str(uuid.uuid4())
    temp_dir = os.path.join("temp_conversions", session_id)
    os.makedirs(temp_dir, exist_ok=True)

    uploaded_epub_path = epub_file.name

    output_filename = f"{os.path.splitext(os.path.basename(uploaded_epub_path))[0]}.mp3"
    output_path = os.path.join(temp_dir, output_filename)

    command = [
        "python",
        ORIGINAL_SCRIPT_NAME,
        uploaded_epub_path,
        output_path
    ]

    if artist:
        command.extend(["--artist", artist])
    if album:
        command.extend(["--album", album])
    if track:
        command.extend(["--track", track])
    if offset is not None:
        command.extend(["--offset", str(int(offset))])
    if parts is not None:
        command.extend(["--parts", str(int(parts))])
    if end is not None:
        command.extend(["--end", str(int(end))])

    log_output = ""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            log_output += line
            yield log_output, None

        process.wait()

        if process.returncode != 0:
            log_output += f"\nError: Script exited with code {process.returncode}"
            yield log_output, None
            raise Exception("Conversion failed. Please check the log for details.")

        generated_files = glob.glob(os.path.join(temp_dir, "*.mp3"))
        if not generated_files:
            log_output += "\nError: No MP3 files were generated."
            yield log_output, None
            raise Exception("No MP3 files were found in the output directory.")

        yield log_output, generated_files

    except FileNotFoundError:
        log_output += f"\nError: The script '{ORIGINAL_SCRIPT_NAME}' was not found. Please ensure it's in the same directory."
        yield log_output, None
    except Exception as e:
        log_output += f"\nError: {e}"
        yield log_output, None
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

inputs = [
    gr.File(label="Upload EPUB File"),
    gr.Textbox(label="Artist", placeholder="e.g., Jane Doe"),
    gr.Textbox(label="Album Title", placeholder="e.g., The Adventures of Alpha"),
    gr.Textbox(label="Track Title", placeholder="e.g., Chapter 1"),
    gr.Number(label="Word Offset", value=0, precision=0),
    gr.Number(label="End Word Offset", value=None, precision=0),
    gr.Number(label="Words per Part", value=4500, placeholder="4500 (approx. 30 mins)", precision=0)
]

outputs = [
    gr.Textbox(label="Conversion Log", lines=10, interactive=False),
    gr.File(label="Download MP3 Audiobook", file_count="multiple")
]

iface = gr.Interface(
    allow_flagging='never',
    fn=convert_epub,
    inputs=inputs,
    outputs=outputs,
    title="EPUB to Audiobook Converter",
    description="Upload an EPUB file and convert it to an MP3 audiobook using your existing Python script. The conversion log will stream below."
)

if __name__ == "__main__":
    iface.launch()
