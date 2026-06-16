from pathlib import Path
base = Path(r'D:/LLM/数理统计/数理统计复习/数理统计复习/_extracted_text')
for txt in sorted(base.glob('*.txt')):
    s = txt.read_text(encoding='utf-8', errors='ignore')
    print('\n###', txt.name)
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    shown = 0
    for ln in lines[:300]:
        if any(k in ln for k in ['§', '章', '定义', '定理', '例', '题', 'Review', 'Sheet']):
            print(ln)
            shown += 1
        if shown >= 60:
            break
