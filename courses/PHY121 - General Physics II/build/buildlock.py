"""
buildlock.py — stop two builds of the SAME course running at once.

Different courses are already safe to build in parallel: every path is derived
from courses/<COURSE>/, so nothing is shared between them. But two chats working
on the SAME course would both run `freeze.py --force` and both write
build/content/ and build/full_manual*.pdf, and the loser's work silently
disappears. This makes that collide loudly instead.

    from buildlock import build_lock
    with build_lock('assemble'):
        ...

A lock whose process is gone is stale and gets taken over, so a crashed build
does not wedge the folder.
"""
import os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(HERE, '.build.lock')


def _alive(pid):
    """Is that pid still running? Used to spot a lock left by a crashed build."""
    if pid == os.getpid():
        return True
    try:
        if sys.platform == 'win32':
            import subprocess
            out = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'],
                                 capture_output=True, text=True, timeout=10).stdout
            return str(pid) in out
        os.kill(pid, 0)
        return True
    except Exception:
        return False


class build_lock:
    def __init__(self, task='build'):
        self.task = task

    def __enter__(self):
        if os.path.exists(LOCK):
            try:
                info = json.load(open(LOCK))
            except Exception:
                info = {}
            pid = info.get('pid', 0)
            if _alive(pid):
                raise SystemExit(
                    f"\nAnother build of this course is already running.\n"
                    f"  task : {info.get('task','?')}\n"
                    f"  pid  : {pid}\n"
                    f"  since: {info.get('started','?')}\n\n"
                    f"Two builds of the same course overwrite each other's content/ and PDF.\n"
                    f"Wait for it to finish, or if you are certain it is dead, delete:\n"
                    f"  {LOCK}\n")
            print(f'note: taking over a stale lock from dead pid {pid}')
        with open(LOCK, 'w') as f:
            json.dump({'pid': os.getpid(), 'task': self.task,
                       'started': time.strftime('%Y-%m-%d %H:%M:%S')}, f)
        return self

    def __exit__(self, *exc):
        try:
            os.remove(LOCK)
        except OSError:
            pass
        return False
