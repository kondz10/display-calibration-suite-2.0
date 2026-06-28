from pathlib import Path
import base64
import json
import mimetypes

folder = Path(__file__).resolve().parent
exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
items = []

for file in sorted(folder.iterdir()):
    if file.suffix.lower() not in exts:
        continue
    mime = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
    data = "data:%s;base64,%s" % (mime, base64.b64encode(file.read_bytes()).decode("ascii"))
    name = file.stem.replace("_", " ").replace("-", " ").strip().title()
    items.append({"name": name, "file": file.name, "dataUrl": data})

out = folder / "katalog.js"
out.write_text(
    "// Katalog grafik dla modułu Calibration Preview.\\n"
    "// Plik wygenerowany automatycznie przez generuj_katalog_grafik.py.\\n\\n"
    "window.CALIBRATION_PREVIEW_IMAGES = "
    + json.dumps(items, ensure_ascii=False, indent=2)
    + ";\\n",
    encoding="utf-8"
)

print(f"Zaktualizowano {out.name}. Liczba grafik: {len(items)}")
