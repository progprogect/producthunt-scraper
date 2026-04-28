"""Excel exporter — writes scored hunters to .xlsx."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path
from datetime import datetime

def export_to_excel(hunters, output_path="", include_below=False):
    rows = [h for h in hunters if h.get("linkedin_url")]
    if not include_below:
        rows = [h for h in rows if h.get("segment") in ("Priority","Secondary")]
    rows.sort(key=lambda h: h.get("score",0), reverse=True)
    if not output_path:
        output_path = str(Path.home()/"Downloads"/f"ph_hunters_{datetime.now().strftime(\'%Y%m%d_%H%M\')}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "PH Hunters"
    HDRS = ["Name","PH Profile","LinkedIn","Score","Segment","PH Followers","X Followers",
            "Categories","Geo","Last Activity","Products Hunted","Avg Upvotes","Twitter"]
    WIDTHS = [22,38,45,8,12,14,12,42,22,14,16,16,18]
    hf = Font(bold=True, color="FFFFFF", name="Calibri")
    hfill = PatternFill(start_color="1E2A3A", end_color="1E2A3A", fill_type="solid")
    for ci,(h,w) in enumerate(zip(HDRS,WIDTHS),1):
        c=ws.cell(row=1,column=ci,value=h); c.font=hf; c.fill=hfill
        c.alignment=Alignment(horizontal="center",vertical="center")
        ws.column_dimensions[get_column_letter(ci)].width=w
    pri_fill=PatternFill(start_color="C6EFCE",end_color="C6EFCE",fill_type="solid")
    sec_fill=PatternFill(start_color="FFEB9C",end_color="FFEB9C",fill_type="solid")
    for ri,h in enumerate(rows,2):
        seg=h.get("segment",""); fill=pri_fill if seg=="Priority" else (sec_fill if seg=="Secondary" else None)
        country=h.get("country",""); geo=f"🇪🇺 {country}" if h.get("is_eu") else (country or "N/A")
        data=[h.get("name",h.get("username","")),h.get("ph_url",""),h.get("linkedin_url",""),
              h.get("score",0),seg,h.get("ph_followers",0),h.get("x_followers",0),
              ", ".join(str(c) for c in (h.get("categories") or [])[:5]),geo,
              str(h.get("last_activity_date",""))[:10],h.get("products_hunted",0),
              round(h.get("avg_upvotes_last_10",0),1),h.get("twitter_username","")]
        for ci,v in enumerate(data,1):
            c=ws.cell(row=ri,column=ci,value=v)
            if fill: c.fill=fill
            if ci in (2,3) and v and str(v).startswith("http"):
                c.hyperlink=str(v); c.font=Font(color="0563C1",underline="single")
    ws.freeze_panes="A2"
    ws.auto_filter.ref=f"A1:{get_column_letter(len(HDRS))}{max(len(rows),1)+1}"
    wb.save(output_path)
    return output_path
