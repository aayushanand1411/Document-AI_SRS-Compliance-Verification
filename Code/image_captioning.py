import os
import json
import base64
from pathlib import Path
from ollama import Client

# Folder containing 1.png, 2.png, ...
folder_path = r"/path/to/your/folder"

# Connect to local Ollama
client = Client(host="http://localhost:11434") # run the ollama in terminal

# Prompt for Gemma3:4b
PROMPT = """
You are an expert software architect and technical documentation analyst.
The input image is extracted from a Software Requirements Specification (SRS) document and may contain architecture diagrams, flowcharts, sequence diagrams, UML diagrams, component diagrams, database schemas, process flows, use case diagrams, wireframes, screenshots, tables, or other technical illustrations.
Your task is to generate a detailed textual description of the image in approximately 250-300 words.

Instructions:
1. Identify the type of diagram or figure.
2. Extract and reproduce all visible labels, component names, headings, entities, and text as accurately as possible.
3. Describe all components, actors, modules, databases, services, APIs, and external systems present.
4. Explain connections, arrows, data flow, control flow, dependencies, and interactions between components.
5. Describe the sequence or process represented in the figure.
6. Mention layers, subsystems, inputs, outputs, and communication mechanisms if present.
7. For tables, summarize rows, columns, and important values.
8. For UI screenshots or wireframes, describe screens, buttons, fields, menus, and user actions.
9. Preserve technical terminology exactly as shown.
10. Do not discuss colors, artistic style, or aesthetics unless they convey meaning.
11. If some text is blurry or unreadable, state that explicitly rather than guessing.
12. Write in coherent paragraphs suitable for reconstructing the figure later from the description.

The output should be detailed enough that a software engineer could understand the diagram without seeing the image.
"""

# Dictionary to store captions
captions = {}

# Get image files sorted numerically: 1.png, 2.png, 3.png...
image_files = sorted(
    [f for f in os.listdir(folder_path) if f.lower().endswith(".png")],
    key=lambda x: int(Path(x).stem)
)

for image_name in image_files:
    image_path = os.path.join(folder_path, image_name)

    print(f"Processing {image_name}...")

    try:
        response = client.chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "user",
                    "content": PROMPT,
                    "images": [image_path]   # Ollama accepts image paths directly
                }
            ]
        )

        description = response["message"]["content"].strip()
        captions[image_name] = description

        print(f"Done: {image_name}")

    except Exception as e:
        print(f"Failed on {image_name}: {e}")
        captions[image_name] = None

# Save JSON in the same folder
json_path = os.path.join(folder_path, "captions.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(captions, f, indent=4, ensure_ascii=False)

print(f"\nSaved captions to: {json_path}")
