"""
PH Hunter file naming utility.

Formula: PH-Hunters — {Topic} — {Source} — {Date} — {N} people.xlsx
"""
import re
from datetime import datetime
from pathlib import Path


def make_ph_filename(topic: str, source_type: str, count: int = 0,
                      output_dir: str = "", extension: str = "xlsx") -> str:
    """
    Generate a human-readable filename for PH Hunter exports.

    Examples:
        make_ph_filename("AI automation", "Topics", 50)
        → "PH-Hunters — AI automation — Topics — 2026-04-29 — 50 people.xlsx"

        make_ph_filename("SaaS", "SOURCE BENCHMARK")
        → "PH-Hunters — SaaS — SOURCE BENCHMARK — 2026-04-29.xlsx"
    """
    def sanitize(s):
        return re.sub(r'[<>:"/\\|?*]', '', s.strip())[:40].strip()

    topic_s = sanitize(topic)
    source_s = sanitize(source_type)
    date_s = datetime.now().strftime("%Y-%m-%d")

    parts = ["PH-Hunters", topic_s, source_s, date_s]
    if count > 0:
        parts.append(f"{count} people")

    filename = " — ".join(parts) + f".{extension}"

    if output_dir:
        return str(Path(output_dir) / filename)
    return filename
