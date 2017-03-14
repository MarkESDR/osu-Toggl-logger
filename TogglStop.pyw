from TogglApi import TogglAPI, TogglConfig

cfg = TogglConfig(cfg_path="Settings.txt")

f = open("tid", "r")
tid = int(f.readline())
f.close()

t = TogglAPI(cfg.API_TOKEN)
r = t._stop_time_entry(tid)

#exec(open("TogglStart.pyw").read())