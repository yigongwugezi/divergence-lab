"""Render the frozen new-task batch from saved verdicts, without model calls."""
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/frozen16-new12"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    summary = read(DATA / "summary.json")
    assert summary["complete_count"] == summary["task_count"] == 12
    votes, labels, direct, expand, letters = Counter(), [], [], [], []
    for tid, row in summary["tasks"].items():
        pairs, task_votes = [], []
        for order in (1, 2):
            verdict = read(DATA / "tasks" / tid / f"judge{order}.json")
            mapping, answer = verdict["mapping"], verdict["answer"]
            counts = {mapping[label]: len(pool["groups"]) for label, pool in answer["pools"].items()}
            winner = answer["pair"]["winner"]
            vote = "T" if winner == "tie" else "W" if mapping[winner] == "EXPAND" else "L"
            assert vote == row["candidate"][order - 1]["vote"]
            votes[vote] += 1
            task_votes.append(vote)
            pairs.append(counts)
        labels.append(tid)
        direct.append(sum(p["DIRECT_FULL"] for p in pairs) / 2)
        expand.append(sum(p["EXPAND"] for p in pairs) / 2)
        letters.append(" / ".join(task_votes) + ("  PASS" if row["pass"] else "  OPEN"))
    assert dict(votes) == {k: v for k, v in summary["votes"].items() if v}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(10, 8), facecolor="#faf8f3")
    ax.set_facecolor("#faf8f3")
    for y, (d, e) in enumerate(zip(direct, expand)):
        ax.plot([d, e], [y, y], color="#c4bfb1", linewidth=4, zorder=1)
        ax.text(1.02, y, letters[y], transform=ax.get_yaxis_transform(), va="center",
                color="#27715c" if "PASS" in letters[y] else "#924433", fontsize=10)
    ax.scatter(direct, range(12), s=70, color="#777b86", label="Strong prompt", zorder=2)
    ax.scatter(expand, range(12), s=70, color="#27715c", label="Candidate16 expand", zorder=3)
    ax.set_yticks(range(12), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(direct + expand) + 1)
    ax.set_xlabel("Usable mechanisms (mean of two reversed reviews)")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=.15)
    ax.legend(loc="upper left", bbox_to_anchor=(0, 1.12), frameon=False, ncol=2)
    fig.suptitle("Frozen candidate16 | 12 new tasks", x=.08, y=.97, ha="left", weight="bold", fontsize=18)
    fig.text(.08, .915, f"{summary['pass_count']}/12 pass   |   {votes['W']} win / {votes['T']} tie / {votes['L']} loss reviews")
    fig.text(.08, .045, "4 engineering + 4 teaching + 4 creative tasks. Fixed version, no outcome-driven tuning.\nModel reviews of written proposals; not human or field validation. OPEN includes ties and regressions.", fontsize=10)
    fig.subplots_adjust(left=.1, right=.72, top=.79, bottom=.15)
    for extension in ("png", "svg"):
        fig.savefig(ROOT / "assets" / f"frozen16-new12.{extension}", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
