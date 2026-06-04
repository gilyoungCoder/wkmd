# 선우님용 설치 가이드 (Mac)

> 전체 30분 정도. 막히면 영환에게 스크린샷과 함께 연락.
> 끝나면 "위캔드무드를 아는 Claude"가 생깁니다.

## 0. 준비물

- [x] VSCode 설치 (완료하셨다고 들었습니다)
- [ ] Claude 계정 (https://claude.ai — Pro 구독 권장)
- [ ] GitHub 계정 (영환에게 전달한 그 계정 — 레포 초대 수락 메일 확인!)

## 1. 터미널 열기

`Cmd + Space` → "터미널" 입력 → Enter. 아래 명령들을 한 블록씩 복사-붙여넣기 → Enter.

## 2. 기본 도구 설치 (Homebrew + Git)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- 중간에 비밀번호(Mac 로그인 암호) 물어보면 입력 (화면에 안 보여도 입력되고 있음)
- 끝나면 화면의 **"Next steps"에 나오는 `eval ...` 명령 2줄을 복사해 실행** (Apple Silicon Mac 필수)

```bash
brew install git gh
```

## 3. GitHub 로그인 + 프로젝트 받기

```bash
gh auth login
```
- 질문에: `GitHub.com` → `HTTPS` → `Login with a web browser` → Enter → 브라우저에서 코드 입력

```bash
gh repo clone gilyoungCoder/wkmd ~/wkndmood
cd ~/wkndmood
```

## 4. 나머지 자동 설치 (스크립트 한 방)

```bash
bash scripts/setup.sh
```
- Node.js, Claude Code, yt-dlp(유튜브 수집 도구), oh-my-claudecode를 설치합니다
- 5~10분 걸릴 수 있음. 빨간 에러로 멈추면 스크린샷 → 영환

## 5. Claude 실행 + 로그인

```bash
cd ~/wkndmood
claude
```
- 처음 한 번 브라우저 로그인 진행
- 시작되면 이렇게 입력:

```
/setup-check
```
→ 전부 ✅ 나오면 설치 끝!

## 6. 첫 사용 예시

| 입력 | 결과 |
|---|---|
| `/trend kr` | 한국 유튜브 패션 트렌드 스캔 → 소재 10개 보드 |
| `/content` | 소재 골라서 쓰레드/블로그/인스타 글 생성 |
| `/diagnosis` | 외모진단서 제작 (처음엔 선우님 지식 인터뷰부터) |
| `/mbti LCQV` | 해당 MBTI 타입 콘텐츠 디벨롭 |
| 그냥 자연어 | "동행쇼핑 후기 안내문 써줘" 같은 것도 다 됨 |

## 다음에 또 쓸 때

터미널 열고 ↓ 두 줄이면 끝:
```bash
cd ~/wkndmood
claude
```

## 💡 알아두면 좋은 것

- **brand/tone.md가 품질의 핵심**: 좋아하는 글들을 Claude에게 주면서 "이 톤을 brand/tone.md에 반영해줘" 하시면 점점 똑똑해집니다.
- 작업 결과물은 전부 `outputs/` 폴더에 쌓입니다 (Finder에서 `~/wkndmood/outputs`).
- 영환이 레포를 업데이트하면: `cd ~/wkndmood && git pull` (또는 Claude에게 "최신 버전 받아줘").
