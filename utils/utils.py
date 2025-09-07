import sys, time

from datetime import date, datetime

def slow_print(text, interval=.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(interval)

    sys.stdout.write('\n')

def getchar():
    try:
        import msvcrt
        ch = msvcrt.getch()
        try:
            return ch.decode()
        except UnicodeDecodeError:
            return ch
    except ImportError:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def get_siege_days_passed(current_date=None):
    if current_date is None:
        current_date = date.today()

    start = date(2025, 9, 1)

    return (current_date - start).days

def siege_week(current_date=None):
    week = get_siege_days_passed(current_date) // 7

    if week < 0:
        return "Not started yet"
    elif week < 3:
        return f"Prep Week {week + 1}"
    elif week < 13:
        return f"Siege Week {week - 2}"
    else:
        return "Event finished"
