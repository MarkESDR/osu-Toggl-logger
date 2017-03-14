SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

isPlaying := False
ticks := A_TickCount

while true {
	if (ticks+100 <= A_TickCount 
	  && WinActive("ahk_exe osu!.exe")) {
		ticks := A_TickCount
		WinGetText, visText, A
		WinGetTitle, winTit, A
		if (InStr(winTit, "-")>0 
			&& RegExMatch(visText, "menuStrip1")==0) {
			if (!isPlaying) {
				Desc := SubStr(winTit, RegExMatch(winTit, " - ")+3)
				Run, TogglStart.pyw %Desc%
			}
			isPlaying := True
			checkTime := 0
		} else if (isPlaying && checkTime == 0)
			checkTime := A_TickCount
		else if (isPlaying 
			&& checkTime+500 <= A_TickCount) {
			isPlaying := False
			Run, TogglStop.pyw
			checkTime := 0
		}
	}
}
