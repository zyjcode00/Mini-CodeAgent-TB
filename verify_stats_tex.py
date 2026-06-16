from pathlib import Path
p = Path(r'D:/LLM/数理统计/数理统计复习/数理统计复习/数理统计_复习知识点_1-8章.tex')
text = p.read_text(encoding='utf-8')
print('exists=', p.exists())
print('bytes=', p.stat().st_size)
print('chars=', len(text))
print('documentclass=', '\\documentclass' in text)
print('begin_document=', '\\begin{document}' in text)
print('end_document=', '\\end{document}' in text)
print('sections=', text.count('\\section{'))
for i in range(1, 9):
    print(f'chapter_{i}_covered=', f'第{i}章' in text or ['一','二','三','四','五','六','七','八'][i-1] in text)
print('utf8_ok=True')
