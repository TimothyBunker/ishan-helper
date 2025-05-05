#!/usr/bin/env python3
"""Merge all PDFs in a directory into a single PDF."""
import os
import sys

try:
    from PyPDF2 import PdfMerger
except ImportError:
    try:
        from PyPDF2 import PdfFileMerger as PdfMerger
    except ImportError:
        sys.exit("Error: PyPDF2 is required. Install with 'pip install PyPDF2'.")

def merge_pdfs(input_dir, output_file):
    merger = PdfMerger()
    pdf_files = []
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, fname))
    pdf_files.sort()
    if not pdf_files:
        print(f"No PDF files found in directory: {input_dir}")
        sys.exit(1)
    for pdf in pdf_files:
        print(f"Merging {pdf}")
        merger.append(pdf)
    with open(output_file, "wb") as fout:
        merger.write(fout)
    print(f"Created merged PDF: {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Merge all PDFs in a specified directory into one."
    )
    parser.add_argument(
        "-d", "--dir", default="slides",
        help="Directory containing PDF slide files"
    )
    parser.add_argument(
        "-o", "--out", default="all_slides.pdf",
        help="Output merged PDF filename"
    )
    args = parser.parse_args()
    merge_pdfs(args.dir, args.out)

if __name__ == "__main__":
    main()