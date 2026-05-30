from pathlib import Path

root = Path('.')
tmp = root / '.codex_tmp_b226874'
adapter = (tmp / 'adapter.txt').read_text(encoding='utf-8')
labels = [line.strip() for line in (tmp / 'labels.txt').read_text(encoding='utf-8').splitlines() if line.strip()]
out = root / 'custom_gpt_knowledge' / 'Everything-Exam-Preparation-Knowledge-Combined.md'
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('w', encoding='utf-8') as fh:
    fh.write(adapter)
    fh.write('# Everything Exam Preparation Skill Knowledge Bundle\n\n')
    fh.write('This single file combines the flattened Custom GPT knowledge files. Each section preserves its original source filename.\n\n')
    for label in labels:
        rel = label.replace('__', '/')
        src = root / rel
        if not src.is_file():
            raise SystemExit(f'missing source for {label} -> {src}')
        fh.write(f'\n\n---\n\n## Source File: `{label}`\n\n```text\n')
        fh.write(src.read_text(encoding='utf-8'))
        fh.write('\n```\n')
