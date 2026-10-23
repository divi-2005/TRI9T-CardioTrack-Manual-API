
from app.staleness import check_staleness


def test_staleness_statuses():
    selected_sections = [
        {
            "section_number": "1.1",
            "title": "Intended Use",
            "text": "Original intended use."
        },
        {
            "section_number": "2.1",
            "title": "Specifications",
            "text": "Old specifications."
        },
        {
            "section_number": "3.1",
            "title": "Old Feature",
            "text": "Feature text."
        }
    ]

    current_sections = [
        {
            "section_number": "1.1",
            "title": "Intended Use",
            "text": "Original intended use."
        },
        {
            "section_number": "2.1",
            "title": "Specifications",
            "text": "Updated specifications."
        }
    ]

    results = check_staleness(
        selected_sections,
        current_sections
    )

    statuses = [item["status"] for item in results]

    assert statuses == ["current", "stale", "removed"]
