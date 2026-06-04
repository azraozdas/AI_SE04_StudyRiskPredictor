"""Fixed course color mapping — identical everywhere in the application."""

from __future__ import annotations

# Muted SaaS-friendly palette (dark-theme readable)
COURSE_COLORS: dict[str, str] = {
    "Algorithms": "#60A5FA",
    "Artificial Intelligence": "#A78BFA",
    "Machine Learning": "#22D3EE",
    "Data Science": "#34D399",
    "Computer Networks": "#FB923C",
    "Cloud Computing": "#818CF8",
    "Statistics": "#2DD4BF",
    "Web Development": "#F472B6",
    "Mobile App Development": "#38BDF8",
    "Cybersecurity Fundamentals": "#FB7185",
    "Computer Architecture": "#67E8F9",
    "Database Systems": "#C084FC",
    "Discrete Mathematics": "#4ADE80",
    "Human-Computer Interaction": "#E879F9",
    "Information Systems": "#7DD3FC",
    "Introduction to Programming": "#93C5FD",
    "Linear Algebra": "#A3E635",
    "Object-Oriented Programming": "#FBBF24",
    "Operating Systems": "#F97316",
    "Software Engineering": "#6366F1",
}

_FALLBACK_PALETTE = (
    "#60A5FA", "#A78BFA", "#22D3EE", "#34D399", "#FB923C",
    "#818CF8", "#2DD4BF", "#F472B6", "#38BDF8", "#FB7185",
)


def get_course_color(course_name: str) -> str:
    """Return the fixed hex color for a course (deterministic)."""
    name = (course_name or "").strip()
    if name in COURSE_COLORS:
        return COURSE_COLORS[name]
    idx = sum(ord(c) for c in name) % len(_FALLBACK_PALETTE)
    return _FALLBACK_PALETTE[idx]


def course_color_bg(course_name: str, alpha: float = 0.12) -> str:
    """Subtle tint for avatars / schedule blocks (not full card fill)."""
    hex_color = get_course_color(course_name).lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
