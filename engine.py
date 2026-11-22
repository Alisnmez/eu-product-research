"""Conservative evidence-first discovery scaffold. No fabricated product records."""
import argparse,datetime,json,sqlite3,hashlib,urllib.request,urllib.robotparser,time
from pathlib import Path
DB='research.sqlite3'
def connect(path):
 c=sqlite3.connect(path);c.execute('CREATE TABLE IF NOT EXISTS evidence (url TEXT PRIMARY KEY, category TEXT, checked_at TEXT, status TEXT, title TEXT, sha256 TEXT)');c.execute('CREATE TABLE IF NOT EXISTS runs (at TEXT, checked INTEGER, errors INTEGER)');c.commit();return c
def run(db,config):
 c=connect(db);sources=json.loads(Path(config).read_text());checked=errors=0
 for s in sources:
  if not s.get('enabled') or not s.get('permission_confirmed'):continue
  url=s['url'];status='error';title='';digest=''
  try:
   from urllib.parse import urlsplit
   u=urlsplit(url);robots=urllib.robotparser.RobotFileParser();robots.set_url(f'{u.scheme}://{u.netloc}/robots.txt');robots.read()
   if not robots.can_fetch('EUProductResearchBot',url):status='robots_disallowed'
   else:
    req=urllib.request.Request(url,headers={'User-Agent':'EUProductResearchBot/0.1 (contact: research-owner)'})
    with urllib.request.urlopen(req,timeout=15) as response: raw=response.read(250000)
    digest=hashlib.sha256(raw).hexdigest();title=raw.decode('utf-8','replace').split('<title>')[-1].split('</title>')[0][:200] if b'<title>' in raw else '';status='fetched'
  except Exception:errors+=1
  c.execute('INSERT OR REPLACE INTO evidence VALUES (?,?,?,?,?,?)',(url,s.get('category','unknown'),datetime.datetime.now(datetime.timezone.utc).isoformat(),status,title,digest));c.commit();checked+=1;time.sleep(2)
 c.execute('INSERT INTO runs VALUES (?,?,?)',(datetime.datetime.now(datetime.timezone.utc).isoformat(),checked,errors));c.commit();print(json.dumps({'sources_checked':checked,'errors':errors,'verified_products':0}))
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['run','status']);p.add_argument('--db',default=DB);p.add_argument('--config',default='sources.json');a=p.parse_args();c=connect(a.db)
 if a.action=='status':print(json.dumps({'source_records':c.execute('SELECT count(*) FROM evidence').fetchone()[0],'verified_products':0}))
 else:run(a.db,a.config)
if __name__=='__main__':main()
