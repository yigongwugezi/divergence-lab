"""Plot the bundled development results without model calls."""
from pathlib import Path
from collections import Counter
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'evidence/candidate4/summary.json').read_text(encoding='utf-8'))
tasks = data['tasks']
votes = Counter(s for row in tasks.values() for s in row['scores'])
assert [votes[1], votes[.5], votes[0]] == data['review_win_tie_loss'] == [19, 6, 1]
assert sum(row['passed'] for row in tasks.values()) == data['passed'] == 11
assert len(tasks) == data['total'] == 13
assert all(row['gates']['mechanism_noninferior_each_review'] and
           row['gates']['no_serious_expand_violation'] for row in tasks.values())
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
fig, ax = plt.subplots(figsize=(8.5, 8.8), facecolor='#faf8f3')
scores = [row['scores'] for row in tasks.values()]
ax.imshow(scores, cmap=ListedColormap(['#c85c49', '#e8dfc5', '#428a76']), vmin=0, vmax=1, aspect='auto')
ax.set_xticks([0, 1], ['Review 1', 'Review 2 (reversed)'])
ax.set_yticks(range(13), tasks)
for y, pair in enumerate(scores):
    for x, score in enumerate(pair):
        ax.text(x, y, {0: 'LOSS', .5: 'TIE', 1: 'WIN'}[score], ha='center', va='center',
                color='white' if score != .5 else '#453f32', weight='bold')
ax.tick_params(length=0, pad=10)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.suptitle('Candidate 4 | Best complete development result', x=.08, ha='left', fontsize=17, weight='bold', y=.97)
fig.text(.08, .912, '11 / 13 tasks pass  ·  19 wins / 6 ties / 1 loss', fontsize=14)
fig.text(.08, .074, 'All 26 reviews: mechanism count >= baseline; no serious violation.\nS05: tie / tie. C05: win / loss. Two tasks remain below the target.', fontsize=10)
fig.text(.08, .023, 'DEVELOPMENT / REGRESSION SET — not an unseen-task win rate.', fontsize=10, weight='bold', color='#924433')
fig.subplots_adjust(left=.16, right=.94, top=.86, bottom=.15)
for ext in ('png', 'svg'):
    fig.savefig(ROOT / f'assets/candidate4-regression.{ext}', dpi=180, facecolor=fig.get_facecolor())
plt.close(fig)
print('Verified 13 development tasks and rendered both candidate4 figures.')
