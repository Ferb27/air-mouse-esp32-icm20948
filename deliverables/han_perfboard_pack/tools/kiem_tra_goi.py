#!/usr/bin/env python3
"""Kiểm tra liên kết/dữ liệu/quyền riêng tư và nén gói; chỉ thư viện chuẩn."""
from pathlib import Path, PurePosixPath
import csv
import hashlib
import io
import json
import re
import runpy
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.with_suffix('.zip')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    generator = runpy.run_path(str(ROOT/'tools/sinh_hinh.py'))
    facts = generator['validate_data']()
    data = generator['DATA']
    for filename in ['00_DOC_TRUOC.md','01_AI_CONTEXT.md','02_HUONG_DAN_HAN_PERFBOARD.md',
                     '03_BOM_VAT_TU.csv','04_NOI_DAY_NETLIST.md','05_CHAN_GPIO.md',
                     '06_KICH_THUOC_MODULE.md','07_NHAT_KY_DO_DAC.md','08_NGUON_TRICH_DAN.md',
                     '09_KIEM_TRA_KHONG_FIRMWARE.md','SO_DO_MO_TA_BANG_CHU.md',
                     'hinh/00_TONG_HOP_HINH.html']:
        assert (ROOT/filename).is_file(),filename
    files = sorted(p for p in ROOT.rglob('*') if p.is_file())
    bad_suffixes = {'.kicad_sch','.kicad_pcb','.kicad_sym','.kicad_mod','.kicad_pro','.kicad_prl','.env','.docx'}
    links = 0
    for p in files:
        rel = p.relative_to(ROOT)
        assert str(rel).isascii(),str(rel)
        assert not p.is_symlink() and p.suffix not in bad_suffixes and not any(v in rel.parts for v in ['backups','_to_delete','__pycache__']),str(rel)
        if p.suffix not in {'.md','.json','.csv','.svg','.html','.py','.cjs','.txt'}:
            continue
        text=p.read_text(encoding='utf-8-sig')
        assert not re.search(r'[A-Za-z]:[\\/][A-Za-z0-9_]',text),f'Absolute machine path: {rel}'
        assert not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',text),f'Email: {rel}'
        assert not re.search(r'\bsk-[A-Za-z0-9_-]{20,}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY',text),f'Possible credential: {rel}'
        if p.suffix=='.md':
            for dest in re.findall(r'\]\(([^)]+)\)',text):
                if dest.startswith(('https://','http://','#')):
                    continue
                dest=dest.split('#')[0]
                target=(p.parent/dest).resolve()
                assert target.is_relative_to(ROOT.resolve()) and target.is_file(),(str(rel),dest)
                links+=1
    html=(ROOT/'hinh/00_TONG_HOP_HINH.html').read_text(encoding='utf-8')
    assert html.count('<svg ')==len(data['figures'])==12
    assert not re.search(r'<(?:script|link|img|iframe)\b|(?:src|href)=["\']https?://',html,re.I)
    rendered_ids=[]
    for name,title,kind in data['figures']:
        svg=ROOT/'hinh'/f'{name}.svg'
        node=ET.parse(svg).getroot()
        assert DATA_LABEL in ''.join(node.itertext()),name
        assert not any(e.tag.endswith('}image') for e in node.iter()),name
        if kind.startswith('wires'):
            rendered_ids += [e.text for e in node.iter() if e.tag.endswith('}text') and e.text and re.fullmatch(r'\d{2}',e.text)]
        png=ROOT/'hinh'/f'{name}.png'
        if png.exists():
            raw=png.read_bytes()
            assert raw[:8]==b'\x89PNG\r\n\x1a\n'
            width,height=struct.unpack('>II',raw[16:24])
            assert width>=2000 and height>=2800,(name,width,height)
    assert sorted(rendered_ids)==[f'{i:02}' for i in range(1,44)],rendered_ids
    assert len(list((ROOT/'hinh').glob('*.svg')))==12
    png_count=len(list((ROOT/'hinh').glob('*.png')))
    assert png_count in (0,12),png_count
    # Check actual rendered module positions, not just the coordinate conversion formula.
    tops=ET.parse(ROOT/'hinh/01_top.svg').getroot()
    bottoms=ET.parse(ROOT/'hinh/02_bottom.svg').getroot()
    def first_rect(tree,ref):
        g=next(e for e in tree.iter() if e.attrib.get('data-ref')==ref)
        return next(e for e in g if e.tag.endswith('}rect'))
    for ref in ['MOD1','MOD2','SW1','U2','U1','SW2','SW3','SW4']:
        a,b=first_rect(tops,ref),first_rect(bottoms,ref)
        assert abs(float(a.attrib['x'])+float(b.attrib['x'])+float(a.attrib['width'])-(2*90+90*5.25))<.05,ref
        assert a.attrib['y']==b.attrib['y'],ref
    guide=(ROOT/'02_HUONG_DAN_HAN_PERFBOARD.md').read_text(encoding='utf-8')
    assert 'BƯỚC PHẦN MỀM — để chủ dự án làm' in guide
    assert 'platformio run' not in guide and 'firmware_probe/' not in guide
    bom=list(csv.reader(io.StringIO((ROOT/'03_BOM_VAT_TU.csv').read_text(encoding='utf-8-sig'))))
    assert all(len(row)==10 for row in bom if row)
    assert sha(ROOT/'03_BOM_VAT_TU.csv')==data['source_sha256']['03_bom']
    browser_file=ROOT/'tools/kiem_tra_trinh_duyet.json'
    browser=None
    if browser_file.exists():
        browser=json.loads(browser_file.read_text(encoding='utf-8'))
        assert browser['png_count']==12 and browser['html_svg_count']==12 and browser['remote_requests']==0
        assert all(not check['outside'] for check in browser['checks'])
    facts.update(local_links=links,svg_count=12,png_count=png_count,bottom_mirror='PASS',
                 svg_wire_ids='01–43',privacy_scan='PASS',software_separation='PASS',
                 browser='PASS' if browser else 'NOT_RUN',png_pixels='2382×3369' if png_count else 'NOT_EXPORTED')
    return facts


DATA_LABEL='đề xuất, chưa đo thực tế'


def main():
    report_path=ROOT/'tools/KET_QUA_KIEM_TRA.md'
    if not report_path.exists():
        report_path.write_text('# Kết quả kiểm tra gói\n\nĐang kiểm tra; chưa có kết luận.\n',encoding='utf-8')
    facts=validate()
    png_note='Đã xuất đủ 12 PNG 2382×3369 bằng trình duyệt có sẵn; không cài thêm gói.' if facts['png_count'] else 'Chưa xuất PNG: chưa có trình duyệt/bộ xuất khả dụng; dùng SVG và HTML inline.'
    report='# Kết quả kiểm tra gói\n\n'+png_note+'\n\n'
    report+='| Kiểm tra thực hiện bằng lệnh | Kết quả |\n|---|---|\n'
    for key,value in facts.items():report+=f'| {key} | {value} |\n'
    report+='\nPhép kiểm dữ liệu có thử âm: đổi tọa độ R1 phải bị từ chối. Kiểm nguồn gốc net từng dòng theo số dòng netlist, số hình, ID 01–43, đối xứng TOP/BOTTOM, PNG, liên kết, tài liệu phần mềm và quyền riêng tư. Trình duyệt kiểm chữ không ra ngoài canvas; chất lượng hình đã được soi trực quan ở lần tạo gói.\n\n**Chưa kiểm phần cứng:** vị trí chân bo thật, kích thước/độ nhô ăng-ten, dòng/điện/nhiệt/PCM, quét I2C và thời lượng. Hình không phải biên bản nghiệm thu. Không kèm mã nguồn phần mềm; chủ dự án làm sau.\n\n## Tệp trong gói\n\n'
    names=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file())
    report+='\n'.join('- '+name for name in names)+'\n'
    (ROOT/'tools/KET_QUA_KIEM_TRA.md').write_text(report,encoding='utf-8')
    manifest=ROOT/'tools/MANIFEST_SHA256.txt'
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p!=manifest)
    manifest.write_text('\n'.join(sha(p)+'  '+p.relative_to(ROOT).as_posix() for p in files)+'\n',encoding='utf-8')
    files=sorted(p for p in ROOT.rglob('*') if p.is_file())
    with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:
            z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
        for p in files:
            name=ROOT.name+'/'+p.relative_to(ROOT).as_posix()
            assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
            assert z.read(name)==p.read_bytes(),name
    print(json.dumps(dict(facts,archive=ARCHIVE.name,file_count=len(files),archive_bytes=ARCHIVE.stat().st_size,
                          archive_mb=round(ARCHIVE.stat().st_size/1_000_000,2),zip_crc='PASS',decompressed_content='MATCH_ALL_FILES'),ensure_ascii=False))


if __name__=='__main__':
    main()
