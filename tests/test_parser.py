
from app.parser import parse_pdf, extract_sections


def test_parse_pdf_returns_pages():
    pages = parse_pdf("data/ct200_manual.pdf")

    assert len(pages) > 0
    assert "page" in pages[0]
    assert "text" in pages[0]


def test_extract_sections_returns_numbered_sections():
    pages = parse_pdf("data/ct200_manual.pdf")
    sections = extract_sections(pages)

    assert len(sections) > 0

    for section in sections:
        assert "section_number" in section
        assert "title" in section
        assert "text" in section
