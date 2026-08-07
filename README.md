# CodeScope

CodeScope is a Python CLI tool that analyzes software projects and generates useful developer metrics.

# SCREENSHOTS

![CodeScope Demo](codescope/assets/demo.png)
![CodeScope Demo](codescope/assets/2f.png)
![CodeScope Demo](codescope/assets/3f.png)

## Features

* Analyze project structure
* Count files and directories
* Detect TODO/FIXME comments
* Show largest files
* Detect programming languages
* Analyze Python code statistics
* Export reports to JSON

## Installation

Clone the repository:

git clone https://github.com/anannyapahuja/codescope.git

Install dependencies:

pip install -e .

## Usage

Analyze current folder:

codescope analyze

Analyze another folder:

codescope analyze path/to/project

Export JSON report:

codescope analyze --export report.json

## Example Output

Languages Detected
- Python
- Markdown
- TOML

Python Stats
- Functions: 4
- Classes: 0
- Imports: 9

## Tech Stack

* Python
* Typer
* Rich
* Pytest
