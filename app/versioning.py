
import re
import hashlib


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    text = text.casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def text_hash(text: str) -> str:
    """Create a SHA-256 hash of normalized text."""
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def compare_sections(
    old_sections: list[dict],
    new_sections: list[dict]
) -> dict:
    """Compare two manual versions by section number and title."""

    def make_key(section: dict) -> tuple[str, str]:
        return (
            section["section_number"].strip(),
            normalize_text(section["title"])
        )

    old_map = {make_key(s): s for s in old_sections}
    new_map = {make_key(s): s for s in new_sections}

    old_keys = set(old_map)
    new_keys = set(new_map)

    added = []
    removed = []
    changed = []
    unchanged = []

    for key in sorted(old_keys | new_keys):
        if key not in old_map:
            added.append(new_map[key])
        elif key not in new_map:
            removed.append(old_map[key])
        elif text_hash(old_map[key]["text"]) != text_hash(new_map[key]["text"]):
            changed.append({
                "section_number": key[0],
                "title": old_map[key]["title"],
                "old_text": old_map[key]["text"],
                "new_text": new_map[key]["text"]
            })
        else:
            unchanged.append(old_map[key])

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged
    }
