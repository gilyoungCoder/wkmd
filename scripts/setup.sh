#!/bin/bash
# WKND MOOD 에이전트 환경 자동 설치 (Mac용, 멱등 — 여러 번 실행해도 안전)
set -uo pipefail

ok()   { printf "  \033[32m✅ %s\033[0m\n" "$1"; }
info() { printf "  \033[36m▸ %s\033[0m\n" "$1"; }
fail() { printf "  \033[31m❌ %s\033[0m\n" "$1"; }

echo "=== WKND MOOD 환경 설치 시작 ==="

# 0. Homebrew (SETUP_GUIDE 2단계에서 설치됨 — 여기선 확인만)
if ! command -v brew >/dev/null 2>&1; then
  # Apple Silicon 기본 경로 시도
  [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
  [ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"
fi
if ! command -v brew >/dev/null 2>&1; then
  fail "Homebrew가 없습니다. SETUP_GUIDE.md 2단계를 먼저 진행해주세요."
  exit 1
fi
ok "Homebrew"

# 1. 필수 패키지
info "필수 패키지 설치 중 (node, python, yt-dlp, ffmpeg)..."
for pkg in node python yt-dlp ffmpeg jq; do
  brew list "$pkg" >/dev/null 2>&1 || brew install "$pkg"
done
ok "node $(node --version 2>/dev/null) / yt-dlp $(yt-dlp --version 2>/dev/null)"

# 2. Claude Code
if ! command -v claude >/dev/null 2>&1; then
  info "Claude Code 설치 중..."
  npm install -g @anthropic-ai/claude-code
fi
ok "Claude Code $(claude --version 2>/dev/null | head -1)"

# 3. oh-my-claudecode (에이전트 오케스트레이션)
if ! command -v omc >/dev/null 2>&1; then
  info "oh-my-claudecode 설치 중..."
  npm install -g oh-my-claudecode
fi
if command -v omc >/dev/null 2>&1; then
  ok "oh-my-claudecode $(omc --version 2>/dev/null | head -1)"
  info "Claude 첫 실행 후 'setup omc'라고 입력하면 마무리 세팅이 됩니다."
else
  fail "omc 설치 실패 — 일단 Claude Code만으로도 모든 기능이 동작합니다. (영환에게 알려주세요)"
fi

# 4. 작업 폴더 준비
cd "$(dirname "$0")/.." || exit 1
mkdir -p data/trends data/subs outputs/content outputs/diagnosis outputs/review outputs/trends
ok "작업 폴더 (data/, outputs/)"

# 5. 빠른 자가진단
echo ""
echo "=== 자가진단 ==="
command -v python3 >/dev/null && ok "python3" || fail "python3"
command -v yt-dlp  >/dev/null && ok "yt-dlp"  || fail "yt-dlp"
command -v claude  >/dev/null && ok "claude"  || fail "claude"
[ -f brand/tone.md ] && ok "brand/ 컨텍스트 파일" || fail "brand/ 파일 없음 — git pull 필요?"

echo ""
echo "=== 설치 완료! ==="
echo "다음 명령으로 시작하세요:"
echo "  claude"
echo "그리고 Claude 안에서:  /setup-check"
