import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _content(page: int) -> list[dict]:
    path = ROOT / "books" / "cpnc-2025" / "pages" / f"p{page:04d}" / "content.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_p0150_p0151_preserves_exact_cross_page_continuity() -> None:
    p0150 = _content(150)
    p0151 = _content(151)

    tail = p0150[-1]["source_transcription"].rstrip()
    head = p0151[0]["source_transcription"].lstrip()

    assert tail.endswith("según la operación")
    assert head.startswith("que vayas a realizar:")
    assert "según la operación que vayas a realizar:" in f"{tail} {head}"
