"""
2020년 기술수출 현황(단위: 억원) 표를 단독 엑셀 파일로 정리.

원자료: 보도 표 이미지 1종 (회사명 / 파이프라인 / 기술료(억원) / 비고 / 일자)
출력:  output/k_bio_licensing_2020.xlsx

원문의 '비고' 칸(예: "영국 익수다테라퓨틱스")은 계약상대 / 국가 두 열로 분리했다.
기술료는 원문이 이미 억원 단위이므로 숫자만 입력하고 하단에 SUM 합계 행을 뒀다.
금액이 비어 있는 건(이수앱지스, 이뮤니스바이오)은 빈칸이라 합계에서 제외된다.
"""

from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
OUT = BASE / "output" / "k_bio_licensing_2020.xlsx"

FONT = "Arial"
TITLE = "2020년 기술수출 현황 (단위: 억원)"

# 월, 개발사, 계약상대, 국가, 적응증, 기술료(억원), 비고
ROWS = [
    (3, "이뮤니스바이오", "NK 바이오셀", "말레이시아", "면역세포치료제", None, "원문 기술료 미기재"),
    (4, "레고켐바이오", "익수다테라퓨틱스", "영국", "항체·약물 복합체(ADC) 기술", 4963, ""),
    (5, "퓨쳐켐", "이아손", "오스트리아", "전립선암 진단 신약", 16, ""),
    (6, "레고켐바이오", "익수다테라퓨틱스", "영국", "항체·약물 복합체(ADC) 기술", 2784, ""),
    (6, "알테오젠", "글로벌 10대 제약사(비공개)", "", "인간 히알루로니다아제 원천기술", 46770, "원문 국가 미표기(상대사 비공개)"),
    (8, "한미약품", "MSD", "미국", "비알코올성 지방간염(NASH)", 10273, "원문 국가 미표기, 상대사 소재국으로 보완"),
    (8, "유한양행", "프로세사 파머수티컬", "미국", "기능성 위장관 질환 신약", 5000, ""),
    (9, "퓨쳐켐", "HTA", "중국", "전립선암 진단 신약", 6500, ""),
    (10, "레고켐바이오", "시스톤 파마수티컬스", "중국", "항체-약물 복합체(ADC) 기반 항암제", 4000, ""),
    (10, "올릭스", "떼아", "프랑스", "안과질환 치료제", 8873, ""),
    (10, "SK바이오팜", "오노약품공업", "일본", "뇌전증 신약", 5800, ""),
    (10, "보로노이", "오릭", "미국", "돌연변이 비소세포폐암·고형암", 7200, ""),
    (10, "JW홀딩스", "산동뤄신제약그룹", "중국", "3체임버 종합영양수액제", 440, "원문 국가 미표기, 상대사 소재국으로 보완"),
    (11, "크리스탈지노믹스", "마카온(자회사)", "", "아이발티노스타트", 1070, "원문 국가 미표기"),
    (11, "이수앱지스", "파마신테즈", "러시아", "바이오시밀러", None, "원문 기술료 미기재"),
    (12, "레고켐바이오", "피식스 온콜로지", "미국", "항체-약물 복합체(ADC) 기반 항암제", 3255, ""),
]

HEADERS = ["번호", "일자(월)", "개발사", "계약상대", "국가", "적응증", "기술료(억원)", "비고"]
WIDTHS = [6, 10, 18, 26, 12, 36, 14, 34]

HDR_FILL = PatternFill("solid", fgColor="1F3864")
SUM_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

MONTH_COL, FEE_COL, NOTE_COL = 2, 7, 8


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2020년 기술수출"

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
    ws.row_dimensions[2].height = 26

    for r, row in enumerate(ROWS, start=3):
        for i, v in enumerate((r - 2,) + row, start=1):
            cell = ws.cell(r, i, v)
            cell.font = Font(FONT, size=10)
            cell.border = BORDER
            if i == MONTH_COL:
                cell.number_format = '0"월"'  # 숫자로 저장해 월 순 정렬이 되게
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif i == FEE_COL:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif i in (1, 5):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    last = 2 + len(ROWS)
    total_row = last + 1
    fee = get_column_letter(FEE_COL)
    for i in range(1, len(HEADERS) + 1):
        cell = ws.cell(total_row, i)
        cell.font = Font(FONT, size=10, bold=True)
        cell.fill = SUM_FILL
        cell.border = BORDER
        if i == 1:
            cell.value = "합계"
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif i == 3:
            cell.value = f"=COUNTA(C3:C{last})&\"건\""
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif i == FEE_COL:
            cell.value = f"=SUM({fee}3:{fee}{last})"
            cell.number_format = "#,##0"
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif i == NOTE_COL:
            cell.value = f"=\"금액 공개 \"&COUNT({fee}3:{fee}{last})&\"건 합계\""
            cell.alignment = Alignment(horizontal="left", vertical="center")

    notes = [
        "※ 기술료는 원문이 이미 억원 단위라 숫자만 입력함(계약 총 규모가 아니라 원문 표의 '기술료' 값).",
        "※ 원문 '비고' 칸의 '국가 + 상대사' 표기를 계약상대 / 국가 두 열로 분리함.",
        "※ 원문에 국가가 없던 건은 상대사 소재국으로 보완하고 비고에 표시(한미약품-MSD, JW홀딩스-산동뤄신제약그룹). 알테오젠·크리스탈지노믹스 건은 확인이 안 돼 빈칸으로 둠.",
        "※ 이수앱지스, 이뮤니스바이오 2건은 원문에 금액이 없어 빈칸이며 합계에서 제외됨.",
        "※ 일자는 월 숫자로 저장하고 표시 형식만 '○월'로 지정해 월 순 정렬이 되게 함.",
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
