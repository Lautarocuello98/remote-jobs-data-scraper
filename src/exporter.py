import json
import pandas as pd
from src.config import RAW_CSV_PATH, CLEAN_CSV_PATH, OUTPUT_XLSX_PATH, OUTPUT_JSON_PATH


def export_raw_csv(df: pd.DataFrame) -> None:
    df.to_csv(RAW_CSV_PATH, index=False, encoding="utf-8")


def export_clean_csv(df: pd.DataFrame) -> None:
    df.to_csv(CLEAN_CSV_PATH, index=False, encoding="utf-8")


def export_excel(df: pd.DataFrame) -> None:
    df.to_excel(OUTPUT_XLSX_PATH, index=False)


def export_json(df: pd.DataFrame) -> None:
    records = df.to_dict(orient="records")
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)