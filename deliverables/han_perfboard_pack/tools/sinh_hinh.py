#!/usr/bin/env python3
"""Sinh SVG, HTML inline và mô tả chữ từ du_lieu_hinh.json; chỉ thư viện chuẩn."""
from pathlib import Path
from html import escape
import json
import re
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'tools/du_lieu_hinh.json').read_text(encoding='utf-8'))
COMP = {c['ref']: c for c in DATA['components']}
INK = '#183044'
RED = '#be2832'


def col_name(n):
    out = ''
    while n:
        n, r = divmod(n - 1, 26)
        out = chr(65 + r) + out
    return out


def hole(h):
    m = re.fullmatch(r'([A-Z]+)(\d+)', h)
    assert m, h
    c = 0
    for x in m[1]:
        c = c * 26 + ord(x) - 64
    r = int(m[2])
    assert 1 <= c <= DATA['board']['cols'] and 1 <= r <= DATA['board']['rows'], h
    b = DATA['board']
    return b['origin'][0] + (c - 1) * b['pitch'], b['origin'][1] + (r - 1) * b['pitch']


def coord(c):
    if c['region']:
        return '…'.join(c['region']) + ('; ' + '/'.join(c['holes']) if c['holes'] else '')
    return '/'.join(c['holes']) or 'gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ'


class SVG:
    def __init__(self, title, subtitle='Sơ đồ chức năng; không phải vị trí chân vật lý.', w=794, h=1123):
        self.w, self.h = w, h
        self.items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',
                      f'<title>{escape(title)}</title>',
                      '<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M-2,2 L2,-2 M0,10 L10,0 M8,12 L12,8" stroke="#d49b38" stroke-width="1.5"/></pattern></defs>',
                      '<style>text{font-family:Arial,"Segoe UI",sans-serif;fill:#183044} .muted{fill:#4c6475}</style>']
        self.rect(0, 0, w, h, '#fff', 'none', 0)
        self.text(28, 37, title, 23, bold=True)
        self.text(28, 64, subtitle, 13)
        self.text(w - 28, 87, DATA['checks']['figure_label'], 12, anchor='end', color=RED)
        self.line(28, 101, w - 28, 101, '#cbd5df', 1)

    def rect(self, x, y, w, h, fill='#f3f6f8', stroke='#587082', sw=1.2, radius=5, extra=''):
        self.items.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line(self, x1, y1, x2, y2, color=INK, width=2, dashed=False):
        self.items.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="5 4"' if dashed else '')+'/>')

    def circle(self, x, y, r=3, color=INK, fill='white', extra=''):
        self.items.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" stroke="{color}" fill="{fill}" {extra}/>')

    def text(self, x, y, value, size=14, anchor='start', color=INK, bold=False):
        self.items.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" style="fill:{color}"'+(' font-weight="700"' if bold else '')+'>'+escape(str(value))+'</text>')

    def wrap(self, x, y, value, width, size=14, color=INK, bold=False, line_height=None):
        lh = line_height or size * 1.35
        lines = []
        for paragraph in str(value).split('\n'):
            lines.extend(textwrap.wrap(paragraph, max(8, int(width / (size * .55))), break_long_words=False) or [''])
        for i, line in enumerate(lines):
            self.text(x, y + i * lh, line, size, color=color, bold=bold)
        return y + len(lines) * lh

    def box(self, ref, x, y, w, h, lines=None, fill=None):
        c = COMP[ref]
        self.items.append(f'<g data-ref="{escape(ref)}">')
        self.rect(x, y, w, h, fill or c['color'])
        self.text(x + 12, y + 24, ref + ' · ' + c['title'], 15, bold=True)
        if lines:
            self.wrap(x + 12, y + 46, '\n'.join(lines), w - 24, 13)
        self.items.append('</g>')

    def arrow(self, x1, y1, x2, y2, color=INK, label=None):
        self.line(x1, y1, x2, y2, color, 2.5)
        if abs(y2 - y1) >= abs(x2 - x1):
            dy = -7 if y2 > y1 else 7
            self.line(x2 - 4, y2 + dy, x2, y2, color)
            self.line(x2 + 4, y2 + dy, x2, y2, color)
        else:
            dx = -7 if x2 > x1 else 7
            self.line(x2 + dx, y2 - 4, x2, y2, color)
            self.line(x2 + dx, y2 + 4, x2, y2, color)
        if label:
            self.text((x1+x2)/2 + 8, (y1+y2)/2 - 5, label, 12, color=color)

    def finish(self, footer='Nguồn: hướng dẫn V2, netlist và dữ liệu đi kèm. Mọi số đo do người lắp thực hiện.'):
        self.line(28, self.h - 54, self.w - 28, self.h - 54, '#cbd5df', 1)
        self.wrap(28, self.h - 33, footer, self.w - 56, 12)
        return '\n'.join(self.items + ['</svg>'])


def board(s, bottom=False, x0=90, y0=164, scale=5.25, small=False, highlight=None):
    b = DATA['board']
    def xy(x, y):
        return x0 + (b['width']-x if bottom else x)*scale, y0+y*scale
    def hp(h):
        return xy(*hole(h))
    s.rect(x0, y0, b['width']*scale, b['height']*scale, '#f8fafb', '#334f63', 1.7, 0)
    if not small:
        s.text(x0 + b['width']*scale/2, y0-43, '90 mm · cột theo TOP, giữ tên lỗ khi lật', 12, anchor='middle')
    for c in range(1, b['cols']+1):
        for r in (range(1, b['rows']+1) if not small else []):
            x,y = hp(col_name(c)+str(r))
            s.circle(x,y, .85 if not small else .35, '#abbac4', '#d8e0e6')
        if not small:
            x,_=hp(col_name(c)+'1')
            s.text(x,y0-(23 if c%2 else 9),col_name(c),11,anchor='middle')
    if not small:
        for r in range(1,b['rows']+1):
            _,y=hp('A'+str(r));s.text(x0-10,y+3,str(r),10,anchor='end')
    k1,k2=[hole(h) for h in b['keepout']]
    left=min(xy(*k1)[0],xy(*k2)[0]); top=xy(*k1)[1]
    s.rect(left,top,(k2[0]-k1[0])*scale,(k2[1]-k1[1])*scale,'#fff4dd','#b77917',1.5,0)
    s.rect(left,top,(k2[0]-k1[0])*scale,(k2[1]-k1[1])*scale,'url(#hatch)','none',0,0)
    if not small:
        s.text(left+8,top+31,'CẤM CHÂN HÀN · B21…Z37',14,bold=True)
        s.text(left+8,top+54,'Vùng pin 60.96×40.64 mm',13)
        s.text(left+8,top+77,'Không dây / vít / mối hàn nổi',12)
        s.text(left+8,top+100,'Pin chưa chọn · gồm viền ≥2 mm',12)
    for c in DATA['components']:
        if c['kind']=='external':
            continue
        if highlight is not None and c['ref'] not in highlight:
            continue
        fill=c['color']; ref=c['ref']; pts=[hp(h) for h in c['holes']]
        s.items.append(f'<g data-ref="{escape(ref)}">')
        if c['region']:
            a,z=[hp(h) for h in c['region']]; rx=min(a[0],z[0]); ry=a[1]; rw=abs(z[0]-a[0]); rh=abs(z[1]-a[1])
            s.rect(rx,ry,rw,rh,fill,'#3f6074',1,0,extra='opacity="0.65"' if ref=='U1' else '')
            if not small:
                if ref=='U1':
                    s.text(rx+rw/2,ry+100,'ESP32',17,anchor='middle',bold=True)
                    s.text(rx+rw/2,ry+122,'thân mờ: tham khảo',11,anchor='middle')
                    s.text(rx+rw/2,ry+143,'U38…U57',12,anchor='middle')
                    s.text(rx+rw/2,ry+162,'AE38…AE57',12,anchor='middle')
                    s.text(rx+rw/2,ry+182,'hoặc AD sau đo',11,anchor='middle')
                    s.arrow(rx+rw/2,ry+60,rx+rw/2,ry+15,'#587082')
                    s.text(rx+rw/2,ry+12,'USB vào trong',11,anchor='middle')
                elif ref=='SW1':
                    s.text(rx+rw/2,ry+16,'SW1',11,anchor='middle',bold=True)
                    s.text(rx+rw/2,ry+31,'AA19…AG22',9,anchor='middle')
                else:
                    s.text(rx+rw/2,ry+23,ref,15,anchor='middle',bold=True)
                    s.text(rx+rw/2,ry+43,c['title'],12,anchor='middle')
                    s.text(rx+rw/2,ry+61,'…'.join(c['region']),11,anchor='middle')
            if ref=='U1':
                for col in ['U','AE']:
                    for rr in range(38,58):
                        sx,sy=hp(col+str(rr));s.rect(sx-2.6*scale/5,sy-2.6*scale/5,5.2*scale/5,5.2*scale/5,'#344957','none',0,0)
            if ref=='MOD1' and not small:
                portx=rx if not bottom else rx+rw
                direction=1 if not bottom else -1
                s.arrow(portx+36*direction,ry+rh-16,portx+6*direction,ry+rh-16,'#155f78')
                s.text(portx+45*direction,ry+rh-12,'USB-C',11,anchor='start' if not bottom else 'end')
        elif c['kind']=='button':
            cx,cy=pts[0]; size=12*scale
            s.rect(cx-size/2,cy-size/2,size,size,fill,'#765c2b',1,2)
            if not small:
                s.text(cx,cy-3,ref,13,anchor='middle',bold=True);s.text(cx,cy+15,c['holes'][0],11,anchor='middle')
        elif c['kind']=='flying':
            if not small:
                edge=x0+b['width']*scale if bottom else x0
                direction=1 if bottom else -1
                s.line(edge-6*direction,y0+55,edge+25*direction,y0+55,'#7c3aed')
                s.text(edge+28*direction,y0+48,'J1',12,anchor='start' if bottom else 'end',bold=True)
                s.text(edge+28*direction,y0+65,'gá rời',10,anchor='start' if bottom else 'end')
        else:
            if len(pts)>1:s.line(*pts[0],*pts[-1], '#9a6d38' if ref.startswith('R') else '#596d7b',4 if not small else 1.5)
            for px,py in pts:s.circle(px,py,2.6 if not small else 1,'#203d51',fill)
            if not small and c['kind'] not in ('test',):
                mx=sum(pt[0] for pt in pts)/len(pts);my=sum(pt[1] for pt in pts)/len(pts)
                if ref in ('R2','R3','C1','C2','J5V'):
                    # Outside-board callouts keep tiny parts and their coordinates readable.
                    call_y={'R2':y0+365,'R3':y0+407,'C1':y0+449,'J5V':y0+491,'C2':y0+533}[ref]
                    s.line(mx,my,x0+b['width']*scale+12,call_y,'#6b7f8c',.8)
                    s.text(x0+b['width']*scale+18,call_y-3,ref,13,bold=True)
                    s.text(x0+b['width']*scale+18,call_y+13,'/'.join(c['holes']),11)
                elif ref=='G*':
                    s.text(mx,my-10,'G* P39',12,anchor='middle',bold=True)
                elif ref=='R1':s.text(mx,my-12,'R1 D19/H19',11,anchor='middle')
                elif ref=='D1':s.text(mx+8,my+19,'D1 K19/L19',11)
        s.items.append('</g>')
    if not small:
        for c in [c for c in DATA['components'] if c['kind']=='test']:
            px,py=hp(c['holes'][0]);tx=px+(15 if not bottom else -15)
            s.text(tx,py+4,c['ref']+' '+c['title']+' '+c['holes'][0],11,anchor='start' if not bottom else 'end')
        # Dashed antenna marker expresses a required location, not an invented measured overhang.
        ax1,ay=xy(52.5,b['height']);ax2,_=xy(80.5,b['height'])
        s.rect(min(ax1,ax2),ay,abs(ax2-ax1),37,'#e0f2f5','#146c7e',1,0,extra='stroke-dasharray="4 3"')
        s.text((ax1+ax2)/2,ay+17,'ĂNG-TEN NGOÀI MÉP',10,anchor='middle',bold=True)
        s.text((ax1+ax2)/2,ay+31,'độ nhô CẦN ĐO',10,anchor='middle')
        s.text(x0,y0+b['height']*scale+64,'Lưới đúng tỉ lệ; A1 cách mép 3 mm là giả định. Không dùng làm mẫu khoan.',12)


def draw_board(title, bottom=False):
    s=SVG(title,'TOP nhìn linh kiện.' if not bottom else 'BOTTOM: trái/phải bị đảo so với TOP; chữ giữ chiều đọc.')
    board(s,bottom)
    s.wrap(28,1033,'Màu: vàng = nút/vùng pin; xanh = module; tím = giắc; xám = socket/test. Nét xám mảnh là chú thích. Ăng-ten nét đứt: yêu cầu vị trí, độ nhô chưa đo.',735,12)
    return s.finish('Nguồn: V2 §3.5.3. Vùng pin không chân cả hai mặt; vùng ăng-ten không đồng/dây/kim loại.')


def draw_power(title):
    s=SVG(title,'Luồng điện, không theo tỉ lệ. Tím = CELL−; đen = GND hệ thống.')
    levels=[('BAT1',120,65,['1S PCM; chưa chọn pin']),('J1',225,65,['+ → B+ ; − → B−']),('MOD1',330,110,['B+/B−: phía cell','OUT+/OUT−: phía hệ thống','USB-C 5V chỉ khi sạc pin thật']),('SW1',500,65,['OUT+ → ON ; COM → V_SYS']),('MOD2',610,80,['VIN+ = V_SYS ; VIN− = GND','VOUT+ = 5V ; VOUT− = GND']),('J5V',750,65,['1 = +5V ; 2 = GND','tháo cả đầu cái khi dùng USB']),('U1',880,80,['VIN/5V từ J5V.1','GND về hệ thống'])]
    for ref,y,h,lines in levels:s.box(ref,85,y,305,h,lines)
    reds=DATA['net_colors']
    for a,b,label in [(185,225,'VBAT'),(290,330,'VBAT'),(440,500,'OUT+'),(565,610,'V_SYS'),(690,750,'5V'),(815,880,'5V qua J5V')]:s.arrow(235,a,235,b,reds['5V'],label)
    # Cell return ends at B-; it never reaches the separate system return.
    s.line(85,150,47,150,reds['GND_BAT_CELL'],3);s.line(47,150,47,410,reds['GND_BAT_CELL'],3);s.line(47,410,85,410,reds['GND_BAT_CELL'],3)
    s.line(47,265,85,265,reds['GND_BAT_CELL'],3)
    s.text(30,475,'CELL−',13,color=reds['GND_BAT_CELL'],bold=True)
    s.line(390,412,463,412,reds['GND'],3);s.line(463,412,463,947,reds['GND'],3)
    for yy in [660,790,940]:s.line(390,yy,463,yy,reds['GND'],3)
    s.text(473,455,'GND = OUT−',13,bold=True)
    s.text(505,372,'✗',45,color=RED,bold=True)
    s.wrap(550,359,'CẤM nối B− với OUT−/GND bên ngoài module',195,15,color=RED,bold=True)
    s.text(410,317,'USB-C vào TP4056',13)
    s.arrow(460,320,390,353,'#146c7e')
    s.line(390,550,625,550,reds['V_SYS'],2)
    s.box('R2',550,575,195,62,['V_SYS → 100 kΩ'])
    s.line(625,550,625,575,reds['V_SYS'])
    s.line(625,637,625,685,reds['BAT_SENSE'])
    s.text(535,664,'BAT_SENSE → GPIO34',13,bold=True)
    s.line(625,680,760,680,reds['BAT_SENSE'])
    s.box('R3',530,700,215,62,['100 kΩ → GND'])
    s.line(625,685,625,700,reds['BAT_SENSE'])
    s.line(625,762,625,830,reds['GND']);s.line(463,830,625,830,reds['GND'])
    s.items.append('<g data-ref="C1">')
    s.line(625,680,500,680,reds['BAT_SENSE']);s.line(500,680,500,720,reds['BAT_SENSE'])
    s.line(486,720,514,720,INK);s.line(486,730,514,730,INK)
    s.line(500,730,500,830,reds['GND'])
    s.text(510,802,'C1 100 nF // R3',12)
    s.items.append('</g>')
    s.text(535,899,'C1: BAT_SENSE ↔ GND',12)
    s.box('U2',530,967,215,65,['VCC/NCS ← ESP32 3V3'])
    s.arrow(390,925,530,995,reds['3V3'],'3V3')
    s.box('C2',85,986,305,50,['+5V ↔ GND; không nối tiếp'])
    s.line(235,720,65,720,reds['5V']);s.line(65,720,65,1010,reds['5V']);s.line(65,1010,85,1010,reds['5V'])
    s.line(390,1010,463,1010,reds['GND']);s.line(463,947,463,1010,reds['GND'])
    return s.finish('Nguồn: V2 §3.0/3.7; C1/C2 mắc song song. Xem hình 04a/04b cho từng liên kết điện.')


def draw_wires(title,power):
    ids=set(list(range(1,14))+[42,43])
    ws=[w for w in DATA['wires'] if (int(w['id']) in ids)==power]
    h=1123
    s=SVG(title,'Sơ đồ từng liên kết theo net; số dòng khớp bảng 3.7. Không phải đường đi vật lý.',h=h)
    for i,w in enumerate(ws):
        y=131+i*30;color=DATA['net_colors'][w['net']]
        s.rect(28,y-17,738,28,'#f3f6f9' if i%2==0 else '#fff','none',0,0)
        s.text(38,y+2,w['id'],14,bold=True)
        s.text(77,y-1,w['net'],11,color=color,bold=True)
        a=w['from'].replace('nhãn thật, tương ứng N chân','N#').replace('theo nhãn thật','nhãn thật')
        b=w['to'].replace('cùng net G*','').replace('qua đầu ghép','qua giắc')
        s.text(207,y-5,a,11)
        s.arrow(212,y+9,500,y+9,color)
        s.text(512,y+3,b,11)
    y=131+len(ws)*30+24
    s.wrap(30,y,'Màu dương: các sắc đỏ; GND: đen; B−/GND_BAT_CELL: tím trên hình để tách rõ (dây thật đen nhãn B−). SDA xanh lá, SCL vàng, nút xanh dương/trắng có viền/tím, LED cam, SENSE xám. Nhãn net luôn là căn cứ chính.',730,14)
    return s.finish('Nguồn: V2 §3.7; P = bó 2–3 lõi; S = một lõi. Dây đi vòng vùng pin, không đi theo nét logic này.')


def draw_imu(title):
    s=SVG(title,'Số theo netlist; đối chiếu chữ in trên module. Chỉ cắm socket trên carrier.')
    for i,p in enumerate(DATA['imu']):
        y=160+i*70; nc=p['target']=='ĐỂ HỞ'; color='#8a97a0' if nc else ('#20252b' if p['target']=='GND' else '#a61b29' if p['target']=='3V3' else '#15803d' if p['name']=='SDA' else '#a17a00')
        s.rect(45,y-26,280,56,'#edf0f2' if nc else '#e7f3ef',color)
        s.text(62,y+7,f"{p['n']:02}  {p['name']}",20,bold=True)
        s.text(240,y+7,p['hole'],13)
        s.arrow(325,y,440,y,color)
        s.text(462,y+6,p['target'],19,color=color,bold=True)
    s.wrap(45,919,'VCC/NCS → 3V3; AD0/FSY → GND. INT/ACL/ADA để hở, không ghép bus phụ vào SDA/SCL. Định hướng trái/phải của module phải đo thực; C42…L42 chỉ áp dụng khi chữ in khớp.',695,16)
    return s.finish('Nguồn: V2 §3.5.3/3.7 và netlist. 0x68 là địa chỉ chọn bởi AD0=GND, chưa phải kết quả quét mới.')


def draw_gpio(title):
    s=SVG(title,'Danh sách chân, KHÔNG suy vị trí vật lý từ bo 38 chân tương tự.')
    s.rect(30,122,734,95,'#fff1e6','#c27d45')
    s.wrap(45,148,'CHƯA ĐỦ CĂN CỨ vẽ vị trí chân ESP32. Đối chiếu chữ in trên đúng bo; số dưới đây chỉ theo netlist, không phải cách đếm lỗ carrier.',700,17,bold=True)
    s.text(45,255,'Nhãn trên bo',16,bold=True);s.text(255,255,'Số netlist',16,bold=True);s.text(425,255,'Nối tới',16,bold=True)
    for i,row in enumerate(DATA['gpio']):
        y=295+i*63
        s.rect(30,y-25,734,60,'#edf3f7' if i%2==0 else '#fff','none',0)
        s.text(45,y+6,row[0],18,bold=True);s.text(255,y+6,row[1],16)
        s.wrap(425,y,row[2],320,14)
    s.wrap(40,978,'GPIO34 chỉ BAT_SENSE, không 5V hay V_SYS trực tiếp. Socket U38…U57 và AE38…AE57 (hoặc AD sau đo); không tự gán GPIO theo hàng 38…57.',710,15,color=RED,bold=True)
    return s.finish('Nguồn: bảng GPIO/netlist và V2 §3.7. Pin thật và khoảng hai hàng: CẦN ĐO THỰC TẾ.')


def draw_parts(title):
    s=SVG(title,'Sơ đồ nhận biết; không theo tỉ lệ. Hướng nhóm chân nút chỉ là logic, phải đo.')
    s.text(40,141,'NÚT 4 CHÂN: đo hai nhóm A/B',18,bold=True)
    for x,label,color in [(125,'A → GPIO','#2563eb'),(330,'B → GND','#20252b')]:
        s.circle(x,192,9,color);s.circle(x,282,9,color);s.line(x,201,x,273,color,4)
        s.text(x,320,label,15,anchor='middle',color=color,bold=True)
    s.line(134,237,321,237,'#64748b',2,True)
    s.text(165,225,'nhấn mới thông',13)
    s.wrap(40,350,'Cùng nhóm luôn thông. Khác nhóm: thả hở, nhấn thông. Không đo ohm khi có nguồn; không suy nhóm A/B từ góc nhìn hình.',390,14)
    s.box('D1',470,135,280,150,['A: chân dài nếu chưa cắt','K: chân ngắn/vát; diode test','GPIO32 → R1 → A; K → GND'])
    s.line(540,286,540,337,'#a61b29',3);s.line(675,286,675,318,'#20252b',3)
    s.text(528,362,'A',17,bold=True);s.text(669,344,'K',17,bold=True)
    band_colors={'nâu':'#795335','đen':'#111827','cam':'#ed8b24'}
    s.text(40,455,'ĐIỆN TRỞ 1%, năm vạch (đo lại bằng đồng hồ)',18,bold=True)
    for i,r in enumerate(DATA['resistors']):
        y=500+i*150
        s.line(65,y+25,715,y+25,'#556976',2)
        s.rect(200,y,240,50,'#e8d8b8','#876c46',1,15)
        for j,b in enumerate(r['bands']):s.rect(220+j*40,y,15,50,band_colors[b],'none',0,0)
        s.text(470,y+10,r['ref']+' · '+('1 kΩ' if r['ohm']==1000 else '100 kΩ'),20,bold=True)
        s.text(80,y+86,' – '.join(r['bands']),15)
    s.box('C1',40,825,330,125,['100 nF / mã 104','Không phân cực; BAT_SENSE–GND'])
    s.box('C2',420,825,330,125,['10 µF; có vạch cực âm (−)','+5V → (+), GND → (−)'])
    s.wrap(40,995,'Vạch/độ dài chân chỉ hỗ trợ nhận biết. Chân đã cắt phải đo/đối chiếu nhãn. Đảo C2 có thể gây nóng/rò/vỡ; LED phải có R1.',710,15,color=RED)
    return s.finish('Nguồn: V2 §3.6/3.12.2, BOM. Không xem hình nhóm chân nút là footprint đã xác nhận.')


def draw_solder(title):
    s=SVG(title,'Tám bước; rút mọi nguồn và rút module khỏi socket khi hàn tiếp.')
    for i,(name,refs) in enumerate(DATA['solder_groups']):
        x=30+(i%2)*385;y=125+(i//2)*218
        s.rect(x,y,350,200,'#f5f8fa','#a8b9c6')
        s.text(x+12,y+25,f'{i+1}. {name}',17,bold=True)
        board(s,x0=x+15,y0=y+42,scale=.83,small=True,highlight=set(refs))
        ctext='\n'.join(ref+' '+('…'.join(COMP[ref]['region']) if COMP[ref]['region'] else '/'.join(COMP[ref]['holes']) or 'gá rời') for ref in refs)
        s.wrap(x+106,y+55,ctext,228,12)
        s.text(x+106,y+175,'Hàn → soi → đo → mới tiếp',12,bold=True)
    s.wrap(35,1030,'Làm cụm logic trước trên cùng board; bước nguồn bổ sung sau. J1/J5V và module nguồn gá trên đệm cách điện. Mọi hình nhỏ dùng cùng tọa độ với hình TOP.',720,13)
    return s.finish('Nguồn: V2 §3.6. Không hàn cố định ESP32/IMU vào carrier; chỉ cắm socket.')


def draw_measure(title):
    s=SVG(title,'Sơ đồ điểm đo logic; que đen phải đúng điểm âm, không luôn lấy B− làm GND.')
    for i,m in enumerate(DATA['measurements']):
        y=145+i*140
        s.circle(70,y+30,22,'#146c7e','#def0f3')
        s.text(70,y+37,str(i+1),20,anchor='middle',bold=True)
        if i<5:s.arrow(70,y+53,70,y+116,'#6b8798')
        s.rect(115,y,630,115,'#f4f8fa','#b0c1cd')
        s.text(131,y+25,m['label'],20,bold=True)
        s.wrap(131,y+52,m['expected'],600,16)
        s.text(131,y+95,'Que đen: '+m['minus'],14,color=RED if m['minus']=='B-' else INK,bold=True)
    s.wrap(40,1016,'Điện áp dải thiết kế không chứng nhận mọi pin. Tắt nguồn trước đổi dây/đo ohm. ADC và I2C cần phần mềm, để chủ dự án làm.',710,14)
    return s.finish('Nguồn: V2 bảng 3.8.2. Chưa có số đo phần cứng; ghi vào nhật ký, không tick từ hình.')


def draw_j5v(title):
    s=SVG(title,'Quy tắc bắt buộc; J5V là cặp dây +5V/GND, không phải shunt chập hai chân.')
    for y,title,lines in [(150,'CHẠY PIN',['✓ Cắm J5V đúng chiều + / −','✓ RÚT USB ESP32 và USB sạc','✓ SW1 ON sau kiểm tra','✗ Không đồng thời USB ESP32']), (590,'CẮM USB ESP32',['✓ SW1 OFF, RÚT J5V','✓ Chỉ cấp USB vào ESP32','✓ Bọc/cố định đầu tháo','✗ SW1 OFF một mình chưa đủ'])]:
        s.rect(35,y,724,360,'#eaf6ef' if y==150 else '#eaf1fa','#599274' if y==150 else '#6688b0',2)
        s.text(65,y+48,title,28,bold=True)
        for i,line in enumerate(lines):s.text(65,y+105+i*48,line,20,color=RED if line.startswith('✗') else INK,bold=True)
        s.text(65,y+325,'J5V.1 = AC34 +5V; J5V.2 = AD34 GND',15)
    s.wrap(40,1013,'Tắt SW1 trước cắm/rút. Đầu cái 1 tới VIN, cái 2 tới GND. Cắm đảo có thể chập; đo cực và chặn hướng trước vận hành.',710,16,color=RED)
    return s.finish('Nguồn: V2 §3.6.8/3.9.1. Không suy có diode trên DevKit tham khảo thành bo thật được cấp hai nguồn.')


def draw_battery(title):
    s=SVG(title,'Chỉ khi có pin thật đúng quy cách. Không đạt phép đo → dừng, ngắt nếu an toàn.')
    for i,step in enumerate(DATA['battery_steps']):
        y=124+i*74
        s.circle(49,y+23,17,'#146c7e','#e2f1f4');s.text(49,y+29,step['n'],16,anchor='middle',bold=True)
        if i<11:s.arrow(49,y+41,49,y+59,'#6a8394')
        s.rect(80,y,680,66,'#f4f7f9','#b9c9d3')
        s.text(92,y+22,step['title'],14,bold=True)
        # Compact condition stays connected to the exact full step in the generated text description.
        body=re.sub(r'\*\*.*?\*\*:?\s*','',step['body'],count=1)
        body=body.replace('**','')
        short=textwrap.shorten(body.split('→')[0].split('Nếu ')[0],width=170,placeholder='…')
        s.wrap(92,y+43,short,650,11,line_height=13)
    s.wrap(35,1030,'✗ Sai cực/áp, sụt/reset, nóng/phồng/mùi → DỪNG. Mọi ngưỡng và đầy đủ 12 bước: V2 §3.13.4 và mô tả chữ đi kèm.',725,14,color=RED,bold=True)
    return s.finish('Nguồn: V2 §3.13.4. Sạc riêng sau đọc rủi ro §3.9.2; không sạc nguồn bàn thay pin.')


def validate_coordinates(c):
    tokens=[h for h in re.findall(r'\b[A-Z]{1,2}\d+\b',c['source_row'].split('|')[2]) if h not in COMP]
    ref=c['ref']
    picks={'SW2':[0],'SW4':[1],'SW3':[2],'R1':[0,1],'D1':[2,3],'R2':[0,1],'R3':[2,3],'C1':[4,5],'C2':[0,1],'J5V':[0,1],'G*':[0]}
    if ref in picks:
        assert c['holes']==[tokens[i] for i in picks[ref]],ref
    elif ref.startswith('TP'):
        assert c['holes']==[tokens[int(ref[2:])-1]],ref
    elif ref=='U2':
        assert c['region']==tokens[:2] and c['holes'][0]==tokens[2] and c['holes'][-1]==tokens[3],ref
        assert all(h.endswith('42') for h in c['holes']) and len(c['holes'])==10,ref
    elif c['region']:
        expected=[tokens[0],tokens[3]] if ref=='U1' else tokens[:2]
        assert c['region']==expected,ref


def validate_data():
    guide=(ROOT/'02_HUONG_DAN_HAN_PERFBOARD.md').read_text(encoding='utf-8')
    wire_section=guide.split('## 3.7.')[1].split('## 3.8.')[0]
    rows=[[v.strip() for v in line.split('|')[1:-1]] for line in wire_section.splitlines() if re.match(r'^\| \d{2} \|',line)]
    assert len(rows)==DATA['checks']['wire_count']==43
    assert [r[0] for r in rows]==[f'{i:02}' for i in range(1,44)]
    assert len({w['net'] for w in DATA['wires']})==DATA['checks']['expected_nets']==15
    for row,w in zip(rows,DATA['wires']):
        assert row[:7]==[w[k] for k in ['id','net','from','to','type','color','length']], w['id']
    for c in DATA['components']:
        assert c['source_row'] in guide,c['ref']
        validate_coordinates(c)
        assert any(c['ref'] in w['from']+' '+w['to'] for w in DATA['wires']), c['ref']
        for h in c['holes']+(c['region'] or []):hole(h)
    net=(ROOT/'04_NOI_DAY_NETLIST.md').read_text(encoding='utf-8')
    for name in DATA['net_names']:assert name in net,name
    net_rows={}
    for line in net.splitlines():
        if re.match(r'^\| \d+ ',line):
            parts=[v.strip() for v in line.split('|')[1:-1]]
            if len(parts)==8:
                net_rows[parts[0]]=re.sub(r'[*` ]','',parts[3])
    for w in DATA['wires']:
        source_number=re.match(r'^(\d+)(?:;|$)',w['source'])
        if source_number:assert net_rows[source_number[1]]==w['net'],w['id']
    bad=dict(COMP['R1']);bad['holes']=['A1','H19']
    try:
        validate_coordinates(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Coordinate negative test failed')
    assert [p['name'] for p in DATA['imu']]==['VCC','GND','SCL','SDA','NCS','AD0','INT','FSY','ACL','ADA']
    assert [p['n'] for p in DATA['battery_steps']]==list(range(1,13))
    b=DATA['board'];a,z=[hole(h) for h in b['keepout']]
    assert z[0]-a[0]>=58 and z[1]-a[1]>=40
    assert len(DATA['figures'])==12
    return {'wire_rows':43,'nets':15,'components':len(COMP),'coordinates':'MATCH_GUIDE','source_table_rows':'MATCH','measurements':'NOT_PERFORMED'}


def main():
    report=validate_data()
    renderers={'board_top':lambda t:draw_board(t),'board_bottom':lambda t:draw_board(t,True),'power':draw_power,'wires_power':lambda t:draw_wires(t,True),'wires_signal':lambda t:draw_wires(t,False),'imu':draw_imu,'gpio':draw_gpio,'parts':draw_parts,'solder':draw_solder,'measure':draw_measure,'j5v':draw_j5v,'battery':draw_battery}
    desc=['# Mô tả hình bằng chữ — sinh cùng dữ liệu với SVG','', 'Nguồn: tools/du_lieu_hinh.json; tọa độ theo hướng dẫn V2. Không phải số đo thực. Màu B− được vẽ tím để tách GND đen; dây thật đen nhãn B−. Màu không thay nhãn net.','']
    panels=[]
    for name,title,kind in DATA['figures']:
        svg=renderers[kind](title)
        xml=ET.fromstring(svg)
        refs={g.attrib['data-ref'] for g in xml.iter() if 'data-ref' in g.attrib}
        assert refs<=set(COMP),refs-set(COMP)
        path=ROOT/'hinh'/f'{name}.svg';path.write_text(svg,encoding='utf-8')
        panels.append(f'<section><h2>{escape(title)}</h2>{svg}</section>')
        desc+=['## '+name+' — '+title,'',f'[SVG](hinh/{name}.svg). Hướng nhìn: '+('BOTTOM, đối xứng trái/phải so TOP.' if kind=='board_bottom' else 'TOP.' if kind=='board_top' else 'Sơ đồ logic, không theo tỉ lệ vật lý.'),'']
        # Extract every label from the actual SVG, rather than maintain a second hand-written description.
        labels=list(dict.fromkeys(''.join(n.itertext()) for n in xml.iter() if n.tag.endswith('}text')))
        desc+=['### Nhãn hiển thị','']+['- '+t for t in labels]+['']
        if kind in ('board_top','board_bottom','solder'):
            desc+=['### Linh kiện và lỗ theo TOP (BOTTOM giữ nguyên tên lỗ)','', '| Ref | Linh kiện | Tọa độ/đặt | Màu vùng | Nối với |','|---|---|---|---|---|']
            for c in DATA['components']:
                connections=[w['id']+': '+w['net']+'; '+w['from']+' → '+w['to'] for w in DATA['wires'] if c['ref'] in w['from']+' '+w['to']]
                desc.append('| '+' | '.join([c['ref'],c['title'],coord(c),c['color'],'<br>'.join(connections)])+' |')
            desc+=['','Vùng pin: '+ '…'.join(DATA['board']['keepout'])+'; 60.96×40.64 mm, cả hình chiếu hai mặt không chân/dây/vít. Lưới A1 cách mép 3 mm là giả định. Dấu ăng-ten ngoài mép chỉ yêu cầu vị trí, độ nhô CẦN ĐO THỰC TẾ.','']
        if kind.startswith('wires') or kind=='power':
            ids=set(list(range(1,14))+[42,43])
            ws=DATA['wires'] if kind=='power' else [w for w in DATA['wires'] if (int(w['id']) in ids)==(kind=='wires_power')]
            desc+=['### Liên kết điện','']+['- '+w['id']+' | '+w['net']+' | '+w['from']+' → '+w['to']+' | màu hình '+DATA['net_colors'][w['net']]+'; màu dây '+w['color'] for w in ws]+['']
        if kind=='battery':desc+=['### Nguyên văn 12 bước từ dữ liệu V2','']+[str(p['n'])+'. '+p['body'] for p in DATA['battery_steps']]+['']
    (ROOT/'SO_DO_MO_TA_BANG_CHU.md').write_text('\n'.join(desc),encoding='utf-8')
    html='<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hình hướng dẫn hàn Air Mouse</title><style>body{margin:0;background:#e8eef2;color:#183044;font-family:Arial,sans-serif}header{max-width:794px;margin:24px auto;padding:0 12px}section{max-width:794px;margin:24px auto;background:white;box-shadow:0 2px 12px #bed0dc}h2{font-size:18px;padding:16px 24px;margin:0}svg{display:block;width:100%;height:auto}@page{size:A4 portrait;margin:8mm}@media print{body{background:white}header{display:none}section{margin:0;box-shadow:none;break-after:page;max-width:none}h2{display:none}svg{max-height:280mm;width:100%}}</style><header><h1>Hình hướng dẫn hàn Air Mouse</h1><p>11 nhóm / 12 hình; 04 tách nguồn và tín hiệu. SVG inline, không tải ngoài. In A4 từng hình; không dùng làm mẫu khoan 1:1.</p></header>'+''.join(panels)+'</html>'
    (ROOT/'hinh/00_TONG_HOP_HINH.html').write_text(html,encoding='utf-8')
    report.update(svg_count=len(panels),description='GENERATED_FROM_SVG_AND_SHARED_DATA',html='INLINE_NO_EXTERNAL_RESOURCES')
    (ROOT/'tools/kiem_tra_du_lieu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':
    main()
