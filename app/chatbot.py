import os
from dotenv import load_dotenv
import openai
import yaml

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

import yaml

def load_schema(file_path="schema.yaml"):
    with open(file_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    return schema

def format_schema(schema):
    lines = []
    for table, info in schema["tables"].items():
        cols = [col if isinstance(col, str) else list(col.keys())[0] for col in info["columns"]]
        lines.append(f"- {table}({', '.join(cols)})")
    return "\n".join(lines)

# Inject into prompt
schema_text = format_schema(load_schema())
prompt = base_prompt + "\n\nSchema:\n" + schema_text

