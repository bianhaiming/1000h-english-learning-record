import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

# 定义自定义路径
source_path = '/path/to/source'  # 源文件夹路径
output_path = '/path/to/output'  # 输出文件夹路径

def reformat_docx(file_path, output_path):
    doc = Document(file_path)
    
    # 遍历文档中的每个段落
    for para in doc.paragraphs:
        # 设置段落对齐方式
        para.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        
        # 调整字体大小，如果段落内容很大，则调整为更小的字体
        for run in para.runs:
            # 默认使用小六号字体（相当于8pt）
            run.font.size = Pt(8)
            # 修改字体为宋体（Windows系统常用中文字体）
            run.font.name = 'SimSun'
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
        
    # 保存文件到输出路径，文件名加上_reformat后缀
    filename = os.path.basename(file_path)
    new_filename = filename.replace('.docx', '_reformat.docx')
    output_file_path = os.path.join(output_path, new_filename)
    
    doc.save(output_file_path)

def scan_and_reformat(source_path, output_path):
    # 扫描源文件夹，找到所有的.docx文件
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith('.docx'):
                file_path = os.path.join(root, file)
                reformat_docx(file_path, output_path)

# 执行文件扫描和重新排版
scan_and_reformat(source_path, output_path)
