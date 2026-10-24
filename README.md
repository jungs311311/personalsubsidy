# 내 지원금 찾기 (전국 + 대구·경북)

나이·가족·집·소득을 고르면 받을 수 있는 개인 지원금을 한 화면에 보여주는 웹페이지입니다.

- `index.html` — 페이지 전체 (직접 정리한 지원 67개 + 판정 규칙 + 신청 기간)
- `data/benefits.json` — 보조금24(행정안전부) API 데이터. GitHub Actions가 매일 새벽 6시 자동 갱신
- `scripts/fetch_api.py` — API에서 개인 대상 · 전국/대구/경북 사업만 골라 저장
- `.github/workflows/update-data.yml` — 매일 자동 실행 설정

## 설정
1. Settings → Secrets and variables → Actions → `GOV24_KEY` 에 공공데이터포털 일반 인증키
2. Settings → Pages → Branch: `main` / `(root)`

입력한 개인정보는 저장하지 않고 브라우저 안에서만 계산합니다. 실제 자격은 각 기관 공고로 확인해야 합니다.
