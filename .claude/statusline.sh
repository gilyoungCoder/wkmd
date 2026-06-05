#!/bin/bash
# WKNDMOOD 브랜딩 상태줄 — Claude Code 터미널 하단 표시
# (프로젝트 설정이 OMC HUD보다 우선 적용됨. stdin으로 세션 JSON이 들어옴)
input=$(cat)

read -r MODEL DIR <<< "$(printf '%s' "$input" | python3 -c "
import json,sys,os
try:
    d=json.load(sys.stdin)
    m=d.get('model',{}).get('display_name') or d.get('model',{}).get('id','')
    w=d.get('workspace',{}).get('current_dir') or d.get('cwd','')
    print((m or 'Claude').replace(' ','·'), os.path.basename(w or '~'))
except Exception:
    print('Claude', '~')
")"

# 골드 브랜드 컬러 + 모노그램
printf '\033[1;38;5;220m◆ WKNDMOOD\033[0m \033[2m│\033[0m \033[38;5;245m%s\033[0m \033[2m│\033[0m \033[38;5;245m%s\033[0m' "${MODEL//·/ }" "$DIR"
