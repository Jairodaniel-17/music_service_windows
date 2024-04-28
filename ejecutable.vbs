Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe app.py", 0, False
Set WshShell = Nothing
