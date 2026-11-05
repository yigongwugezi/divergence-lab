"""Run one task's P0, exploration, or refinement using isolated requests."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from build_prompt import candidates

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
SCHEMA = ROOT / "references/response.schema.json"


def prompt(phase, task, p0=None, p1=None, prior=()):
    if phase == "P0":
        source = ROOT / "references/BASELINE_PROMPT.txt"
        history = None
    elif phase == "REFINE":
        source = ROOT / "references/REPAIR_PROMPT.txt"
        history = [{"index": i, **row} for i, row in enumerate(
            candidates(p0) + list(prior) + candidates(p1))]
    elif phase in {"EXPAND_P1", "EXPAND_P2"}:
        narrow = len(candidates(p0)) < 3
        source = ROOT / "references" / (
            ("CONTINUE_PROMPT_P1_NARROW.txt" if narrow else "CONTINUE_PROMPT_P1.txt")
            if phase == "EXPAND_P1" else
            ("CONTINUE_PROMPT_P2_ASSUMPTION.txt" if narrow else "CONTINUE_PROMPT_P2.txt"))
        history = ([{"index": i, **row} for i, row in enumerate(candidates(p0))] + list(prior)
                   if phase == "EXPAND_P1" else
                   [{"index": i, "title": row["title"], "proposal": row["proposal"]}
                    for i, row in enumerate(candidates(p0))] +
                   [{"title": row["title"], "proposal": row["proposal"]} for row in prior] +
                   [{"title": row["title"], "proposal": row["proposal"]}
                    for row in candidates(p1, 6)])
    elif phase in {"SAVE_P1", "SAVE_P2"}:
        wide = len(candidates(p0)) == 3
        source = ROOT / "references" / (
            "SAVE_WIDE_PROMPT.txt" if phase == "SAVE_P1" and wide else "SAVE_FULL_PROMPT.txt")
        history = ([{"index": i, **row} for i, row in enumerate(candidates(p0))] +
                   [{"index": i + len(candidates(p0)), **row} for i, row in enumerate(prior)]
                   if phase == "SAVE_P1" else
                   [{"index": i, **row} for i, row in enumerate(
                       candidates(p0) + list(prior) + candidates(p1))])
    else:
        source = ROOT / "references/CONTINUE_PROMPT.txt"
        history = ([{"index": i, **row} for i, row in enumerate(candidates(p0))] + list(prior)
                   if phase == "P1" else
                   [{"index": i, "title": row["title"], "proposal": row["proposal"]}
                    for i, row in enumerate(candidates(p0))] +
                   [{"title": row["title"], "proposal": row["proposal"]} for row in prior] +
                   [{"title": row["title"], "proposal": row["proposal"]}
                   for row in candidates(p1, 6)])
    result = source.read_text(encoding="utf-8").replace(
        "{TASK}", json.dumps(task, ensure_ascii=False))
    return result if history is None else result.replace(
        "{HISTORY}", json.dumps(history, ensure_ascii=False))


def generate(text, destination, limit=3, model=None):
    executable = shutil.which("codex")
    if not executable:
        raise RuntimeError("No independent Codex CLI request channel is available")
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "response.json"
        command = [executable, "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only"]
        if model:
            command.extend(["--model", model])
        command.extend(["--output-schema", str(SCHEMA if limit == 3 else ROOT / "references/response6.schema.json"),
                        "-o", str(output), "-"])
        try:
            call = subprocess.run(
                command,
                input=text, text=True, encoding="utf-8", capture_output=True,
                cwd=ROOT, check=False, timeout=300)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("Independent request timed out after 300 seconds; saved rounds remain available") from error
        if call.returncode:
            raise RuntimeError(f"Independent request failed ({call.returncode}): {call.stderr[-1200:]}")
        rows = candidates(output, limit)
        destination.write_text(json.dumps({"candidates": rows}, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "continue", "refine", "expand", "save"])
    parser.add_argument("task", type=Path, help="agent-maintained task JSON, never required from the user")
    parser.add_argument("--model", help="Codex CLI model override when the local default is unavailable")
    args = parser.parse_args()
    task = json.loads(args.task.read_text(encoding="utf-8"))
    if (not isinstance(task, dict) or not isinstance(task.get("goal"), str) or not task["goal"]
            or not isinstance(task.get("hard_constraints"), list)
            or any(not isinstance(x, str) for x in task["hard_constraints"])):
        parser.error("task requires goal and hard_constraints string list")
    digest = hashlib.sha256(json.dumps(task, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    folder = STATE / digest
    folder.mkdir(parents=True, exist_ok=True)
    saved_task = folder / "task.json"
    if saved_task.exists() and json.loads(saved_task.read_text(encoding="utf-8")) != task:
        parser.error("task hash collision")
    saved_task.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    p0 = folder / "p0.json"
    if args.action == "start":
        if not p0.exists():
            generate(prompt("P0", task), p0, model=args.model)
    else:
        if not p0.exists():
            parser.error("no complete first pass for this exact task; run start")
        rounds = sorted(folder.glob("continue-*"))
        round_dir = (rounds[-1] if rounds and not (rounds[-1] / "done.txt").exists()
                     and not (rounds[-1] / "p2.json").exists()
                     else folder / f"continue-{len(rounds) + 1:03d}")
        round_dir.mkdir(exist_ok=True)
        mode_file = round_dir / "mode.txt"
        if mode_file.exists() and mode_file.read_text(encoding="utf-8") != args.action:
            parser.error("finish the interrupted continuation in its original mode first")
        if not mode_file.exists():
            mode_file.write_text(args.action, encoding="utf-8")
        p1, p2 = round_dir / "p1.json", round_dir / "p2.json"
        prior = [row for past in rounds if past != round_dir and
                 ((past / "done.txt").exists() or (past / "p2.json").exists())
                 for phase in ("p1", "p2") if (past / f"{phase}.json").exists()
                 for row in candidates(past / f"{phase}.json", 6)]
        if not p1.exists():
            generate(prompt("EXPAND_P1" if args.action == "expand" else
                            "SAVE_P1" if args.action == "save" else "P1", task, p0, prior=prior),
                     p1, 6 if args.action in {"expand", "save"} and len(candidates(p0)) == 3 else 3,
                     model=args.model)
        if not (args.action == "save" and len(candidates(p0)) == 3) and not p2.exists():
            generate(prompt("REFINE" if args.action == "refine" else
                            "EXPAND_P2" if args.action == "expand" else
                            "SAVE_P2" if args.action == "save" else "P2",
                            task, p0, p1, prior=prior), p2, model=args.model)
        (round_dir / "done.txt").write_text("complete", encoding="utf-8")
    files = [p0] + [path for past in sorted(folder.glob("continue-*"))
                    for phase in ("p1", "p2") if (path := past / f"{phase}.json").exists()]
    print(json.dumps({"task_state": str(folder), "rounds": [
        {"round": 0 if path == p0 else int(path.parent.name.split("-")[1]),
         "phase": ((path.parent / "mode.txt").read_text(encoding="utf-8").upper()
                   if (path.parent / "mode.txt").exists() and
                   ((path.stem == "p2" and
                     (path.parent / "mode.txt").read_text(encoding="utf-8") in {"refine", "expand", "save"})
                    or (path.stem == "p1" and
                        (path.parent / "mode.txt").read_text(encoding="utf-8") == "save" and
                        not (path.parent / "p2.json").exists()))
                   else path.stem.upper()), "candidates": candidates(path, 6)} for path in files
    ]}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
