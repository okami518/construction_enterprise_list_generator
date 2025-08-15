import pdfplumber
import tkinter as tk
from tkinter import filedialog


def main():
    file_path = select_file()
    if file_path:
        read_document(file_path)


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='選擇 PDF 檔案', filetypes=[("PDF files", "*.pdf")])
    return file_path


def read_document(file):
    lst = []
    best = []
    great = []
    with pdfplumber.open(file) as p:
        for page in p.pages:  # enumerate可以產生迭代對象的index，enumerate(迭代對像, index起始值)
            table = page.extract_tables()  # tables = 從page中的表格提取得文字內容（所以不是一行一行，是儲存格）
            if table:  # 如果有內容才做
                for rows in table:
                    for row in rows:
                        for cell in row:
                            if isinstance(cell, str):  # isinstance可以檢查string是否為str
                                my_str = cell.replace("\n", "")  # 把\n(換行符號)改掉
                                lst.append(my_str)  # 把處理好的my_str放入 lst中
                        # print(lst)
                        if len(lst) > 1 and lst[1] == "建築":  # 篩選是土木類別的
                            if lst[14] == 'V' and lst[9] not in best:  # 如果是特優且沒出現過放進去
                                best.append(lst[9])
                            elif lst[13] == 'V' and lst[9] not in great:  # 如果是優等且沒出現過放進去
                                great.append(lst[9])

                        lst = []  # 進到下一列要清空
            else:
                # 如果無表格，提取普通文字
                print(page.extract_text())
    output(best, great)


def output(best, great):
    with open(r'營造廠名單.txt', 'w', encoding='utf-8') as file:
        file.write("特優：")
        for item in best:
            file.write(f"{item}/")

        file.write('\n')

        file.write('優等：')
        for item in great:
            file.write(f"{item}/")


if __name__ == '__main__':
    main()
