# WKND MOOD 작업 핸드오프 — 2026-06-04

> 이 세션(06-02 ~ 06-04)에서 진행한 작업 총정리. 새 세션 시작 전 참고용.
> 프로젝트 루트: `siml-09:/mnt/home3/yhgil99/etc/wkmd/web/`
> 라이브: https://wkmd.vercel.app · Studio: https://wkmd.vercel.app/studio (Sanity project `ecfhyeez`, production, 무료플랜 — Upgrade 클릭 금지)
> ⚠️ 2026-06-04 09:30 KST 기준 siml 서버 SSH 전체 불통 → 이 문서는 로컬에 저장됨. 복구되면 `siml-09:/mnt/home3/yhgil99/etc/wkmd/HANDOFF_2026-06-04.md`로 복사 권장.

---

## 1. 인트로 타이밍 단축 (박선우 요청: "로고 완성 후 1초 당기기")

- **파일**: `web/src/components/Intro.tsx` — 타임라인 상수가 파일 상단에 모여 있음. 모바일/데스크톱 동일 컴포넌트(크기만 반응형: `w-[56vw] max-w-[400px] sm:w-[42vw] md:w-[30vw]`).
- 마운트 위치: `src/app/layout.tsx`의 `<Intro />`. 세션 1회만 재생(`sessionStorage "wkmd-intro-played"`) → 테스트는 **Ctrl+Shift+R** 또는 새 탭.
- 1차 패치(commit `66c3426`): TOTAL 2.65s → 1.95s (DRAW_DUR 1.8→1.3s, 로고 완성 후 꼬리 0.7s→0.05s 압축).
- 2차: **영환님이 직접 상수 수정** → 그대로 커밋/배포 (commit "intro: tune timeline constants (faster reveal)"). **현재 라이브 값**:
  - FADE_IN 0.6 / DRAW_DUR 1.3 / FILL_AT 1.0 / FILL_DUR 1.0 / WORD_AT 0.9 / WORD_DUR 0.3 / TAG_AT 1.0 / TAG_DUR 0.1 / HOLD 0.0
  - → REVEAL_AT(커튼 시작) = 1.1s, TOTAL ≈ 1.6s
- ⚠️ **미해결 플래그**: FILL_DUR=1.0이라 로고 채움이 2.0s에 끝나는데 커튼은 1.1s에 올라감 → 로고가 다 안 채워진 채 전환될 수 있음. 라이브 테스트 피드백 대기 상태. (해결책: FILL_DUR을 ~0.4로 되돌리거나 REVEAL_AT을 늦추기)

## 2. Sanity CMS 전면 확장 (코드 전용 콘텐츠 → Studio 편집 가능)

전부 "Sanity 값 || 코드 폴백" 패턴 — 서버 페이지(`export const revalidate = 60`)에서 fetch 후 클라이언트 바디에 props 주입. Sanity 장애/빈 필드여도 사이트 100% 동작(코드 콘텐츠로 폴백).

### 2-1. WKND MOOD TEST (패션 MBTI) 전체
- 스키마(신규): `src/sanity/schemaTypes/documents/moodType.ts` (16타입 — name/tagline/description/keywords/palette/service/CTA/oneLiner/image), `moodQuestion.ts` (12문항 — prompt/optionA/optionB{label,caption,image}). Studio 리스트: "MBTI · Result Types (16)" / "MBTI · Questions (12)".
- 데이터레이어(신규): `src/sanity/moodTest.ts` — `getMoodTypesMerged()` / `getQuestionsMerged()` (필드 단위 머지, 실패 시 코드 콘텐츠).
- 페이지 구조변경: `src/app/test/page.tsx` 서버 컴포넌트화 → 기존 427줄 클라이언트 퀴즈는 `src/app/test/_TestBody.tsx`로 분리, props로 데이터 주입. 결과페이지 `test/result/[code]/page.tsx` + `ResultBody.tsx` + `MoodTypeGrid.tsx`도 머지 데이터 사용.
- **점수계산은 절대 안 깨짐**: `scoreToCode()`는 코드의 QUESTIONS/AXES에 자급자족, Studio에서 code/axis/pole/order 필드 전부 readOnly.
- 시드 파이프라인: `scripts/extract-moodtest.mjs` (esbuild alias `@`→src로 `src/content/moodTest.ts` 번들 → `scripts/moodtest-data.json`) → `scripts/seed-sanity.mjs`가 16 moodType + 12 moodQuestion 문서 push (멱등 createOrReplace).

### 2-2. Before/After + 헤더 로고
- `siteSettings` 스키마에 `branding` 그룹 `logo` 이미지 + `transform` 그룹 `beforeAfterCases[]` {before, after, label} 추가.
- 로고 전역 배선: 루트 레이아웃(async)에서 `getBranding()` fetch → `src/lib/branding.tsx` BrandingProvider 컨텍스트 → `Header.tsx`가 `useBranding()`으로 사용. 폴백 `/logo-mark-dark.png`.

### 2-3. 포트폴리오 20장 전부
- 시드의 `pOrder < 6` 제한 제거 → 20장 모두 Sanity 업로드 완료, Studio에서 교체 가능.

### 2-4. 일부러 미노출 (디자인 보호 — 의도된 결정)
- 라틴 장식 라벨(eyebrow: "Services"/"Portfolio" 등) — 한글 입력 시 디자인 깨짐 방지.
- 결과페이지 OG 이미지/메타데이터 — 코드값 사용(한글폰트 회피).
- 원하면 노출 가능(현재 미요청).

### 시드 재실행 방법
```bash
cd /mnt/home3/yhgil99/etc/wkmd/web
export NVM_DIR=/mnt/home3/yhgil99/.nvm; source $NVM_DIR/nvm.sh
set -a; source ../.secretkeys; set +a
node scripts/extract-moodtest.mjs   # moodTest.ts 코드 변경시에만
NEXT_PUBLIC_SANITY_PROJECT_ID=ecfhyeez NEXT_PUBLIC_SANITY_DATASET=production \
  SANITY_TOKEN="$SANITY_TOKEN" node scripts/seed-sanity.mjs
```

## 3. 검증 완료 내역
- tsc clean, `next build` 45 라우트 성공 (16 결과페이지 + OG SSG 포함).
- 시드 카운트: moodType 16 / moodQuestion 12 / portfolioItem 20 / siteSettings 1 (logo + beforeAfterCases 포함).
- 라이브 확인: 전 라우트 200, `/test` HTML에 Q1 프롬프트("거울 앞에서 더 끌리는 나는") 렌더, 결과페이지 "더 디렉터/The Director" 정상, 홈에 Sanity CDN 이미지 393개, 헤더 로고 `cdn.sanity.io/.../6faa959c...png` 서빙 확인, /studio 200.

## 4. 배포 방법
```bash
cd /mnt/home3/yhgil99/etc/wkmd/web
set -a; source ../.secretkeys; set +a
npx vercel deploy --prod --yes --token "$VERCEL_TOKEN" --scope "$VERCEL_TEAM_ID"
```

## 5. 남은 TODO
1. **인트로 라이브 테스트 피드백 대기** (FILL_DUR vs REVEAL_AT 불일치 — §1 ⚠️ 참고)
2. 16타입 MBTI 카피 박선우 검수
3. Resend API 키 발급 → 문의폼 실제 발송 활성화
4. wknd.kr 도메인 연결 (네이버 DNS)

## 6. 비밀키 / 운영 메모
- `siml-09:/mnt/home3/yhgil99/etc/wkmd/.secretkeys` (chmod 600, 커밋 절대 금지): VERCEL_TOKEN(vcp_), VERCEL_TEAM_ID=team_G3EyDirwC4C0eZg7ORfQwlnH, SANITY_PROJECT_ID=ecfhyeez, SANITY_DATASET=production, SANITY_TOKEN(Editor 쓰기토큰).
- Node는 nvm(v22.20.0)으로만. 모든 작업은 siml-09 NFS에서 (로컬 Windows ✗).
- Vercel GOTCHA: CLI로 만든 빈 프로젝트는 framework=null→404; API로 framework=nextjs PATCH 필요. 팀 SSO 보호도 API로 해제했음.
