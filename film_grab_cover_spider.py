#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
film_grab_cover_spider.py
~~~~~~~~~~~~~~~~~~~~~~~~~
抓取 https://film-grab.com/ 1-62 页中的封面图片（仅下载 <img> 的 src）。
"""

import os
import time
import pathlib
import logging
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# =============== 配置项 ===============
BASE_URL   = "https://film-grab.com"
PAGES      = range(2, 63)      # 1-62
PAUSE_SEC  = 1.0
SAVE_DIR   = pathlib.Path("film_grab_covers")
UA         = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/125.0.0.0 Safari/537.36")

# =============== 工具函数 ===============
def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

### 改动 1：只取 src（不再解析 srcset / data-*）
def get_img_src(img_tag) -> str | None:
    src = img_tag.get("src")
    if not src:
        return None
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return BASE_URL + src
    return src

def download(url: str, dest: pathlib.Path) -> bool:
    if dest.exists():
        return False
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=15)
        r.raise_for_status()
    except Exception as e:
        logging.warning("fail %s – %s", url, e)
        return False
    dest.write_bytes(r.content)
    logging.info("saved %s", dest.name)
    return True

def crawl_page(n: int) -> None:
    page_url = BASE_URL if n == 1 else f"{BASE_URL}/page/{n}/"
    logging.info(">>> Page %d", n)

    try:
        r = requests.get(page_url, headers={"User-Agent": UA}, timeout=15)
        r.raise_for_status()
    except Exception as e:
        logging.error("request %s – %s", page_url, e)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    ### 改动 2：精确在 <article> 中找第一张 <img>（wp-post-image）
    for art in soup.select("article"):
        img = art.select_one("img.wp-post-image") or art.find("img")
        if not img:
            continue
        img_url = get_img_src(img)
        if not img_url:
            continue

        filename = os.path.basename(urlparse(img_url).path)
        download(img_url, SAVE_DIR / filename)

# =============== 主入口 ===============
def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")
    ensure_dir(SAVE_DIR)
    for p in PAGES:
        crawl_page(p)
        time.sleep(PAUSE_SEC)
    logging.info("🎬 Done — images in %s", SAVE_DIR.resolve())

if __name__ == "__main__":
    main()
