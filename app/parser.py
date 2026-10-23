
import pymupdf
import re
from pathlib import Path


def parse_pdf(pdf_path: str) -> list[dict]:
    """Extract text from each PDF page."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            pages.append({
                "page": page_number,
                "text": page.get_text("text").strip()
            })

    return pages


def extract_sections(pages: list[dict]) -> list[dict]:
    """Extract numbered headings while keeping section content."""

    sections = []
    current_section = None

    # Match headings like "1 Device Overview" and "1.1 Intended Use".
    heading_pattern = re.compile(
        r"^\s*(\d+(?:\.\d+)*\.?)\s+([A-Za-z][A-Za-z0-9 ,&()/–—-]*?)\s*$"
    )

    ignored_starts = (
        "normal:",
        "elevated:",
        "hypertension",
        "hypertensive"
    )

    for page in pages:
        for line in page["text"].splitlines():
            line = line.strip()

            if not line:
                continue

            match = heading_pattern.match(line)

            if match:
                number = match.group(1).rstrip(".")
                title = match.group(2).strip()

                if title.lower().startswith(ignored_starts):
                    if current_section:
                        current_section["text"] += line + " "
                    continue

                current_section = {
                    "section_number": number,
                    "title": title,
                    "page": page["page"],
                    "text": ""
                }

                sections.append(current_section)

            elif current_section:
                current_section["text"] += line + " "

    return sections


if __name__ == "__main__":
    pdf_files = [
        "data/ct200_manual.pdf",
        "data/ct200_manual_v2.pdf"
    ]

    for pdf_file in pdf_files:
        print("\n" + "=" * 50)
        print("FILE:", pdf_file)

        try:
            pages = parse_pdf(pdf_file)
            sections = extract_sections(pages)

            print("Pages:", len(pages))
            print("Sections found:", len(sections))

            for section in sections:
                print(
                    section["section_number"],
                    section["title"]
                )

        except (FileNotFoundError, pymupdf.FileDataError) as error:
            print("Error:", error)
