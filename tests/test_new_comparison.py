import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _run(args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "scripts.new_comparison", *args],
        cwd=cwd, capture_output=True, text=True,
    )


def test_creates_file_with_valid_front_matter(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    r = _run(
        ["--title", "AとBの違い", "--category", "ai-llm",
         "--slug", "a-vs-b", "--tags", "A,B", "--docs", str(docs)],
        cwd=ROOT,
    )
    assert r.returncode == 0, r.stderr
    md = docs / "ai-llm" / "a-vs-b.md"
    assert md.exists()
    text = md.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---")[1])
    assert fm["title"] == "AとBの違い"
    assert fm["category"] == "ai-llm"
    assert fm["tags"] == ["A", "B"]
    assert fm["freshness"] == "stable"
    assert "# AとBの違い" in text
    assert "## 比較表" in text


def test_existing_file_without_force_fails(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    args = ["--title", "Dup", "--category", "ai-llm", "--slug", "dup",
            "--docs", str(docs)]
    assert _run(args, cwd=ROOT).returncode == 0
    r2 = _run(args, cwd=ROOT)
    assert r2.returncode != 0
    assert "既に存在" in r2.stderr


def test_new_category_requires_title(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    r = _run(
        ["--title", "T", "--category", "newcat", "--slug", "t",
         "--docs", str(docs)],
        cwd=ROOT,
    )
    assert r.returncode != 0
    r2 = _run(
        ["--title", "T", "--category", "newcat", "--slug", "t",
         "--category-title", "新カテゴリ", "--docs", str(docs)],
        cwd=ROOT,
    )
    assert r2.returncode == 0, r2.stderr
    assert (docs / "newcat" / ".pages").read_text(
        encoding="utf-8"
    ).strip() == "title: 新カテゴリ"
