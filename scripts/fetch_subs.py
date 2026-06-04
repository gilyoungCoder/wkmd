#!/usr/bin/env python3
"""
유튜브 자막 다운로드 → 깨끗한 텍스트로 변환 (소재 분석용)

사용:
  python3 scripts/fetch_subs.py <영상URL 또는 ID> [추가URL...]
  python3 scripts/fetch_subs.py https://www.youtube.com/watch?v=XXXX --langs ko,en

출력: data/subs/<영상ID>.txt  (마지막 줄들에 경로 출력 — 에이전트가 읽음)
의존: yt-dlp — 자동생성 자막 포함, API 키 불필요
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBDIR = ROOT / "data" / "subs"

# 수집 대상 언어 (자동생성 포함). *-orig = 원어 자동자막
DEFAULT_LANGS = "ko,en,ja,fr,it,ko-orig,en-orig,ja-orig,fr-orig,it-orig"


def video_id(u: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", u)
    return m.group(1) if m else u.strip()


def clean_vtt(path: Path) -> str:
    """VTT → 평문. 타임스탬프/태그 제거 + 자동자막 특유의 롤링 중복 제거."""
    lines, prev = [], None
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = re.sub(r"<[^>]+>", "", raw).strip()
        if (not line or "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE"))
                or re.fullmatch(r"\d+", line)
                or re.fullmatch(r"align:[^ ]+ position:[^ ]+", line)):
            continue
        if line != prev:            # 연속 중복(롤링 캡션) 제거
            lines.append(line)
            prev = line
    # 한 번 더: 인접 줄이 서로 포함관계면 긴 쪽만
    out = []
    for l in lines:
        if out and (l in out[-1] or out[-1] in l):
            out[-1] = max(out[-1], l, key=len)
        else:
            out.append(l)
    return "\n".join(out)


def fetch(url: str, langs: str) -> Path | None:
    vid = video_id(url)
    SUBDIR.mkdir(parents=True, exist_ok=True)
    tmpl = str(SUBDIR / "%(id)s.%(ext)s")
    base = ["yt-dlp", "--no-warnings", "--skip-download",
            "--write-subs", "--write-auto-subs",
            "--sub-langs", langs, "--sub-format", "vtt",
            "-o", tmpl, f"https://www.youtube.com/watch?v={vid}"]
    # 자동자막은 android 클라이언트로만 노출되는 경우가 많음 → android 먼저, 실패 시 기본
    for extra in (["--extractor-args", "youtube:player_client=android"], []):
        r = subprocess.run(base + extra, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and list(SUBDIR.glob(f"{vid}.*.vtt")):
            break
    else:
        if r.returncode != 0:
            print(f"[실패] {vid}: {r.stderr.strip()[:200]}", file=sys.stderr)
            return None
    vtts = sorted(SUBDIR.glob(f"{vid}.*.vtt"))
    if not vtts:
        print(f"[자막없음] {vid}", file=sys.stderr)
        return None
    # 우선순위: 원어(orig) > ko > en > 첫 번째
    def rank(p: Path):
        s = p.name
        return (0 if "-orig" in s else 1 if ".ko." in s else 2 if ".en." in s else 3)
    best = sorted(vtts, key=rank)[0]
    txt = SUBDIR / f"{vid}.txt"
    lang = best.name.replace(f"{vid}.", "").replace(".vtt", "")
    body = clean_vtt(best)
    txt.write_text(f"# video: https://www.youtube.com/watch?v={vid}\n"
                   f"# subtitle-lang: {lang}\n\n{body}\n", encoding="utf-8")
    for p in vtts:                  # 원본 vtt 정리
        p.unlink(missing_ok=True)
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--langs", default=DEFAULT_LANGS)
    args = ap.parse_args()
    ok = []
    for u in args.urls:
        p = fetch(u, args.langs)
        if p:
            ok.append(p)
    for p in ok:
        print(str(p))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
