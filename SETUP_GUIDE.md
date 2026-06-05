# 선우님용 설치 가이드 (Mac)

> 전체 30~40분. 순서대로 한 블록씩 복사 → 터미널에 붙여넣기 → Enter.
> 막히면 화면 스크린샷과 함께 영환에게 연락. 끝나면 터미널 하단에 **◆ WKNDMOOD** 가 뜨는, "위캔드무드를 아는 Claude"가 생깁니다.

## 0. 준비물

- [x] VSCode 설치 (완료)
- [x] Claude 계정 — **MAX 구독** (완료!)
- GitHub 로그인은 **지금은 불필요** (설치 기간 동안 레포를 공개로 열어둠 — 로그인 없이 받아짐). 초대 수락은 나중에 비공개 전환 후를 위해 해두면 좋음.

## 1. 터미널 열기

`Cmd + Space` → "터미널" 입력 → Enter

## 2. Homebrew 설치 (Mac 패키지 관리자 — 모든 것의 토대)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

⚠️ 두 가지만 주의:
- 중간에 비밀번호를 물으면 **Mac 로그인 암호** 입력 (화면에 안 보여도 입력되는 중)
- 끝나면 화면 "Next steps:"에 나오는 **`eval` 로 시작하는 명령 2줄을 복사해 실행** (Apple Silicon 필수 — 안 하면 brew 명령을 못 찾습니다)

확인:
```bash
brew --version
```
→ `Homebrew 4.x` 처럼 나오면 성공

## 3. Git 설치

```bash
brew install git
```

## 4. Node.js 설치 (npm 포함)

```bash
brew install node
```

확인:
```bash
node --version && npm --version
```
→ 버전 두 줄이 나오면 성공

## 5. Claude Code 설치 (npm으로)

```bash
npm install -g @anthropic-ai/claude-code
```

확인:
```bash
claude --version
```

## 6. oh-my-claudecode(OMC) 설치 (에이전트 엔진)

```bash
npm install -g oh-my-claudecode
omc setup
```

- `omc setup` 중 질문이 나오면 기본값(Enter)으로 진행하면 됩니다
- ※ 내부 엔진은 OMC지만, 우리 프로젝트 안에서는 화면 하단 브랜딩이 **WKNDMOOD**로 표시됩니다 (8단계에서 확인)

## 7. 위캔드무드 레포 클론 ⭐ 핵심 (로그인 불필요)

```bash
git clone https://github.com/gilyoungCoder/wkmd.git ~/wkndmood
cd ~/wkndmood
bash scripts/setup.sh
```

- `setup.sh`는 빠진 도구(yt-dlp 등)를 채우고 작업 폴더를 만드는 마무리 점검입니다 (2~6단계를 했으면 금방 끝남)

## 8. 실행 — 여기서부터는 항상 이 두 줄

```bash
cd ~/wkndmood
claude
```

- 처음 한 번 브라우저 로그인
- **터미널 하단에 `◆ WKNDMOOD │ 모델명 │ wkndmood` 가 보이면 브랜딩까지 완벽 적용** ✨
- 시작되면 입력:

```
/setup-check
```
→ 전부 ✅ 면 설치 완료!

## 9. 첫 사용 추천 코스

| 순서 | 입력 | 결과 |
|---|---|---|
| 1 | `/trend kr` | 한국 유튜브 패션 트렌드 → 소재 보드 ("오 된다" 체험) |
| 2 | 좋아하는 글 붙여넣고 "이 톤을 tone.md에 반영해줘" | 글 품질의 기준 학습 |
| 3 | `/diagnosis` | 외모진단 기준 인터뷰 (선우님 노하우 → AI 이식) |
| 4 | `/exp 오늘 고객이 ○○했는데` | 경험 30초 기록 → 모든 글의 재료가 됨 |

## 문제 해결

| 증상 | 해결 |
|---|---|
| `command not found: brew` | 2단계의 eval 2줄 실행 누락 — Homebrew 설치 마지막 화면 참조 |
| `command not found: claude` | 터미널 껐다 켜기 → 그래도 안 되면 5단계 재실행 |
| 클론할 때 404/권한 오류 | 레포가 비공개로 돌아간 경우 — 영환에게 연락 (또는 GitHub 초대 수락 후 로그인 클론) |
| 하단에 WKNDMOOD 안 뜸 | `cd ~/wkndmood` 안에서 `claude`를 실행했는지 확인 (프로젝트 폴더 안에서만 적용) |
| 그 외 | Claude에게 그대로 물어보기 → 안 되면 `/setup-check` 결과 캡처 → 영환 |

## 다음에 또 쓸 때 — `wknd` 한 단어면 끝 ⭐

설치(7단계 setup.sh)가 끝나면 **새 터미널부터** 어디서든:

```bash
wknd              # 시작 — WKND MOOD 로고와 함께 바로 작업 폴더에서 실행
wknd --madmax     # 풀 자율 모드 (권한 질문 생략 — 익숙해진 뒤 추천)
wknd update       # 영환이 업데이트했다고 하면 이걸로 최신 버전 받기
wknd "/trend kr"  # 시작하자마자 트렌드 스캔까지 한 번에
```

- `cd` 할 필요 없음 — 어느 폴더에 있든 알아서 워크스페이스로 이동해 실행됩니다
- ⚠️ 설치 직후엔 터미널을 **한 번 새로 열어야** `wknd`가 인식됩니다
