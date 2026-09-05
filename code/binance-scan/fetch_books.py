import json, os, time, concurrent.futures, urllib.request, ssl

base = "/workspace/binance-scan-2340"
depth_dir = f"{base}/depth"
kl_dir = f"{base}/klines_1m"
os.makedirs(depth_dir, exist_ok=True)
os.makedirs(kl_dir, exist_ok=True)
syms = [s.strip() for s in open(f"{base}/symbols.txt") if s.strip() and s.strip().isascii()]
print("n", len(syms))

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (compatible; ResearchDesk/2312)"

def get(url, dest, retries=1):
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                data = r.read()
            if not data or data[:1] not in (b"{", b"["):
                last_err = f"bad body {data[:80]!r}"
                time.sleep(0.3)
                continue
            with open(dest, "wb") as f:
                f.write(data)
            return True, None
        except Exception as e:
            last_err = str(e)
            time.sleep(0.4)
    return False, last_err

def one(sym):
    d_ok, d_err = get(
        f"https://www.binance.com/fapi/v1/depth?symbol={sym}&limit=500",
        f"{depth_dir}/{sym}.json",
    )
    k_ok, k_err = get(
        f"https://www.binance.com/fapi/v1/klines?symbol={sym}&interval=1m&limit=60",
        f"{kl_dir}/{sym}.json",
    )
    return sym, d_ok, d_err, k_ok, k_err

fails = []
ok = 0
t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(one, s) for s in syms]
    for i, fut in enumerate(concurrent.futures.as_completed(futs), 1):
        sym, d_ok, d_err, k_ok, k_err = fut.result()
        if d_ok and k_ok:
            ok += 1
        else:
            fails.append((sym, d_err, k_err))
        if i % 20 == 0 or i == len(syms):
            print(f"progress {i}/{len(syms)} ok={ok} fails={len(fails)} elapsed={time.time()-t0:.1f}s")

print("done ok", ok, "fails", len(fails), "elapsed", round(time.time()-t0, 1))
for row in fails:
    print("FAIL", row)
json.dump({"ok": ok, "fails": fails, "n": len(syms)}, open(f"{base}/fetch_books_log.json", "w"))
