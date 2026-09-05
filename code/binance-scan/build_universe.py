import json
from datetime import datetime, timezone, timedelta

BST = timezone(timedelta(hours=1))
base = "/workspace/binance-scan-2340"
SKIP_HARD = {"CYSUSDT", "SUIUSDT", "TRUMPUSDT", "UAIUSDT"}
FORCE_INCLUDE = {"CRCLUSDT", "XAUUSDT"}  # live seat + stale 2149 recheck
ex = json.load(open(f"{base}/exchangeInfo.json"))
tick = json.load(open(f"{base}/ticker24hr.json"))
info = {}
for s in ex["symbols"]:
    if s.get("contractType") in ("PERPETUAL", "TRADIFI_PERPETUAL") and s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING":
        info[s["symbol"]] = s
print("trading perps", len(info))
tmap = {t["symbol"]: t for t in tick}
univ = []
seen = set()
for sym, meta in info.items():
    if sym in SKIP_HARD:
        continue
    if not sym.isascii():
        continue
    t = tmap.get(sym)
    if not t:
        continue
    qvol = float(t.get("quoteVolume") or 0)
    if qvol < 20e6 and sym not in FORCE_INCLUDE:
        continue
    univ.append({
        "symbol": sym,
        "contractType": meta.get("contractType"),
        "quoteVolume": qvol,
        "priceChangePercent": float(t.get("priceChangePercent") or 0),
        "lastPrice": float(t.get("lastPrice") or 0),
        "forced": sym in FORCE_INCLUDE and qvol < 20e6,
    })
    seen.add(sym)
# Ensure force-includes even if missing from tick filter edge cases
for sym in FORCE_INCLUDE:
    if sym in SKIP_HARD:
        continue
    if sym in seen:
        continue
    meta = info.get(sym)
    t = tmap.get(sym)
    if not meta or not t:
        print("FORCE miss (no meta/tick)", sym)
        continue
    univ.append({
        "symbol": sym,
        "contractType": meta.get("contractType"),
        "quoteVolume": float(t.get("quoteVolume") or 0),
        "priceChangePercent": float(t.get("priceChangePercent") or 0),
        "lastPrice": float(t.get("lastPrice") or 0),
        "forced": True,
    })
    seen.add(sym)
univ.sort(key=lambda x: -x["quoteVolume"])
print("universe n", len(univ))
print("CRCL included", any(u["symbol"]=="CRCLUSDT" for u in univ))
print("XAU included", any(u["symbol"]=="XAUUSDT" for u in univ))
if univ:
    print("min qvol", univ[-1]["quoteVolume"], "max", univ[0]["quoteVolume"])
json.dump(univ, open(f"{base}/universe.json", "w"), indent=2)
with open(f"{base}/symbols.txt", "w") as f:
    for u in univ:
        f.write(u["symbol"] + "\n")
print("wrote symbols", len(univ))
print("tradifi", sum(1 for u in univ if u["contractType"] == "TRADIFI_PERPETUAL"))
print("top 10:")
for u in univ[:10]:
    print(" ", u["symbol"], round(u["quoteVolume"] / 1e6, 1), "M", u["contractType"])
print("now_bst", datetime.now(BST).isoformat())
