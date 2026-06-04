# WKND MOOD × 영환 협업 프로젝트

> 위캔드무드(WKND MOOD) — 남성 프리미엄 퍼스널 비주얼 컨설턴트 브랜드의
> 웹사이트 · 퍼널 · 콘텐츠 자동화 · 리뷰 시스템 구축 프로젝트.
>
> 작성 기준일: 2026-06-04 / 원본 태스크 목록: 박선우 (위캔드무드 대표)

---

## 한눈에 보기

| 단계 | 내용 | 목표 기한 | 상태 | 문서 |
|---|---|---|---|---|
| **0-A** | AI 환경 세팅 (선우님 Claude 에이전트 구축) | 6/8 (일) | 🔜 진행 예정 | [docs/00-ai-setup.md](docs/00-ai-setup.md) |
| **0-B** | 협업 준비물 (자료 .zip 등) | 6/8 | ⏳ 선우님 | [docs/materials-checklist.md](docs/materials-checklist.md) |
| **1** | 웹사이트 B2B / B2C 분리 구조 **[최우선]** | 6/15 (일) | 🔜 | [docs/01-website-b2b-b2c.md](docs/01-website-b2b-b2c.md) |
| **2** | 외모진단 · 패션MBTI 퍼널 | 6/22 (월) | 🔜 | [docs/02-diagnosis-funnel.md](docs/02-diagnosis-funnel.md) |
| **3** | 콘텐츠 자동화 파이프라인 | 6/29 (월) | 🔜 | [docs/03-content-pipeline.md](docs/03-content-pipeline.md) |
| **4** | 후기 · 리뷰 시스템 | 7/6 (월) | 🔜 | [docs/04-review-system.md](docs/04-review-system.md) |
| **2차** | 역량 강화 (크롤링/PPT/프롬프트/사진보정) | 수시 | 🔜 | [docs/05-skills-track.md](docs/05-skills-track.md) |

전체 일정/의존관계: **[ROADMAP.md](ROADMAP.md)**

## 이미 만들어진 것 (토대)

- **데모 사이트 라이브**: https://wkmd.vercel.app — Next.js 16 + Sanity CMS, 45 라우트
  - 홈 / 브랜드 / 컨설팅 / 포트폴리오 / FAQ / 문의 / **패션 MBTI 테스트**(12문항→16타입, /test)
  - 거의 모든 사진·문구를 코드 수정 없이 https://wkmd.vercel.app/studio 에서 편집 가능
  - 현재 상태 상세: [docs/website-current-state.md](docs/website-current-state.md)
- 소스코드: `siml-09:/mnt/home3/yhgil99/etc/wkmd/web/` (연구실 서버 — 추후 이 레포 또는 별도 레포로 이관 검토)

## 🤖 에이전트 워크스페이스 (선우님은 여기부터!)

이 레포 자체가 **위캔드무드 전용 AI 작업 환경**입니다. 클론 + 설치만 하면 바로 동작:

→ **[SETUP_GUIDE.md](SETUP_GUIDE.md)** 따라 설치 (Mac, 30분) → `claude` 실행 → `/setup-check`

| 명령 | 기능 | 뒷받침 |
|---|---|---|
| `/trend` | 유튜브 패션 트렌드 스캔(한/미/일/프/영/이) → 급상승 채널 TOP10 → 소재 보드 | `scripts/trend_scan.py` + `scripts/fetch_subs.py`(자막) — API 키 불필요 |
| `/content` | 소재 → 쓰레드/블로그/인스타 콘텐츠 (브랜드 톤) | `copywriter` 에이전트 + `prompts/content/` |
| `/diagnosis` | 유료 외모진단서 제작 (첫 실행 = 기준 인터뷰) | `diagnosis-writer` + `brand/diagnosis-criteria.md` |
| `/mbti SMTH` | 패션 MBTI 타입 콘텐츠 디벨롭 | `fashion-director` + 라이브 사이트 연동 |
| `/review` | 후기 다듬기 · 스타일링 PDF 원고 | `review-assistant` + `prompts/review/` |
| `/setup-check` | 환경 자가진단 | — |

구성: `CLAUDE.md`(브랜드 두뇌) · `.claude/agents/` 전문 에이전트 5종 · `.claude/commands/` 워크플로 6종 · `brand/` 톤·서비스·진단기준 · `prompts/` 템플릿 · `scripts/` 수집 도구

## 이 레포의 역할

1. **에이전트 워크스페이스** — 위 표의 모든 기능이 클론 즉시 동작
2. **기획/설계 문서의 단일 진실 공급원** — 각 단계 상세 기획, 결정 사항, TODO
3. **선우님과의 협업 보드** — 이슈/체크리스트로 진행 상황 공유 (선우님 GitHub 초대 예정)
4. 2~4단계의 **프롬프트 템플릿 / PDF 템플릿 / 파이프라인 스크립트** 저장소

## 역할 분담 원칙

- **영환**: 기술 구축 (사이트/퍼널/파이프라인/템플릿), AI 세팅, 방법 안내
- **선우**: 콘텐츠 방향성·문구 확정, 자료 전달, 브랜드 톤 결정, 채널 운영, 고객 응대
- 기한은 제안값 — 영환 평일 연구 일정에 맞춰 조정 가능

## 운영 메모

- ⚠️ 이 레포는 **private** — 사업 정보(가격 전략·퍼널 설계·고객 플로우) 포함
- 비밀키(.secretkeys, API 토큰)는 **절대 커밋 금지** (.gitignore 처리됨)
