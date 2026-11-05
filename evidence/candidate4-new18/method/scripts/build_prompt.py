"""Build the frozen P0/P1/P2 prompts; model execution stays with the host."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def candidates(path, limit=3):
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        if set(data) != {'candidates'}:
            raise ValueError('expected only candidates in response')
        data = data['candidates']
    if not isinstance(data, list) or len(data) > limit or any(
        not isinstance(row, dict) or set(row) != {'title', 'proposal', 'experiment'}
        or any(not isinstance(row[key], str) or not row[key] for key in row)
        for row in data
    ):
        raise ValueError(f'expected 0..{limit} complete title/proposal/experiment candidates')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['P0', 'P1', 'P2'])
    parser.add_argument('--task', type=Path, required=True)
    parser.add_argument('--p0', type=Path)
    parser.add_argument('--p1', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if (args.phase in {'P1', 'P2'}) != bool(args.p0) or (args.phase == 'P2') != bool(args.p1):
        parser.error('P1 needs --p0; P2 needs --p0 and --p1; P0 needs neither')
    task = json.loads(args.task.read_text(encoding='utf-8'))
    if (not isinstance(task, dict) or not isinstance(task.get('goal'), str) or not task['goal']
            or not isinstance(task.get('hard_constraints'), list)
            or any(not isinstance(item, str) for item in task['hard_constraints'])):
        parser.error('task needs a nonempty goal and hard_constraints string list (empty if none)')
    if args.phase == 'P0':
        template = (ROOT / 'references/BASELINE_PROMPT.txt').read_text(encoding='utf-8')
        prompt = template.replace('{TASK}', json.dumps(task, ensure_ascii=False))
    else:
        p0 = candidates(args.p0)
        history = [{'index': i, **row} if args.phase == 'P1'
                   else {'index': i, 'title': row['title'], 'proposal': row['proposal']}
                   for i, row in enumerate(p0)]
        if args.phase == 'P2':
            history += [{'title': row['title'], 'proposal': row['proposal']} for row in candidates(args.p1)]
        template = (ROOT / 'references/CONTINUE_PROMPT.txt').read_text(encoding='utf-8')
        prompt = template.replace('{TASK}', json.dumps(task, ensure_ascii=False)).replace(
            '{HISTORY}', json.dumps(history, ensure_ascii=False))
    with args.out.open('x', encoding='utf-8', newline='\n') as file:
        file.write(prompt)


if __name__ == '__main__':
    main()
