import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM students")
if cursor.fetchone()[0] == 0:
    students_data = [
        ("Đặng Đức Anh", "CNTT", 3.2),
        ("Đoàn Anh Tuấn", "Kinh tế", 2.8),
        ("Trần Tuấn Long", "Y dược", 3.6),
        ("Nguyễn Thiện Thuật", "Luật", 1.9),
        ("Cao Bá Quát", "Xây dựng", 2.5)
    ]
    cursor.executemany(
        "INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
        students_data
    )
    conn.commit()

def add_student():
    name = entry_name.get()
    major = entry_major.get()
    gpa = entry_gpa.get()

    if name == "" or major == "" or gpa == "":
        messagebox.showwarning("Lỗi", "Nhập đầy đủ thông tin!")
        return

    try:
        cursor.execute("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
                       (name, major, float(gpa)))
        conn.commit()
        messagebox.showinfo("OK", "Thêm thành công!")
        show_all()
    except:
        messagebox.showerror("Lỗi", "GPA phải là số!")

def show_all():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        text = f"ID: {row[0]} | Tên: {row[1]} | Ngành: {row[2]} | GPA: {row[3]}"
        listbox.insert(tk.END, text)

def show_gpa():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
    for row in cursor.fetchall():
        text = f"ID: {row[0]} | Tên: {row[1]} | Ngành: {row[2]} | GPA: {row[3]}"
        listbox.insert(tk.END, text)

def update_gpa():
    try:
        selected = listbox.get(listbox.curselection())
        new_gpa = float(entry_gpa.get())

        cursor.execute("UPDATE students SET gpa=? WHERE id=?",
                       (new_gpa, selected[0]))
        conn.commit()
        messagebox.showinfo("OK", "Cập nhật thành công!")
        show_all()
    except:
        messagebox.showwarning("Lỗi", "Chọn sinh viên và nhập GPA hợp lệ!")

def delete_low_gpa():
    cursor.execute("DELETE FROM students WHERE gpa < 2.0")
    conn.commit()
    messagebox.showinfo("OK", "Đã xóa sinh viên GPA < 2.0")
    show_all()

def delete_all():
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa TẤT CẢ sinh viên?")
    if confirm:
        cursor.execute("DELETE FROM students")
        conn.commit()
        messagebox.showinfo("OK", "Đã xóa toàn bộ sinh viên!")
        show_all()

root = tk.Tk()
root.title("Quản lý sinh viên")
root.geometry("620x620")
root.configure(bg="#1e1e1e")

listbox = tk.Listbox(
    root,
    width=60,
    height=10,
    bg="#2b2b2b",
    fg="white",
    font=("Consolas", 14),
    selectbackground="#4CAF50"
)
listbox.pack(pady=10)

frame_input = tk.Frame(root, bg="#1e1e1e")
frame_input.pack()

label_font = ("Arial", 14)
entry_font = ("Arial", 14)

tk.Label(frame_input, text="Tên", bg="#1e1e1e", fg="white", font=label_font).grid(row=0, column=0)
entry_name = tk.Entry(frame_input, font=entry_font, bg="#3a3a3a", fg="white", insertbackground="white")
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Ngành", bg="#1e1e1e", fg="white", font=label_font).grid(row=1, column=0)
entry_major = tk.Entry(frame_input, font=entry_font, bg="#3a3a3a", fg="white", insertbackground="white")
entry_major.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="GPA", bg="#1e1e1e", fg="white", font=label_font).grid(row=2, column=0)
entry_gpa = tk.Entry(frame_input, font=entry_font, bg="#3a3a3a", fg="white", insertbackground="white")
entry_gpa.grid(row=2, column=1, padx=5, pady=5)

frame_btn = tk.Frame(root, bg="#1e1e1e")
frame_btn.pack(pady=10)

btn_font = ("Arial", 13, "bold")

def create_btn(text, cmd, color):
    return tk.Button(
        frame_btn,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        width=18,
        font=btn_font,
        relief="flat"
    )

create_btn("Thêm sinh viên", add_student, "#4CAF50").grid(row=0, column=0, padx=5, pady=5)
create_btn("Hiển thị tất cả", show_all, "#2196F3").grid(row=0, column=1, padx=5, pady=5)
create_btn("GPA > 3.0", show_gpa, "#9C27B0").grid(row=1, column=0, padx=5, pady=5)
create_btn("Cập nhật GPA", update_gpa, "#FF9800").grid(row=1, column=1, padx=5, pady=5)
create_btn("Xóa GPA < 2.0", delete_low_gpa, "#F44336").grid(row=2, column=0, padx=5, pady=5)
create_btn("Xóa tất cả", delete_all, "#b71c1c").grid(row=2, column=1, padx=5, pady=5)
show_all()
root.mainloop()
conn.close()