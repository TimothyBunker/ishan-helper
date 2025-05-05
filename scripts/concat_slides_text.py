#!/usr/bin/env python3
"""Concatenate extracted slide text from the index into a single text file."""
import json
import sys
import os

def concat_text(index_file, output_file):
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        sys.exit(f"Error loading index file '{index_file}': {e}")
    slides = data.get("slides", [])
    if not slides:
        print("No slide data found in index.")
    with open(output_file, "w", encoding="utf-8") as out:
        for slide in slides:
            fname = slide.get("filename", "")
            out.write(f"===== {fname} =====\n\n")
            for page in slide.get("pages", []):
                num = page.get("page_number")
                text = page.get("text", "")
                out.write(f"---- Page {num} ----\n")
                out.write(text + "\n\n")
    print(f"Concatenated text written to {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Concatenate slide text from slide_index.json into one file."
    )
    parser.add_argument(
        "-i", "--index", default="slide_index.json",
        help="Slide index JSON file"
    )
    parser.add_argument(
        "-o", "--out", default="all_slides.txt",
        help="Output text filename"
    )
    args = parser.parse_args()
    concat_text(args.index, args.out)

if __name__ == "__main__":
    main()