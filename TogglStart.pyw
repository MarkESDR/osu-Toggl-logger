import sys

from TogglApi import TogglAPI, TogglConfig

cfg = TogglConfig(cfg_path="Settings.txt")

desc = cfg.DEFAULT_DESCRIPTION
if len(sys.argv)>1 and cfg.SONG_AS_DESCRIPTION:
	desc = ""
	for i in range(1, len(sys.argv)):
		desc += ' '+sys.argv[i]

t = TogglAPI(cfg.API_TOKEN)
r = t._start_time_entry(description=desc, pid=cfg.PID, program_name='osu! timer')

f = open("tid", "w+")
f.write(str(r["data"]["id"]))
f.close()