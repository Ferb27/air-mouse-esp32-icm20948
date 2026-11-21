import os
import win32com.client

docx_path = os.path.abspath("BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx")  # ban nop o thu muc goc
pdf_path = os.path.abspath("BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.pdf")

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

try:
    doc = word.Documents.Open(docx_path)
    # Update fields in all story ranges (including headers and footers)
    for story in doc.StoryRanges:
        story.Fields.Update()
        next_story = story.NextStoryRange
        while next_story:
            next_story.Fields.Update()
            next_story = next_story.NextStoryRange
            
    doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
    page_count = doc.ComputeStatistics(2) # 2 = wdStatisticPages
    doc.Close(False)
    print(f"[SUCCESS] PDF generated: {pdf_path}")
    print(f"[PAGE COUNT] Total pages: {page_count}")
finally:
    word.Quit()
