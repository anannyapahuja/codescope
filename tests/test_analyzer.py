import ast
import json
from pathlib import Path

from codescope.analyzer import analyze_project


def test_analyzer_counts_files(tmp_path: Path):
    file1 = tmp_path / "file1.py"
    file2 = tmp_path / "file2.txt"

    file1.write_text(
        "def hello():\n"
        "    print('Hello')\n"
    )

    file2.write_text(
        "This is a test file.\n"
    )

    result = analyze_project(tmp_path)

    assert result["total_files"] == 2
    assert result["python_stats"]["functions"] == 1
    assert result["extensions"][".py"] == 1
    assert result["extensions"][".txt"] == 1
def test_analyzer_detects_languages(tmp_path):
    python_file = tmp_path / "main.py"
    javascript_file = tmp_path / "app.js"

    python_file.write_text("print('hello')\n")
    javascript_file.write_text("console.log('hello');\n")

    result = analyze_project(tmp_path)

    assert "Python" in result["languages"]
    assert "JavaScript" in result["languages"]
def test_analyzer_counts_python_code_correctly(tmp_path):
    python_file = tmp_path / "example.py"

    python_file.write_text(
        'message = "def this_is_not_a_function():"\n'
        "\n"
        "async def real_function():\n"
        "    return 42\n"
        "\n"
        "class Example:\n"
        "    def method(self):\n"
        "        return 1\n"
    )

    result = analyze_project(tmp_path)

    assert result["python_stats"]["functions"] == 2
    assert result["python_stats"]["classes"] == 1
def test_analyzer_counts_control_flow(tmp_path):
    python_file = tmp_path / "logic.py"

    python_file.write_text(
        "def example(items):\n"
        "    if items:\n"
        "        for item in items:\n"
        "            print(item)\n"
        "    while False:\n"
        "        break\n"
    )

    result = analyze_project(tmp_path)

    assert result["python_stats"]["if_statements"] == 1
    assert result["python_stats"]["for_loops"] == 1
    assert result["python_stats"]["while_loops"] == 1