import os
import json
import fitz  # PyMuPDF

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = doc.metadata.get("title") or os.path.basename(pdf_path)
    outline = []

    prev_level = None
    prev_text = ""
    prev_page = None
    prev_y = None
    prev_size = None
    threshold_y_diff = 25  # relaxed for multi-line headings

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                full_text = ""
                sizes = []

                for span in line["spans"]:
                    span_text = span["text"].strip()
                    if span_text:
                        full_text += span_text + " "
                        sizes.append(span["size"])

                full_text = full_text.strip()
                if not full_text or len(full_text) < 3:
                    continue

                avg_size = sum(sizes) / len(sizes) if sizes else 0

                # Heuristic heading level
                if avg_size > 17:
                    level = "H1"
                elif 13 < avg_size <= 17:
                    level = "H2"
                elif 11 <= avg_size <= 13:
                    level = "H3"
                else:
                    continue  # not a heading

                y_position = line["bbox"][1]

                # Merge logic
                if (
                    prev_text
                    and level == prev_level
                    and prev_page == page_num
                    and prev_size is not None
                    and abs(y_position - prev_y) < threshold_y_diff
                    and abs(avg_size - prev_size) < 0.5
                ):
                    prev_text += " " + full_text
                    prev_y = y_position
                else:
                    if prev_text:
                        outline.append({
                            "level": prev_level,
                            "text": prev_text.strip(),
                            "page": prev_page + 1
                        })
                    prev_text = full_text
                    prev_level = level
                    prev_page = page_num
                    prev_y = y_position
                    prev_size = avg_size

    # Add final
    if prev_text:
        outline.append({
            "level": prev_level,
            "text": prev_text.strip(),
            "page": prev_page + 1
        })

    return {
        "title": title,
        "outline": outline
    }

def main():
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, file.replace(".pdf", ".json"))

            print(f"Processing {file}...")
            outline_data = extract_outline_from_pdf(pdf_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(outline_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
