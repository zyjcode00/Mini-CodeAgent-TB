from pathlib import Path
base = Path(r'D:/LLM/数理统计/数理统计复习/数理统计复习/_extracted_text')
for name in ['第一章.txt','第二章.txt','第四章.txt','第五章.txt','第六章.txt','第七章.txt']:
    s = (base / name).read_text(encoding='utf-8', errors='ignore')
    print('\n---', name, '---')
    count = 0
    for line in s.splitlines():
        line = line.strip()
        if any(k in line for k in ['§', '定义', '定理', '中心极限定理', '大数定律', '正态', '区间估计', '假设检验', '统计量']):
            print(line)
            count += 1
            if count >= 120:
                break
