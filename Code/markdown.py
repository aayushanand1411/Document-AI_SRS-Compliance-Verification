from docling.document_converter import DocumentConverter
from docling_core.types.doc import PictureItem

converter = DocumentConverter()
result = converter.convert("input.pdf")

parts = []

for item, _level in result.document.iterate_items():
    if isinstance(item, PictureItem):
        parts.append("<!-- image -->")
    elif hasattr(item, "text"):
        parts.append(item.text)

markdown = "\n\n".join(parts)

with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown)
