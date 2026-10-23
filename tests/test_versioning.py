
from app.versioning import compare_sections


def test_compare_sections_detects_changes():
    old_sections = [
        {
            "section_number": "1.1",
            "title": "Intended Use",
            "text": "Used for blood pressure measurement."
        },
        {
            "section_number": "2.1",
            "title": "Battery Life",
            "text": "Battery lasts 250 cycles."
        },
        {
            "section_number": "3.1",
            "title": "Old Feature",
            "text": "Old feature description."
        }
    ]

    new_sections = [
        {
            "section_number": "1.1",
            "title": "Intended Use",
            "text": "Used for blood pressure measurement."
        },
        {
            "section_number": "2.1",
            "title": "Battery Life",
            "text": "Battery lasts 300 cycles."
        },
        {
            "section_number": "4.1",
            "title": "New Feature",
            "text": "New feature description."
        }
    ]

    result = compare_sections(old_sections, new_sections)

    assert len(result["unchanged"]) == 1
    assert len(result["changed"]) == 1
    assert len(result["added"]) == 1
    assert len(result["removed"]) == 1
