"""Check frozen runner state with archived N01 responses; makes no model requests."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


WORK = Path(__file__).resolve().parents[1]
SCRIPT = WORK / ".agents/skills/divergence-lab-unified/scripts"
QUALITY = WORK / "evidence/usability/replay"
sys.path.insert(0, str(SCRIPT))
import run  # noqa: E402


def invoke(action, task_file):
    sys.argv = [str(SCRIPT / "run.py"), action, str(task_file)]
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        run.main()
    return json.loads(output.getvalue())


def main():
    task = json.loads((QUALITY / "TASKS.json").read_text(encoding="utf-8"))[0]
    calls = QUALITY / "runs/N01/calls"
    fixtures = [
        "b6826246ee002ba19b67",  # P0: two candidates
        "f088e1d187e63a4cc7ae",  # expand P1: no candidates
        "0f6fb7a2757ef5357291",  # expand P2: two candidates
        "f088e1d187e63a4cc7ae",  # save P1 replay: no candidates
        "0f6fb7a2757ef5357291",  # save P2 replay: two candidates
    ]
    with tempfile.TemporaryDirectory() as scratch:
        scratch = Path(scratch)
        task_file = scratch / "task.json"
        task_file.write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8")
        run.STATE = scratch / "state"
        original_generate = run.generate

        def replay(_text, destination, limit=3):
            rows = json.loads((calls / f"{fixtures.pop(0)}.json").read_text(encoding="utf-8"))
            assert len(rows) <= limit
            destination.write_text(json.dumps({"candidates": rows}, ensure_ascii=False), encoding="utf-8")

        run.generate = replay
        try:
            first = invoke("start", task_file)
            expanded = invoke("expand", task_file)
            saved = invoke("save", task_file)
            assert not fixtures
            assert [len(x["candidates"]) for x in first["rounds"]] == [2]
            assert [len(x["candidates"]) for x in expanded["rounds"]] == [2, 0, 2]
            assert [len(x["candidates"]) for x in saved["rounds"]] == [2, 0, 2, 0, 2]
            assert all(x in saved["rounds"] for x in expanded["rounds"])

            state = Path(saved["task_state"])
            p0, p1 = state / "p0.json", state / "continue-001/p1.json"
            for phase in ("P0", "P1", "P2", "REFINE", "EXPAND_P1", "EXPAND_P2", "SAVE_P1", "SAVE_P2"):
                rendered = run.prompt(phase, task, p0, p1)
                assert task["goal"] in rendered and "{TASK}" not in rendered and "{HISTORY}" not in rendered
            for schema, count in ((run.SCHEMA, 3), (run.ROOT / "references/response6.schema.json", 6)):
                assert json.loads(schema.read_text(encoding="utf-8"))["properties"]["candidates"]["maxItems"] == count

            code = (
                "import json,sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); "
                "import run; run.STATE=Path(sys.argv[2]); sys.argv=['run.py','start',sys.argv[3]]; run.main()"
            )
            resumed = subprocess.run(
                [sys.executable, "-c", code, str(SCRIPT), str(run.STATE), str(task_file)],
                capture_output=True, text=True, encoding="utf-8", check=True,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            assert json.loads(resumed.stdout)["rounds"] == saved["rounds"]

            changed = dict(task, goal=task["goal"] + " Changed task.")
            task_file.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    invoke("continue", task_file)
                except SystemExit as error:
                    assert error.code == 2
                else:
                    raise AssertionError("changed task continued old state")
            assert json.loads((state / "p0.json").read_text(encoding="utf-8"))["candidates"] == first["rounds"][0]["candidates"]
        finally:
            run.generate = original_generate
    print("PASS: state, history, task guard, modes, schemas, and new-process resume (archived replay)")


if __name__ == "__main__":
    main()
