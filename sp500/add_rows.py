import csv, sys, json
P='press_releases_2012_2026.csv'
def add(new):
    rows=list(csv.DictReader(open(P))); hdr=list(rows[0].keys())
    have={r['url'] for r in rows}
    n=0
    for r in new:
        if r['url'] in have: continue
        rows.append(r); have.add(r['url']); n+=1
    rows.sort(key=lambda r:(r['year'], r['announced']))
    with open(P,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=hdr); w.writeheader(); w.writerows(rows)
    return n, len(rows)
if __name__=='__main__':
    new=json.load(open(sys.argv[1]))
    n,t=add(new); print(f"added {n}, total {t}")
