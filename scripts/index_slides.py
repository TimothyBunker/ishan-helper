#!/usr/bin/env python3
"""
Index slide PDFs in a directory by extracting text from each page.
Usage:
  python3 scripts/index_slides.py -d slides -o slide_index.json
"""
import os
import sys
import json

try:
    from PyPDF2 import PdfReader
except ImportError:
    sys.exit("Error: PyPDF2 is required. Install with 'pip install PyPDF2'.")

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        pages = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page_number": i, "text": text})
        return pages
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}", file=sys.stderr)
        return []

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Index slide PDFs by extracting text from each page."
    )
    parser.add_argument(
        "-d", "--dir", default="slides",
        help="Directory containing PDF slide files"
    )
    parser.add_argument(
        "-o", "--out", default="slide_index.json",
        help="Output JSON filename"
    )
    args = parser.parse_args()

    slides = []
    for root, _, files in os.walk(args.dir):
        for fname in files:
            if fname.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, fname)
                print(f"Processing {pdf_path}...")
                pages = extract_text_from_pdf(pdf_path)
                slides.append({
                    "filename": os.path.relpath(pdf_path),
                    "pages": pages
                })
    with open(args.out, "w", encoding="utf-8") as fw:
        json.dump({"slides": slides}, fw, ensure_ascii=False, indent=2)
    print(f"Indexed {len(slides)} PDF(s). Output written to {args.out}.")

if __name__ == "__main__":
    main()