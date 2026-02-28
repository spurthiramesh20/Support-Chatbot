import json
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:
    raise SystemExit(
        "pandas is required. Install with: .\\.venv\\Scripts\\python.exe -m pip install pandas openpyxl"
    ) from exc


def main() -> None:
    evaluator_dir = Path(__file__).parent
    input_path = evaluator_dir / "output.json"
    output_path = evaluator_dir / "output.xlsx"

    if not input_path.exists():
        raise SystemExit(f"Input not found: {input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("Expected output.json to be a list of results.")

    df = pd.json_normalize(data)
    df.to_excel(output_path, index=False)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
