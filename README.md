# Adobe Hackathon 2025 – Round 1A

## Overview

This is my submission for Round 1A of the Adobe Hackathon. The goal was to extract a structured outline from a PDF file, including the document title and headings like H1, H2, and H3 along with their page numbers.

I used `PyMuPDF` (fitz) to parse the PDF and built a simple logic to identify headings based on font size and position. The final output is a JSON file in the required format.

---

## How It Works

- Reads all PDF files from the `/app/input` folder
- Processes each page to find text blocks and extract headings
- Assigns heading levels (H1, H2, H3) based on average font size
- Saves the result as a JSON file in the `/app/output` folder

---

## Heading Level Logic

Here's how I determine the heading levels based on font size:
- Font size > 17 → H1
- Font size between 13–17 → H2
- Font size between 11–13 → H3

Multiline headings are also handled using position and font similarity.

---

## Files

- `extract_outline.py` – the main script that processes PDFs
- `Dockerfile` – sets up everything inside a container
- `requirements.txt` – contains the PyMuPDF dependency

---

## How to Run (using Docker)

1. Place all your PDF files inside the `input` folder.
2. Build the Docker image:

```bash
docker build --platform linux/amd64 -t adobe_extractor:latest .

docker run --rm -v E:/adobe_hackathon/input:/app/input -v E:/adobe_hackathon/output:/app/output --network none adobe_extractor:latest
