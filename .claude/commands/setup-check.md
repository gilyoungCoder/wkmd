---
description: 환경 점검 — 설치 직후 또는 뭔가 안 될 때 실행
---

위캔드무드 작업 환경을 점검하고 결과를 ✅/❌ 체크리스트로 보여준다. 비개발자 사용자 기준으로 친절하게.

## 점검 항목 (순서대로 실행)

1. **도구**: `python3 --version`, `yt-dlp --version`, `git --version` — 하나라도 없으면 `bash scripts/setup.sh` 재실행 안내
2. **폴더**: data/trends, data/subs, outputs/{content,diagnosis,review,trends} 존재 확인 (없으면 직접 mkdir로 만들어주기)
3. **브랜드 컨텍스트**: brand/tone.md, services.md, audience.md, diagnosis-criteria.md 존재 + **내용이 채워졌는지** (골격뿐이면 "⚠️ 아직 비어있음 — 채우면 품질이 크게 올라갑니다" + 채우는 법 안내)
4. **유튜브 수집 실동작**: `python3 scripts/trend_scan.py --countries kr --per-keyword 2 --workers 4` (1~2분) → 리포트 생성되면 ✅
5. **웹사이트 연결**: WebFetch로 https://wkmd.vercel.app 가 응답하는지
6. **레포 최신 여부**: `git fetch && git status` — 뒤처져 있으면 "영환님이 업데이트했네요. 받아올까요?" → `git pull`

## 결과 출력
```
=== 환경 점검 결과 ===
✅/❌ 항목별 한 줄
→ 다음 할 일 제안 (예: brand/tone.md 채우기, /trend 첫 실행)
```
❌가 있으면 해결을 직접 해주거나, 영환에게 보낼 한 줄 요약을 만들어준다.
