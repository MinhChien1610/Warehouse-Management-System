import tkinter as tk
from tkinter import messagebox
import ctypes
import json
import os

from GUI.Common.base import GiaoDienCoSo


# =========================
# MÀU GIAO DIỆN
# =========================

MAU_NEN = "#F5F1EE"
MAU_CARD = "white"

MAU_CHU_DAM = "#3B2F2F"
MAU_CHU_PHU = "#8C7B75"

MAU_LABEL = "#5C4E4E"

MAU_INPUT = "#FCFAF8"
MAU_VIEN = "#E0D8D2"

MAU_NUT = "#C89F8A"
MAU_NUT_HOVER = "#B98E78"


# =========================
# TẠO LABEL
# =========================
def tao_label(parent, text, color, size, bold=False):

    font_style = ("Arial", size)

    if bold:
        font_style = ("Arial", size, "bold")

    label = tk.Label(
        parent,
        text=text,
        bg=MAU_CARD,
        fg=color,
        font=font_style
    )

    return label


# =========================
# TẠO Ô NHẬP
# =========================
def tao_o_nhap(parent, text, is_password=False):

    label = tk.Label(
        parent,
        text=text,
        bg=MAU_CARD,
        fg=MAU_LABEL,
        font=("Arial", 10, "bold"),
        anchor="w"
    )

    label.pack(fill="x")

    entry = tk.Entry(
        parent,
        bg=MAU_INPUT,
        fg=MAU_CHU_DAM,
        font=("Arial", 12),
        bd=0,
        relief="solid",
        highlightthickness=1,
        highlightbackground=MAU_VIEN,
        highlightcolor=MAU_NUT,
        show="*" if is_password else ""
    )

    entry.pack(
        fill="x",
        ipady=10,
        pady=(5, 20)
    )

    return entry


# =========================
# XỬ LÝ ĐĂNG NHẬP
# =========================
def lay_thu_muc_goc():
    return GiaoDienCoSo.lay_thu_muc_goc()


def doc_json(ten_file, mac_dinh=None):
    return GiaoDienCoSo.doc_json(ten_file, mac_dinh)


def lay_vai_tro_tai_khoan(data, ma_tai_khoan):
    vai_tro_map = {}

    for vai_tro in data.get("vaiTro", []):
        vai_tro_map[vai_tro.get("maVaiTro", "")] = vai_tro.get("tenVaiTro", "")

    ket_qua = []

    for phan_quyen in data.get("phanQuyen", []):
        if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
            ket_qua.append(vai_tro_map.get(phan_quyen.get("maVaiTro", ""), ""))

    return ket_qua


def dang_nhap_vao_giao_dien(root, tai_khoan, vai_tro):
    root.destroy()
    ten_vai_tro = str(vai_tro).strip().lower()

    if ten_vai_tro == "admin":
        from GUI.Admin.admin import hien_thi_admin
        hien_thi_admin(tai_khoan)
        return

    if ten_vai_tro in ["nhanvienkho", "nhân viên kho"]:
        from GUI.NhanVienKho.nhanvienkho import hien_thi_nhan_vien_kho
        hien_thi_nhan_vien_kho(tai_khoan)
        return

    if ten_vai_tro in ["ketoan", "kế toán"]:
        from GUI.KeToan.ketoan import hien_thi_ke_toan
        hien_thi_ke_toan(tai_khoan)
        return

    messagebox.showerror("Lỗi", "Tài khoản chưa được phân quyền giao diện.")


def xu_ly_dang_nhap(entry_username, entry_password):

    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Thông báo",
            "Vui lòng nhập đầy đủ thông tin!"
        )
        return

    data = doc_json("nguoi_dung.json", {})

    for tai_khoan in data.get("taiKhoan", []):
        dung_ten = tai_khoan.get("tenTaiKhoan", "") == username
        dung_mat_khau = tai_khoan.get("matKhau", "") == password
        trang_thai = str(tai_khoan.get("trangThai", "")).strip().lower()
        dang_hoat_dong = trang_thai in ["true", "1", "hoạt động", "active"]

        if dung_ten and dung_mat_khau:
            if not dang_hoat_dong:
                messagebox.showwarning("Thông báo", "Tài khoản đã bị khóa.")
                return

            vai_tro = lay_vai_tro_tai_khoan(data, tai_khoan.get("maTaiKhoan", ""))

            if len(vai_tro) == 0:
                messagebox.showerror("Lỗi", "Tài khoản chưa được phân quyền.")
                return

            dang_nhap_vao_giao_dien(entry_username.winfo_toplevel(), tai_khoan, vai_tro[0])
            return

    messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")


# =========================
# TẠO NÚT ĐĂNG NHẬP
# =========================
def tao_nut_dang_nhap(parent, command):

    button = tk.Button(
        parent,
        text="ĐĂNG NHẬP",
        bg=MAU_NUT,
        fg="white",
        activebackground=MAU_NUT_HOVER,
        activeforeground="white",
        font=("Arial", 12, "bold"),
        bd=0,
        cursor="hand2",
        command=command
    )

    button.pack(
        fill="x",
        ipady=10,
        pady=(10, 10)
    )

    return button


# =========================
# GIAO DIỆN LOGIN
# =========================
def hien_thi_login():

    root = tk.Tk()

    root.title("Đăng nhập Hệ thống")

    root.geometry("450x650")

    root.configure(bg=MAU_NEN)

    root.resizable(False, False)

    # =========================
    # CARD TRẮNG
    # =========================
    card = tk.Frame(
        root,
        bg=MAU_CARD,
        padx=40,
        pady=40,
        highlightbackground=MAU_VIEN,
        highlightthickness=1
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=380,
        height=540
    )

    # =========================
    # TIÊU ĐỀ
    # =========================
    title = tao_label(
        card,
        "Đăng nhập",
        MAU_CHU_DAM,
        30,
        True
    )

    title.pack(pady=(10, 5))

    subtitle = tao_label(
        card,
        "Hệ thống quản lý kho hàng",
        MAU_CHU_PHU,
        11
    )

    subtitle.pack(pady=(0, 40))

    # =========================
    # Ô nhập
    # =========================
    entry_username = tao_o_nhap(
        card,
        "Tên đăng nhập"
    )

    entry_password = tao_o_nhap(
        card,
        "Mật khẩu",
        True
    )

    # =========================
    # Nút đăng nhập
    # =========================
    tao_nut_dang_nhap(
        card,
        lambda: xu_ly_dang_nhap(
            entry_username,
            entry_password
        )
    )

    # =========================
    # GHI CHÚ
    # =========================
    note = tao_label(
        card,
        "Tài khoản và mật khẩu được quản trị viên cấp",
        "#A0908A",
        9
    )

    note.pack(pady=(10, 0))

    root.mainloop()

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# =========================
# CHẠY CHƯƠNG TRÌNH
# =========================
if __name__ == "__main__":
    hien_thi_login()
