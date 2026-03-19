"""
images/ 内の全JPGを長辺2000px・画質85%でリサイズして images/web/ に書き出す
"""

from pathlib import Path
from PIL import Image

SRC_DIR = Path(__file__).parent / "images"
DST_DIR = SRC_DIR / "web"
MAX_SIZE = 2000
QUALITY = 85

DST_DIR.mkdir(exist_ok=True)

targets = sorted(SRC_DIR.glob("*.jpg")) + sorted(SRC_DIR.glob("*.jpeg"))

if not targets:
    print("対象画像が見つかりません")
    exit()

for src in targets:
    with Image.open(src) as img:
        # EXIF回転を適用
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)

        # 長辺が2000pxを超える場合のみリサイズ
        if max(img.size) > MAX_SIZE:
            img.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)

        dst = DST_DIR / (src.stem + ".jpg")
        img.convert("RGB").save(dst, "JPEG", quality=QUALITY, optimize=True)
        print(f"{src.name}  {img.size[0]}x{img.size[1]}  →  {dst.name}")

print(f"\n完了: {len(targets)}枚 → {DST_DIR}")
