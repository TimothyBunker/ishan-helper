#!/usr/bin/env python3
"""
Index a single PDF by extracting text from each page.
Usage:
  python3 scripts/index_pdf.py -p input.pdf -o output_index.json
"""
import sys
import os
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
        description="Index a PDF file by extracting text from each page."
    )
    parser.add_argument(
        "-p", "--pdf", required=True,
        help="Path to the PDF file to index"
    )
    parser.add_argument(
        "-o", "--out", default="pdf_index.json",
        help="Output JSON filename"
    )
    args = parser.parse_args()

    pdf_path = args.pdf
    if not os.path.isfile(pdf_path):
        sys.exit(f"Error: PDF file not found: {pdf_path}")

    # Derive output filename if using default
    if args.out == "pdf_index.json":
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        out_file = f"{base}_index.json"
    else:
        out_file = args.out

    print(f"Processing {pdf_path}...")
    pages = extract_text_from_pdf(pdf_path)
    data = {"slides": [{"filename": os.path.relpath(pdf_path), "pages": pages}]}

    try:
        with open(out_file, "w", encoding="utf-8") as fw:
            json.dump(data, fw, ensure_ascii=False, indent=2)
        print(f"Indexed {len(pages)} page(s). Output written to {out_file}.")
    except Exception as e:
        sys.exit(f"Error writing output file '{out_file}': {e}")

if __name__ == "__main__":
    main()