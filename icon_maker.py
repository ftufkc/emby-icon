#!/usr/bin/env python3
# coding: utf-8
"""
Batch icon processor:
1. Center-crop non-square images.
2. Resize to 144×144 px.
3. Add white Chinese text centered near the bottom.
4. Apply rounded-corner mask.
"""

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def process_images(
    input_dir: Path,
    output_dir: Path,
    text: str,
    font_path: str = "NotoSansCJKtc-Bold.ttf",
    font_size_ratio: float = 0.15,   # 字号 ≈ 图宽 × 0.22，可按需调
    padding_ratio: float = 0.25,     # 底部留白比例
    corner_radius: int = 20,
):
    """Scan input_dir, write processed PNGs to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in input_dir.iterdir():
        if not img_path.is_file():
            continue
        try:
            with Image.open(img_path).convert("RGBA") as im:
                # 1. 居中裁剪为正方形
                w, h = im.size
                if w != h:
                    side = min(w, h)
                    left = (w - side) // 2
                    top = (h - side) // 2
                    im = im.crop((left, top, left + side, top + side))
                    w = h = side

                # 2. 缩放到 144×144
                if w != 144:
                    im = im.resize((144, 144), Image.LANCZOS)
                    w = h = 144

                # 3. 叠加文字
                draw = ImageDraw.Draw(im)
                # 找到合适字号：宽度占 90% 以内
                font_size = int(w * font_size_ratio)
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), text, font=font)  # (x0,y0,x1,y1)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                while text_w > w * 0.9 and font_size > 8:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]

                x = (w - text_w) // 2
                y = h - text_h - int(h * padding_ratio)
                draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

                # 4. 圆角蒙版
                if corner_radius > 0:
                    mask = Image.new("L", (w, h), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.rounded_rectangle((0, 0, w, h), radius=corner_radius, fill=255)
                    im.putalpha(mask)

                # 5. 保存
                out_path = output_dir / img_path.name
                im.save(out_path.with_suffix(".png"), "PNG")
                print(f"✔ {img_path.name} → {out_path.name}")
        except Exception as e:
            print(f"⚠ 跳过 {img_path.name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Batch-add Chinese text and rounded corners to 144×144 icons.")
    parser.add_argument("input_dir", help="包含原始图片的文件夹路径")
    parser.add_argument("output_dir", help="处理后图片的输出文件夹路径")
    parser.add_argument("text", help='要写入的中文文字，如 "青梅映画"')
    parser.add_argument("--font", default="NotoSansCJK-Bold.otf", help="支持中文的字体文件路径")
    parser.add_argument("--radius", type=int, default=20, help="圆角半径 (px)，默认 20")
    args = parser.parse_args()

    process_images(
        Path(args.input_dir),
        Path(args.output_dir),
        args.text,
        font_path=args.font,
        corner_radius=args.radius,
    )


if __name__ == "__main__":
    main()
