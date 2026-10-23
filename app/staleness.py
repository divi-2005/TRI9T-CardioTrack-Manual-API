
from app.versioning import text_hash


def check_staleness(
    selected_sections: list[dict],
    current_sections: list[dict]
) -> list[dict]:
    """Check whether selected section snapshots are outdated."""

    current_map = {
        (
            section["section_number"],
            section["title"].strip().casefold()
        ): section
        for section in current_sections
    }

    results = []

    for selected in selected_sections:
        key = (
            selected["section_number"],
            selected["title"].strip().casefold()
        )

        current = current_map.get(key)

        if current is None:
            status = "removed"
        elif text_hash(selected.get("text", "")) != text_hash(
            current.get("text", "")
        ):
            status = "stale"
        else:
            status = "current"

        results.append({
            "section_number": selected["section_number"],
            "title": selected["title"],
            "status": status
        })

    return results
