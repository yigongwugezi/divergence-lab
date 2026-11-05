"""Recompute published results from archived verdicts; no model calls."""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    release = read(ROOT / "VERSION.json")
    selection = sys.argv[1] if len(sys.argv) > 1 else re.search(
        r"candidate(\d+)-", release["source_candidate"]).group(1)
    version = 16 if selection == "new12" else int(selection)
    directory = (ROOT / "evidence/frozen16-new12" if selection == "new12" else
                 ROOT / "evidence/iterations" / f"candidate{version}")
    summary = read(directory / "summary.json")
    if selection == "new12":
        freeze = read(directory / "FREEZE.json")
        assert digest(directory / "TASKS.json") == freeze["task_index_sha256"]
        assert digest(ROOT / "evidence/iterations/JUDGE_PROMPT.txt") == freeze["judge_sha256"]
    provenance = read(directory / "PROVENANCE.json")
    for item in provenance:
        assert digest(directory / item["export"]) == item["export_sha256"], item["export"]
    votes = Counter()
    mechanisms = Counter()
    complete = passed = 0
    failed = []
    for tid, row in summary["tasks"].items():
        if row["status"] != "complete":
            continue
        complete += 1
        task_votes = []
        eligible = not row.get("format_errors", [])
        for order in (1, 2):
            verdict = read(directory / "tasks" / tid / f"judge{order}.json")
            mapping, answer = verdict["mapping"], verdict["answer"]
            pools = {mapping[label]: pool for label, pool in answer["pools"].items()}
            winner = answer["pair"]["winner"]
            vote = "T" if winner == "tie" else "W" if mapping[winner] == "EXPAND" else "L"
            task_votes.append(vote)
            votes[vote] += 1
            expand = len(pools["EXPAND"]["groups"])
            direct = len(pools["DIRECT_FULL"]["groups"])
            mechanisms["higher" if expand > direct else "equal" if expand == direct else "lower"] += 1
            eligible &= expand >= direct and not pools["EXPAND"]["serious_violations"]
            assert vote == row["candidate"][order - 1]["vote"], (tid, order)
        is_pass = bool(eligible and "W" in task_votes and "L" not in task_votes)
        assert is_pass == row["pass"], tid
        passed += is_pass
        if not is_pass:
            failed.append(tid)
    assert complete == summary["complete_count"]
    assert passed == summary["pass_count"]
    assert dict(votes) == {k: v for k, v in summary["votes"].items() if v}
    assert sorted(failed) == sorted(summary["failed_ids"])
    if release["source_candidate"] == f"superiority-candidate{version}-20261103":
        for relative, expected in release["files"].items():
            assert digest(ROOT / relative) == expected, relative
    print(json.dumps({"candidate": version, "dataset": selection, "completed": complete,
                      "passed": passed, "votes": dict(votes), "failed_ids": failed,
                      "mechanism_reviews": dict(mechanisms),
                      "verified_export_hashes": len(provenance),
                      "scope": "Recomputes archived judgments and verifies bytes; does not rerun models or measure field outcomes."},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
