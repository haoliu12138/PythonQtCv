import win32GuiUtil

dicts=win32GuiUtil.list_window_names()
for item in dicts.items():
    print(item)