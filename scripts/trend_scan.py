#!/usr/bin/env python3
"""
WKND MOOD 유튜브 트렌드 스캔
- 국가별 패션 키워드로 유튜브 검색 (최근 1개월 업로드 + 조회수순)
- 영상별 일평균 조회수(velocity)를 계산해 "급상승" 정도를 측정
- 채널 단위로 집계 → 급상승 채널 TOP 10 + 소재 추출용 영상 목록 리포트 생성

사용:
  python3 scripts/trend_scan.py                    # 전체 6개국
  python3 scripts/trend_scan.py --countries kr,jp  # 국가 지정
  python3 scripts/trend_scan.py --per-keyword 8 --workers 8

출력:
  data/trends/trend_YYYY-MM-DD.md   (사람/에이전트가 읽는 리포트)
  data/trends/raw_YYYY-MM-DD.json   (원본 데이터)

의존: yt-dlp (brew install yt-dlp) — API 키 불필요
키워드 수정: brand/trend-keywords.json
"""
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

# 기본 키워드 (brand/trend-keywords.json 이 있으면 그걸 우선 사용)
DEFAULT_KEYWORDS = {
    "kr": {"name": "한국",     "keywords": ["남자 패션", "남자 코디", "남자 스타일링"]},
    "us": {"name": "미국",     "keywords": ["men's fashion", "mens outfit ideas", "men style tips"]},
    "jp": {"name": "일본",     "keywords": ["メンズファッション", "メンズコーデ", "メンズ 着こなし"]},
    "fr": {"name": "프랑스",   "keywords": ["mode homme", "tenue homme", "style homme"]},
    "uk": {"name": "영국",     "keywords": ["british mens fashion", "mens smart casual uk", "men style guide uk"]},
    "it": {"name": "이탈리아", "keywords": ["moda uomo", "outfit uomo", "stile uomo"]},
}

# 유튜브 검색 필터: 정렬=조회수, 업로드=이번 달, 종류=동영상
SP_VIEWS_THIS_MONTH = "CAMSBAgEEAE%3D"


def load_keywords():
    cfg = ROOT / "brand" / "trend-keywords.json"
    if cfg.exists():
        try:
            return json.loads(cfg.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[경고] {cfg} 파싱 실패({e}) — 기본 키워드 사용", file=sys.stderr)
    return DEFAULT_KEYWORDS


def run_ytdlp(args, timeout=120):
    cmd = ["yt-dlp", "--no-warnings", "--quiet"] + args
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300] or "yt-dlp failed")
    return r.stdout


def search_keyword(keyword, limit):
    """조회수순·이번달 필터 검색 → 후보 영상 (flat, 빠름)."""
    url = (f"https://www.youtube.com/results?search_query={quote(keyword)}"
           f"&sp={SP_VIEWS_THIS_MONTH}")
    out = run_ytdlp(["-J", "--flat-playlist", "--playlist-end", str(limit), url])
    data = json.loads(out)
    entries = data.get("entries") or []
    vids = []
    for e in entries:
        if not e or e.get("_type") not in (None, "url") or not e.get("id"):
            continue
        if e.get("duration") and e["duration"] < 45:  # 너무 짧은 클립 제외(쇼츠 일부)
            pass  # 쇼츠도 소재로는 유효 — 제외하지 않고 표시만
        vids.append({
            "id": e["id"],
            "title": e.get("title") or "",
            "channel": e.get("channel") or e.get("uploader") or "?",
            "channel_id": e.get("channel_id") or "",
            "view_count": e.get("view_count"),
            "duration": e.get("duration"),
            "keyword": keyword,
            "url": f"https://www.youtube.com/watch?v={e['id']}",
        })
    return vids


def enrich_video(v):
    """업로드일·정확한 조회수 보강 (영상당 1회 요청)."""
    try:
        out = run_ytdlp(["-J", "--no-playlist", v["url"]], timeout=60)
        d = json.loads(out)
        v["view_count"] = d.get("view_count") or v.get("view_count") or 0
        v["upload_date"] = d.get("upload_date")          # YYYYMMDD
        v["channel"] = d.get("channel") or v["channel"]
        v["channel_id"] = d.get("channel_id") or v["channel_id"]
        v["channel_follower_count"] = d.get("channel_follower_count")
        v["title"] = d.get("title") or v["title"]
        v["duration"] = d.get("duration") or v.get("duration")
        if v["upload_date"]:
            up = datetime.strptime(v["upload_date"], "%Y%m%d").replace(tzinfo=timezone.utc)
            days = max((datetime.now(timezone.utc) - up).days, 1)
            v["days_old"] = days
            v["velocity"] = round((v["view_count"] or 0) / days)
        return v
    except Exception as e:
        v["error"] = str(e)[:120]
        return v


def fmt_n(n):
    if n is None:
        return "?"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


def scan_country(code, conf, per_keyword, workers, max_age_days):
    print(f"[{conf['name']}] 검색 중: {', '.join(conf['keywords'])}", file=sys.stderr)
    candidates, seen = [], set()
    for kw in conf["keywords"]:
        try:
            for v in search_keyword(kw, per_keyword):
                if v["id"] not in seen:
                    seen.add(v["id"])
                    candidates.append(v)
        except Exception as e:
            print(f"  [경고] '{kw}' 검색 실패: {e}", file=sys.stderr)

    print(f"[{conf['name']}] 후보 {len(candidates)}개 상세 수집 중...", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(enrich_video, v) for v in candidates]
        videos = [f.result() for f in as_completed(futs)]

    # 최근 N일 이내만 (필터가 새지 않게 이중 안전망)
    videos = [v for v in videos
              if v.get("velocity") is not None and v.get("days_old", 999) <= max_age_days]
    videos.sort(key=lambda v: v["velocity"], reverse=True)

    # 채널 집계 → 급상승 채널 TOP 10
    channels = {}
    for v in videos:
        c = channels.setdefault(v["channel_id"] or v["channel"], {
            "channel": v["channel"], "videos": [], "total_velocity": 0,
            "subscribers": v.get("channel_follower_count"),
        })
        c["videos"].append(v)
        c["total_velocity"] += v["velocity"]
    top_channels = sorted(channels.values(),
                          key=lambda c: c["total_velocity"], reverse=True)[:10]
    return {"videos": videos, "top_channels": top_channels}


def build_report(results, kws, date_str):
    L = [f"# 유튜브 패션 트렌드 리포트 — {date_str}",
         "",
         "> 기준: 최근 1개월 업로드 영상, 일평균 조회수(velocity) 순.",
         "> 다음 단계: 이 리포트를 `/trend` 에이전트가 읽고 소재 보드를 만듭니다.",
         ""]
    for code, res in results.items():
        name = kws[code]["name"]
        L.append(f"## {name} ({code})")
        L.append("")
        L.append("### 🚀 급상승 채널 TOP 10")
        L.append("")
        L.append("| # | 채널 | 구독자 | 일평균 조회수 합 | 잡힌 영상 |")
        L.append("|---|---|---|---|---|")
        for i, c in enumerate(res["top_channels"], 1):
            L.append(f"| {i} | {c['channel']} | {fmt_n(c.get('subscribers'))} "
                     f"| {fmt_n(c['total_velocity'])}/일 | {len(c['videos'])}개 |")
        L.append("")
        L.append("### 📈 소재 추출용 상위 영상 (velocity 순)")
        L.append("")
        for v in res["videos"][:15]:
            dur = f"{(v.get('duration') or 0)//60}분" if v.get("duration") else "?"
            L.append(f"- **{v['title']}**  \n"
                     f"  {v['channel']} · 조회 {fmt_n(v['view_count'])} · "
                     f"{fmt_n(v['velocity'])}/일 · {v.get('days_old','?')}일 전 · {dur} · "
                     f"검색어 `{v['keyword']}`  \n"
                     f"  {v['url']}")
        L.append("")
    L.append("---")
    L.append("자막이 필요한 영상: `python3 scripts/fetch_subs.py <영상URL>`")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--countries", default="kr,us,jp,fr,uk,it")
    ap.add_argument("--per-keyword", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-age-days", type=int, default=35)
    ap.add_argument("--out", default=str(ROOT / "data" / "trends"))
    args = ap.parse_args()

    kws = load_keywords()
    codes = [c.strip() for c in args.countries.split(",") if c.strip() in kws]
    if not codes:
        print(f"국가 코드 오류. 가능: {', '.join(kws)}", file=sys.stderr)
        sys.exit(1)

    results = {}
    for code in codes:
        results[code] = scan_country(code, kws[code], args.per_keyword,
                                     args.workers, args.max_age_days)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    raw = outdir / f"raw_{date_str}.json"
    raw.write_text(json.dumps(results, ensure_ascii=False, indent=1, default=str),
                   encoding="utf-8")
    report = outdir / f"trend_{date_str}.md"
    report.write_text(build_report(results, kws, date_str), encoding="utf-8")
    print(str(report))           # 마지막 줄 = 리포트 경로 (에이전트가 읽음)


if __name__ == "__main__":
    main()
