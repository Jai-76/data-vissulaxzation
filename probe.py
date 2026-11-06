import json, socket, urllib.request
_o = socket.getaddrinfo
socket.getaddrinfo = lambda h,p,f=0,*a,**k: [r for r in _o(h,p,socket.AF_INET,*a,**k)]
B="https://api.worldbank.org/v2"
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"probe"}), timeout=60) as r:
        return json.load(r)
IND={"gdp_ppp":"NY.GDP.PCAP.PP.CD","gdp_const":"NY.GDP.PCAP.KD","life":"SP.DYN.LE00.IN",
     "pop":"SP.POP.TOTL","co2":"EN.GHG.CO2.PC.CE.AR5","fert":"SP.DYN.TFRT.IN",
     "mort":"SH.DYN.MORT","urban":"SP.URB.TOTL.IN.ZS","energy":"EG.USE.PCAP.KG.OE"}
for k,c in IND.items():
    d=get(f"{B}/country/all/indicator/{c}?format=json&date=2023:2026&per_page=20000")
    rows=[r for r in d[1] if r["value"] is not None]
    from collections import Counter
    cnt=Counter(r["date"] for r in rows)
    print(f"{k:10s} {c:22s} lastupdated={d[0]['lastupdated']} " + "  ".join(f"{y}:{cnt.get(y,0)}" for y in ["2023","2024","2025","2026"]))
