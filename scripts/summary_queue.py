"""요약할 지원 목록을 조회수 순으로 뽑습니다 (매일 9시 작업이 사용).

사용: python scripts/summary_queue.py 150 > queue.json
- data/summaries.json 에 이미 있고 원문이 바뀌지 않은 항목은 건너뜁니다 (h = 원문 해시).
- 대구·경북 2/3, 전국 1/3을 각각 조회수 순으로 섞어서 뽑습니다.
"""
import hashlib, json, os, re, sys

D = os.path.join(os.path.dirname(__file__), "..", "data")


def load(name):
    p = os.path.join(D, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"items": []}


def h(*parts):
    return hashlib.md5("|".join(p or "" for p in parts).encode("utf-8")).hexdigest()[:10]


def base(n):
    return re.sub(r"[\s()·\-–_,.\[\]]", "", re.sub(r"\(.*?\)", "", n or ""))


def rows():
    for x in load("benefits.json")["items"]:
        yield {"sid": "g:" + x["id"], "name": x["name"], "reg": x["reg"], "views": int(x.get("views") or 0),
               "text": {"내용": x.get("content"), "대상": x.get("target"), "선정기준": x.get("criteria"), "신청방법": x.get("how"), "접수기관": x.get("recv")}}
    for x in load("bokjiro.json")["items"]:
        yield {"sid": "b:" + x["servId"], "name": x["servNm"], "reg": "전국", "views": int(x.get("inqNum") or 0),
               "text": {"내용": x.get("servDgst"), "생애주기": x.get("lifeArray"), "대상": x.get("trgterIndvdlArray")}}
    for x in load("local.json")["items"]:
        reg = "대구" if (x.get("ctpvNm") or "").startswith("대구") else "경북"
        yield {"sid": "l:" + x["servId"], "name": x["servNm"], "reg": reg, "views": int(x.get("inqNum") or 0),
               "text": {"내용": x.get("servDgst"), "생애주기": x.get("lifeNmArray") or x.get("lifeArray"), "신청방법": x.get("aplyMtdNm"), "지역": x.get("sggNm")}}
    for x in load("youth.json")["items"]:
        yield {"sid": "y:" + str(x.get("plcyNo")), "name": x.get("plcyNm"), "reg": x["reg"], "views": int(x.get("inqCnt") or 0),
               "text": {"설명": x.get("plcyExplnCn"), "지원내용": x.get("plcySprtCn"), "나이": f'{x.get("sprtTrgtMinAge","")}~{x.get("sprtTrgtMaxAge","")}',
                        "추가자격": x.get("addAplyQlfcCndCn"), "신청방법": x.get("plcyAplyMthdCn")}}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    done = load("summaries.json").get("items", {})
    seen, out = set(), []
    for r in rows():
        if not r["name"] or re.search(r"테스트|시연", r["name"]):
            continue
        k = base(r["name"]) + r["reg"]
        if k in seen:
            continue
        seen.add(k)
        r["h"] = h(*[str(v) for v in r["text"].values()])
        if r["sid"] in done and done[r["sid"]].get("h") == r["h"]:
            continue
        r["text"] = {a: b for a, b in r["text"].items() if b and b != "~"}
        out.append(r)
    # 대구·경북 2/3 + 전국 1/3, 각각 조회수 순
    loc = sorted([r for r in out if r["reg"] != "전국"], key=lambda r: -r["views"])
    nat = sorted([r for r in out if r["reg"] == "전국"], key=lambda r: -r["views"])
    nl = min(len(loc), n * 2 // 3)
    pick = loc[:nl] + nat[: n - nl]
    pick += loc[nl: nl + (n - len(pick))]
    json.dump(pick, sys.stdout, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
