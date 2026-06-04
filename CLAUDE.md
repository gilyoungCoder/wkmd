# WKND MOOD 에이전트 워크스페이스

이 폴더는 위캔드무드(WKND MOOD) — 남성 프리미엄 퍼스널 비주얼 컨설턴트 브랜드의 AI 작업 공간입니다.
사용자는 **박선우 대표(비개발자)**입니다. 아래 규칙을 항상 따르세요.

## 기본 규칙

1. **항상 한국어로** 대화하고 결과물을 만든다 (영어 콘텐츠 요청 시 예외).
2. 사용자는 개발자가 아니다 — 기술 용어를 최소화하고, 터미널 명령이 필요하면 설명 후 **직접 실행해준다**.
3. 모든 콘텐츠 작업 전에 `brand/tone.md`, `brand/services.md`, `brand/audience.md`를 읽고 브랜드 톤을 따른다.
4. 결과물은 `outputs/` 아래에 저장한다 (콘텐츠→`outputs/content/`, 진단서→`outputs/diagnosis/`, 후기→`outputs/review/`, 소재보드→`outputs/trends/`).
5. 잘 나온 프롬프트/결과물 패턴은 `prompts/`에 누적한다 (자산화).
6. 비밀키·고객 개인정보(사진, 연락처)는 **절대 git에 커밋하지 않는다** (`data/`, `outputs/`는 gitignore됨).

## 톤 핵심 (상세: brand/tone.md)

- 프리미엄·절제. 과장 광고 표현 금지 ("인생이 바뀝니다" ✗ → "인상이 정리됩니다" ✓)
- 의료·시술 권유성 표현 금지. 외모 비하 금지 — 항상 "보완·방향" 프레임.
- 이모지 남발 금지. 채널별 형식은 `prompts/content/` 참조.

## 작업 라우팅 (슬래시 커맨드)

| 하고 싶은 일 | 명령 |
|---|---|
| 유튜브 패션 트렌드 스캔 → 소재 추출 | `/trend` (국가 지정: `/trend kr,jp`) |
| 블로그/쓰레드/인스타 콘텐츠 작성 | `/content` |
| 외모진단서 제작 (유료 상품) | `/diagnosis` |
| 패션 MBTI 타입 콘텐츠 디벨롭 | `/mbti` (예: `/mbti SMTH`) |
| 고객 후기 다듬기 · 스타일링 PDF | `/review` |
| 환경 점검 (뭔가 안 될 때) | `/setup-check` |

슬래시 커맨드 없이 자연어로 요청해도 위 작업이면 해당 커맨드의 절차를 따른다.

## 전문 에이전트 (자동 위임)

- `fashion-director` — 패션 전문 지식이 필요한 모든 판단 (스타일 분석, MBTI 디벨롭, 진단 기준)
- `copywriter` — 브랜드 톤 콘텐츠 작성 (블로그/쓰레드/인스타/카페)
- `trend-analyst` — 트렌드 리포트 해석, 소재 추출, 자막 분석
- `diagnosis-writer` — 외모진단서 작성 (fashion-director 기준 + 진단 템플릿)
- `review-assistant` — 후기 정리, 스타일링 PDF 콘텐츠

## 외부 정보

- 웹사이트(라이브): https://wkmd.vercel.app · MBTI 테스트: /test · 콘텐츠 편집: /studio
- 유튜브 수집: `scripts/trend_scan.py` (검색·조회수), `scripts/fetch_subs.py` (자막) — API 키 불필요(yt-dlp)
- 수집 국가: 한국·미국·일본·프랑스·영국·이탈리아 (중국은 추후 샤오홍슈 단계에서)

## 사업자 정보 (필요 시 인용)

위캔드무드 / 대표 박선우 / 821-57-00833 / 서울 강남구 강남대로112길 47 2층 429A
IG @wkndmood_official · 카카오톡 pf.kakao.com/_NexofG/chat · 메일 wkndmood.official@gmail.com
