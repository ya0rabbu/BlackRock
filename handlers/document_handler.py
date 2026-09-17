import fitz
import pandas as pd
import matplotlib.pyplot as plt
import os

async def process_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text[:2000] if text else "PDF থেকে text extract করা যায়নি।"

async def process_excel(file_path: str) -> str:
    df = pd.read_excel(file_path)
    summary = f"📊 Excel Summary:\n"
    summary += f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
    summary += f"Columns: {', '.join(df.columns.tolist())}\n\n"
    summary += str(df.describe().round(2))
    return summary

async def generate_chart(file_path: str, output_path: str) -> str:
    df = pd.read_excel(file_path)
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return "Chart বানানোর জন্য numeric data নেই।"
    df[numeric_cols].plot(kind="bar", figsize=(10, 6))
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path