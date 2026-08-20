"""
국내 제약바이오 기술수출 현황(33건, 총액 13조 3,720억원) 표를 단독 엑셀 파일로 정리.

원자료: 보도 표 이미지 1종 (일자 1.7.~12.31., 연도 표기 없음)
출력:  output/k_bio_licensing_33deals.xlsx

원문의 '계약상대(국가)' 한 칸은 계약상대 / 국가 두 열로 분리했다.
계약규모는 원문 표기(예: "약 2조 900억원 / (약 18억 6,600만 달러)")를 단위 통일해
  - 만달러 열: 숫자만 (단위 = 만 달러)
  - 억원   열: 숫자만 (단위 = 억 원)
로 입력했다. 비공개 건은 빈칸이며 하단에 SUM 합계 행이 있다.
원문 표기는 '원문(계약규모)' 열에 그대로 보존.
"""

from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
OUT = BASE / "output" / "k_bio_licensing_33deals.xlsx"

FONT = "Arial"
TITLE = "국내 제약바이오 기술수출 현황 (33건 / 원문 총액 13조 3,720억원, 비공개 제외)"

# 일자, 개발사, 계약상대, 국가, 제품/적응증/기술, 만달러, 억원, 비고, 원문(계약규모)
ROWS = [
    ("1. 7.", "알테오젠", "인타스 파마슈티컬스", "인도", "인간 히알루로니다제(ALT-B4)",
     None, 1250, "달러 금액 미표기", "약 1,250억원"),
    ("1. 29.", "GC녹십자랩셀·아티바", "MSD", "미국", "고형암에 쓰는 CAR-NK 세포치료제 3종(공동개발)",
     186600, 20900, "", "약 2조 900억원 (약 18억 6,600만 달러)"),
    ("2. 18.", "제넥신", "KG바이오", "인도네시아", "GX-17(코로나19 치료제와 면역항암제로 개발 중)",
     110000, 12000, "", "약 1조 2,000억원 (약 11억 달러)"),
    ("3. 18.", "대웅제약", "상해하이니", "중국", "위식도역류질환 치료 신약 '펙수프라잔'",
     None, 3800, "달러 금액 미표기", "약 3,800억원"),
    ("3. 31.", "이뮨온시아", "3D메디슨", "중국", "CD47 항체 항암신약후보 물질 'IMC-002'",
     47050, 5400, "", "약 5,400억원 (약 4억 7,050만 달러)"),
    ("3. 31.", "펩트론", "치루제약", "중국",
     "표적항암 항체치료제 / MUC1 타겟 암 치료용 항체 후보 약물-접합체(ADC) 'PAb001-ADC'",
     53900, 6340, "", "약 6,340억원 (약 5억 3,900만 달러)"),
    ("4. 28.", "LG화학", "트랜스테라 바이오사이언스", "중국", "자가면역질환 치료 후보물질 'LC510255'",
     None, None, "", "비공개"),
    ("5. 10.", "한독·CMG제약", "AUM바이오사이언스", "싱가포르", "표적항암제 후보물질 CHC2014",
     17250, 1934, "", "약 1,934억원 (약 1억 7,250만 달러)"),
    ("6. 8.", "대웅제약", "뉴로가스트릭스", "미국", "'펙수프라잔' 위식도역류질환 치료제",
     43000, 4800, "", "약 4,800억원 (약 4억 3,000만 달러)"),
    ("6. 8.", "팬젠", "VEM", "터키", "빈혈치료제 바이오시밀러 생산기술",
     300, 33.4, "", "약 33억 4,000만원 (약 300만 달러)"),
    ("6. 18.", "레고켐바이오", "익수다테라퓨틱스", "영국", "항체약물접합체 플랫폼기술",
     None, 4237, "달러 금액 미표기", "4,237억원"),
    ("6. 24.", "대웅제약", "", "중남미 4개국", "위식도역류질환 치료제 '펙수프라잔(Fexuprazan)'",
     None, 340, "원문에 상대사 미기재(수출 대상국만 표기), 달러 금액 미표기", "약 340억원"),
    ("6. 28.", "HK이노엔", "뤄신", "중국", "'케이캡' 위식도 역류질환 치료주사",
     None, None, "", "비공개"),
    ("6. 28.", "툴젠", "카세릭스", "호주", "CAR-T 치료제",
     None, 1500, "달러 금액 미표기", "약 1,500억원"),
    ("7. 6.", "와이바이오로직스", "피에르파브르", "프랑스", "고형암 치료를 위한 신규 항체 후보물질",
     None, 1164, "달러 금액 미표기", "약 1,164억원"),
    ("7. 20.", "동아에스티", "인타스", "다국적",
     "스텔라라 바이오시밀러 'DMB-3115'의 글로벌 라이선스 아웃 계약",
     10500, 1200, "원문 국가 표기는 '다국적제약사'", "약 1,200억원 (총 1억 500만 달러)"),
    ("8. 21.", "동아에스티", "양쯔강약업그룹", "중국", "DA-7310(요로감염증)",
     None, None, "", "비공개"),
    ("8. 30.", "바이오팜솔루션즈", "경신제약", "중국", "소아연축·뇌전증 치료물질 계약",
     4000, 468, "", "468억원 (약 4,000만 달러)"),
    ("9. 2.", "보로노이", "브리켈바이오텍", "미국", "자가면역질환 치료제 프로그램",
     32350, 3800, "", "약 3,800억원 (3억 2,350만 달러)"),
    ("9. 27.", "디앤디파마텍", "선전 살루브리스 제약", "중국", "대사성질환 치료제 DD01",
     400, 47, "총 계약규모 비공개, 계약금만 공개", "비공개 / 계약금 약 47억원 (약 400만 달러)"),
    ("10. 12.", "올릭스", "한소제약", "중국", "GalNAc-asiRNA 기반 기술 관련 신약후보물질 2종",
     45100, 5368, "", "5,368억원 (약 4억 5,100만 달러)"),
    ("10. 14.", "에이프릴바이오", "룬드벡", "덴마크", "자가면역 질환 치료 후보물질 APB-A1",
     44800, 5370, "", "약 5,370억원 (4억 4,800만 달러)"),
    ("10. 15.", "대웅제약", "아그라스 등",
     "중동 6개국(사우디아라비아·아랍에미리트·쿠웨이트·바레인·오만·카타르)",
     "위식도역류질환 치료 신약 '펙수프라잔' 라이선스아웃(기술수출)",
     8466, 991, "아그라스는 아랍에미리트 소재", "약 991억원 (약 8,466만 달러)"),
    ("10. 27.", "큐라클", "테아오픈이노베이션", "프랑스",
     "당뇨병성 황반부종 및 습성 황반변성 치료제 'CU06-RE'",
     16350, 1906.9005, "", "약 1,906억 9,005만원 (1억 6,350만 달러)"),
    ("10. 28.", "고바이오랩", "상해의약그룹 자회사 신이", "중국", "면역질환 치료 소재 KBL697와 KBL693",
     11000, 1200, "", "약 1,200억원 (1억 1,000만 달러)"),
    ("11. 4.", "한미약품", "앱토즈 바이오사이언스", "캐나다", "급성골수성 백혈병(AML) 치료 신약 'HM43239'",
     42000, 4961, "", "약 4,961억원 (4억 2,000만 달러)"),
    ("11. 11.", "SK바이오팜", "이그니스테라퓨틱스", "중국", "세노바메이트 등 6개 CNS 신약",
     18500, 2180, "지분 형태", "약 2,180억원(지분) (1억 8,500만 달러)"),
    ("11. 17.", "보로노이", "피라미드바이오사이언스", "미국", "MPS1 타겟 고형암치료제(VRN08)",
     84600, 10000, "", "약 1조원 (8억 4,600만 달러)"),
    ("11. 17.", "레고켐바이오", "소티오바이오텍", "체코", "항체약물접합체(ADC) 플랫폼 기술",
     102750, 12127, "", "약 1조 2,127억원 (10억 2,750만 달러)"),
    ("12. 23.", "SK바이오팜", "엔도그룹", "아일랜드", "세노바메이트",
     4100, 433.0465, "", "433억 465만원 / 4,100만 달러"),
    ("12. 23.", "HK이노엔", "브레인트리 래보라토리스", "미국", "케이캡(테고프라잔)",
     54000, 6400, "", "6,400억원 / 5억 4,000만 달러"),
    ("12. 27.", "레고켐바이오사이언스", "익수다테라퓨틱스", "영국", "표적유방암치료제 LCB14(HER2-ADC)",
     100000, 11864, "", "1조 1,864억원 / 10억 달러"),
    ("12. 31.", "한미약품", "에퍼메드 테라퓨틱스", "중국", "안과분야 신약 루미네이트(리수테가닙)",
     14500, 1719, "", "약 1,719억원 / 1억 4,500만 달러"),
]

HEADERS = ["번호", "일자", "개발사", "계약상대", "국가", "제품/적응증/기술",
           "계약규모(만달러)", "계약규모(억원)", "비고", "원문(계약규모)"]
WIDTHS = [6, 10, 20, 26, 22, 48, 16, 16, 30, 44]

HDR_FILL = PatternFill("solid", fgColor="1F3864")
SUM_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

USD_COL, KRW_COL, NOTE_COL = 7, 8, 9


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "기술수출 33건"

    ws.cell(1, 1, TITLE).font = Font(FONT, size=14, bold=True)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
    ws.row_dimensions[1].height = 22

    for i, h in enumerate(HEADERS, start=1):
        cell = ws.cell(2, i, h)
        cell.font = Font(FONT, size=10, bold=True, color="FFFFFF")
        cell.fill = HDR_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = WIDTHS[i - 1]
    ws.row_dimensions[2].height = 30

    for r, row in enumerate(ROWS, start=3):
        values = (r - 2,) + row
        for i, v in enumerate(values, start=1):
            cell = ws.cell(r, i, v)
            cell.font = Font(FONT, size=10)
            cell.border = BORDER
            if i in (USD_COL, KRW_COL):
                cell.number_format = "#,##0.####"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif i in (1, 2, 5):
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    last = 2 + len(ROWS)
    total_row = last + 1
    for i in range(1, len(HEADERS) + 1):
        cell = ws.cell(total_row, i)
        cell.font = Font(FONT, size=10, bold=True)
        cell.fill = SUM_FILL
        cell.border = BORDER
        if i == 1:
            cell.value = "합계"
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif i == 2:
            cell.value = f"=COUNTA(C3:C{last})&\"건\""
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif i in (USD_COL, KRW_COL):
            col = get_column_letter(i)
            cell.value = f"=SUM({col}3:{col}{last})"
            cell.number_format = "#,##0.####"
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif i == NOTE_COL:
            cell.value = "비공개 건 제외 합계"
            cell.alignment = Alignment(horizontal="left", vertical="center")

    notes = [
        "※ 계약규모는 원문 표기를 단위 통일해 숫자만 입력(만 달러 / 억 원 기준). 비공개 건은 빈칸이므로 합계에서 제외됨. 원문 표기는 우측 '원문(계약규모)' 열 참조.",
        "※ 원문 표의 '계약상대(국가)' 한 칸을 계약상대 / 국가 두 열로 분리함.",
        "※ 원문 표에는 달러 금액이 없는 건이 있어 '계약규모(만달러)' 합계 건수는 '계약규모(억원)' 합계 건수보다 적음.",
        "※ 원문 표기 총액은 13조 3,720억원. 본 시트의 억원 합계는 원문 각 행을 반올림 없이 더한 값이라 약 13억원(0.01%) 차이가 남.",
        "※ 원문 표에 연도 표기가 없음(일자 1. 7. ~ 12. 31. 1년치).",
    ]
    for k, text in enumerate(notes):
        c = ws.cell(total_row + 2 + k, 1, text)
        c.font = Font(FONT, size=9, italic=True, color="808080")

    ws.freeze_panes = "C3"
    ws.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS))}{last}"

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
