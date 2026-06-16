from pathlib import Path
from pypdf import PdfReader
base = Path(r'D:/LLM/数理统计/数理统计复习/数理统计复习')
out = base / '_extracted_text'
out.mkdir(exist_ok=True)
for pdf in sorted(base.glob('*.pdf')):
    print('EXTRACT', pdf.name)
    try:
        reader = PdfReader(str(pdf))
        parts = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            parts.append(f'\n\n===== Page {i} =====\n{text}')
        txt = ''.join(parts)
        (out / (pdf.stem + '.txt')).write_text(txt, encoding='utf-8')
        print(' pages', len(reader.pages), 'chars', len(txt))
    except Exception as e:
        print(' ERROR', type(e).__name__, e)
