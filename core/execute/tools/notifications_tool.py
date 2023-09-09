import platform

system = platform.system()

if system == 'Windows':
    import win10toast
    toaster = win10toast.ToastNotifier()
    notifications = toaster.get_toast_history()
elif system == 'Darwin':
    import subprocess
    notifications = subprocess.check_output(['osascript', '-e', 'display notification "Test" with title "Title"'])
elif system == 'Linux':
    import subprocess
    notifications = subprocess.check_output(['notify-send', 'Title', 'Test'])

print(notifications)