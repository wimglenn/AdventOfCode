import fileinput
import io
import pathlib
import runpy
import sys
import tempfile


def plugin(year, day, data):
    script = pathlib.Path(__file__).parent / f"{year}" / f"{day}.py"
    if not script.exists():
        raise Exception(f"script not found: {script}")
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    if year == 2020:
        # these scripts are using fileinput module
        mod = type("FakeFileInput", (), {"input": lambda: iter(data.splitlines())})
        sys.modules["fileinput"] = mod
        try:
            runpy.run_path(script)
            txt = sys.stdout.getvalue()
        finally:
            sys.modules["fileinput"] = fileinput
            sys.stdout = old_stdout
    else:
        # these scripts are reading from a filename directly
        old_sys_argv = sys.argv[:]
        with tempfile.NamedTemporaryFile("wt") as f:
            sys.argv = [f"{day}.py", f.name]
            f.write(data)
            f.flush()
            try:
                runpy.run_path(script)
                txt = sys.stdout.getvalue()
            finally:
                sys.argv = old_sys_argv
                sys.stdout = old_stdout
    parts = txt.split()
    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        # assume part A only completed so far
        return parts[0], ""
    else:
        # assume answers are on the last 2 lines
        return parts[-2], parts[-1]
