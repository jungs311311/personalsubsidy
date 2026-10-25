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

## 직접 관리하는 72개 지원 기준 (구글 시트)

- 시트: Google Drive "개인 보조금" 폴더의 **개인 보조금 기준표** (링크가 있는 모든 사용자 보기로 공유)
- 탭: 지원목록(글·신청 기간), 기준값(나이·소득 %·한도 숫자), 중위소득(연도별), 새 지원, 변경기록, 설정
- `.github/workflows/sheet-sync.yml` 이 매시 17분에 `scripts/fetch_sheet.py` 로 시트를 읽어 `data/manual.json` 을 만듭니다.
- 값이 이상하면(숫자 칸에 글자, 기본값의 1/3~3배를 벗어남, 날짜 형식 오류) 그 칸은 버리고 코드 기본값을 씁니다.
- 매주 월요일 Claude 예약 작업이 기준을 웹에서 확인해 시트를 고치고 변경기록에 남깁니다.
