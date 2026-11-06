import csv, io, socket, urllib.request
_o = socket.getaddrinfo
socket.getaddrinfo = lambda h,p,f=0,*a,**k: [r for r in _o(h,p,socket.AF_INET,*a,**k)]
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0 probe"}), timeout=90) as r:
        return r.read().decode("utf-8", "replace")
for name,u in [
  ("life-expectancy","https://ourworldindata.org/grapher/life-expectancy.csv?csvType=full&useColumnShortNames=true"),
  ("population","https://ourworldindata.org/grapher/population.csv?csvType=full&useColumnShortNames=true"),
]:
    try:
        t=fetch(u); rows=list(csv.DictReader(io.StringIO(t)))
        ys=[int(r["Year"]) for r in rows if r.get("Year","").isdigit()]
        print(name, "rows",len(rows), "years",min(ys),max(ys), "cols", list(rows[0].keys()))
    except Exception as e:
        print(name,"ERR",repr(e)[:120])
