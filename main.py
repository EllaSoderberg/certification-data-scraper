from Scrapers.Europe.TED import run_ted
from Scrapers.Europe.vergabe import run_evergabe

date = "2020-05-05"

print("Running TED...")
run_ted("20200423 <> 20200501", date)
print("Done with TED...")
print("Running Evergabe...")
run_evergabe(date)
print("Done with Evergabe...")
