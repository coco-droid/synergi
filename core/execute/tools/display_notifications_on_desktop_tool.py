import platform
import redis

def display_notification(title, message):
    system = platform.system()

    if system == 'Windows':
        import win10toast
        toaster = win10toast.ToastNotifier()
        shown = toaster.show_toast(title, message)
    elif system == 'Darwin':
        import subprocess
        shown = subprocess.call(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
    elif system == 'Linux':
        import subprocess
        shown = subprocess.call(['notify-send', title, message])

    if shown:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.rpush('notifications', f'{title}: {message}')
        return True
    else:
        return False