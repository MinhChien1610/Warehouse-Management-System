import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Calculator import admin as tinh_admin
from Calculator import tonkho as tinh_ton_kho
from GUI.Common.base import GiaoDienCoSo
from CRUD.Admin.admin import NghiepVuAdmin


# =========================
# XỬ LÝ FILE JSON
# =========================
def tao_base_helper():
    return GiaoDienCoSo()


def lay_thu_muc_goc():
    helper = tao_base_helper()
    return helper.lay_thu_muc_goc()


def doc_json(ten_file, mac_dinh=None):
    helper = tao_base_helper()
    return helper.doc_json(ten_file, mac_dinh)


def ghi_json(ten_file, data):
    helper = tao_base_helper()
    helper.ghi_json(ten_file, data)


# =========================
# GIAO DIỆN ADMIN
# =========================
class GiaoDienAdmin(GiaoDienCoSo):
    def __init__(self, tai_khoan_dang_nhap=None):
        super().__init__()
        self.khoi_tao_mau_admin()

        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap
        self.nghiep_vu_admin = NghiepVuAdmin(lay_thu_muc_goc(), tai_khoan_dang_nhap)

        self.root = tk.Tk()
        self.root.title("Admin")
        self.root.geometry("1280x720")
        self.root.minsize(1120, 640)
        self.root.configure(bg=self.mau_nen)

        self.danh_sach_menu = []

        self.cau_hinh_style()
        self.tao_bo_cuc_chinh()
        self.tao_sidebar()
        self.hien_trang_chu()








    def khoi_tao_mau_admin(self):
        self.khoi_tao_mau_sac()

    def cau_hinh_style(self):
        super().cau_hinh_style()

    def chay(self):
        self.root.mainloop()

    # =========================
    # BỐ CỤC CHÍNH
    # =========================



    def tao_bo_cuc_chinh(self):
        self.sidebar = tk.Frame(
            self.root,
            bg=self.mau_sidebar,
            width=238,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self.root,
            bg=self.mau_nen,
        )
        self.content.pack(side="right", fill="both", expand=True)




    def tao_sidebar(self):
        logo = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        logo.pack(fill="x", padx=14, pady=(16, 10))

        top_logo = tk.Frame(logo, bg=self.mau_sidebar)
        top_logo.pack(fill="x")

        icon_box = tk.Frame(
            top_logo,
            bg=self.mau_card,
            width=46,
            height=46,
            highlightbackground=self.mau_blue_sang,
            highlightthickness=1,
        )
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)

        tk.Label(
            icon_box,
            text="📦",
            bg=self.mau_card,
            fg=self.mau_menu_chon,
            font=("Segoe UI", 19),
        ).place(relx=0.5, rely=0.5, anchor="center")

        text_logo = tk.Frame(top_logo, bg=self.mau_sidebar)
        text_logo.pack(side="left", padx=(10, 0))

        tk.Label(
            text_logo,
            text="ADMIN",
            bg=self.mau_sidebar,
            fg="white",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            text_logo,
            text="Warehouse",
            bg=self.mau_sidebar,
            fg=self.mau_sidebar_nhat,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")

        slogan = tk.Frame(
            logo,
            bg=self.mau_sidebar_dam,
            highlightbackground=self.mau_blue_sang,
            highlightthickness=1,
        )
        slogan.pack(fill="x", pady=(12, 0))

        tk.Label(
            slogan,
            text="Quản trị kho hàng",
            bg=self.mau_sidebar_dam,
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=(7, 1))

        tk.Label(
            slogan,
            text="Theo dõi • Báo cáo",
            bg=self.mau_sidebar_dam,
            fg=self.mau_sidebar_nhat,
            font=("Segoe UI", 8),
        ).pack(anchor="w", padx=10, pady=(0, 7))

        vung_menu = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        vung_menu.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        canvas_menu = tk.Canvas(
            vung_menu,
            bg=self.mau_sidebar,
            bd=0,
            highlightthickness=0,
        )
        canvas_menu.pack(side="left", fill="both", expand=True)

        thanh_cuon_menu = ttk.Scrollbar(
            vung_menu,
            orient="vertical",
            command=canvas_menu.yview,
        )
        thanh_cuon_menu.pack(side="right", fill="y")

        canvas_menu.configure(yscrollcommand=thanh_cuon_menu.set)

        menu = tk.Frame(canvas_menu, bg=self.mau_sidebar)
        menu_window = canvas_menu.create_window((0, 0), window=menu, anchor="nw")

        def cap_nhat_vung_cuon(event=None):
            canvas_menu.configure(scrollregion=canvas_menu.bbox("all"))
            canvas_menu.itemconfigure(menu_window, width=canvas_menu.winfo_width())

        def cuon_menu(event):
            canvas_menu.yview_scroll(int(-1 * (event.delta / 120)), "units")

        menu.bind("<Configure>", cap_nhat_vung_cuon)
        canvas_menu.bind("<Configure>", cap_nhat_vung_cuon)
        canvas_menu.bind("<Enter>", lambda event: canvas_menu.bind_all("<MouseWheel>", cuon_menu))
        canvas_menu.bind("<Leave>", lambda event: canvas_menu.unbind_all("<MouseWheel>"))

        self.tao_nut_menu(menu, "🏠  Trang chủ", self.hien_trang_chu)

        self.tao_menu_xo_sidebar(
            menu,
            "👥  Nhân viên",
            [
                ("Danh sách nhân viên", self.hien_nhan_vien),
                ("Danh sách tài khoản", self.hien_tai_khoan),
            ],
        )

        self.tao_menu_xo_sidebar(
            menu,
            "🏬  Kho",
            [
                ("Danh sách kho", self.hien_kho),
                ("Nhập kho", self.hien_nhap_kho),
                ("Xuất kho", self.hien_xuat_kho),
                ("Tồn kho", self.hien_ton_kho),
                ("Kiểm kho", self.hien_kiem_kho),
            ],
        )

        self.tao_menu_xo_sidebar(
            menu,
            "📦  Hàng hóa",
            [
                ("Danh mục hàng hóa", self.hien_hang_hoa),
                ("Loại hàng", self.hien_loai_hang),
                ("Nhà sản xuất", self.hien_nha_san_xuat),
            ],
        )

        self.tao_menu_xo_sidebar(
            menu,
            "📊  Thống kê",
            [
                ("Tổng quan", self.hien_thong_ke_tong_quan),
                ("Thống kê nhập kho", self.hien_thong_ke_nhap_kho),
                ("Thống kê xuất kho", self.hien_thong_ke_xuat_kho),
                ("Doanh thu theo kho", self.hien_doanh_thu_theo_kho),
                ("Cảnh báo tồn thấp", self.hien_canh_bao_ton_thap),
            ],
        )

        self.tao_menu_xo_sidebar(
            menu,
            "📝  Nhật ký",
            [
                ("Nhật ký đăng nhập", self.hien_nhat_ky_dang_nhap),
                ("Nhật ký thao tác", self.hien_nhat_ky_thao_tac),
            ],
        )

        bottom = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        bottom.pack(side="bottom", fill="x", padx=12, pady=(6, 12))

        self.tao_nut(
            bottom,
            "Đăng xuất",
            self.dang_xuat,
            self.mau_sidebar_dam,
        ).pack(fill="x")


    def tao_nut_menu(self, parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            bg=self.mau_menu,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
            relief="flat",
        )

        button.config(command=lambda: self.chon_menu(button, command))
        button.pack(fill="x", pady=(0, 10))

        self.danh_sach_menu.append(button)
        return button


    def tao_menu_xo_sidebar(self, parent, title, danh_sach_con):
        khung = tk.Frame(parent, bg=self.mau_sidebar)
        khung.pack(fill="x", pady=(0, 10))

        khung_con = tk.Frame(khung, bg=self.mau_sidebar)
        dang_mo = {"value": False}

        def toggle_menu():
            if dang_mo["value"]:
                khung_con.pack_forget()
                dang_mo["value"] = False
                nut_cha.config(text=title + "   ▾")
            else:
                khung_con.pack(fill="x", pady=(3, 0))
                dang_mo["value"] = True
                nut_cha.config(text=title + "   ▴")

        nut_cha = tk.Button(
            khung,
            text=title + "   ▾",
            bg=self.mau_menu,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
            relief="flat",
            command=toggle_menu,
        )
        nut_cha.pack(fill="x")
        self.danh_sach_menu.append(nut_cha)

        for text, command in danh_sach_con:
            nut_con = tk.Button(
                khung_con,
                text="      " + text,
                bg=self.mau_sidebar,
                fg=self.mau_sidebar_nhat,
                activebackground=self.mau_menu_hover,
                activeforeground="white",
                font=("Segoe UI", 9),
                bd=0,
                anchor="w",
                padx=14,
                pady=7,
                cursor="hand2",
                relief="flat",
            )
            nut_con.config(command=lambda btn=nut_con, cmd=command: self.chon_menu(btn, cmd))
            nut_con.pack(fill="x", pady=(2, 2))
            self.danh_sach_menu.append(nut_con)


    def chon_menu(self, button, command):
        for nut in self.danh_sach_menu:
            text = str(nut.cget("text"))

            if text.startswith("      "):
                nut.config(bg=self.mau_sidebar, fg=self.mau_sidebar_nhat)
            else:
                nut.config(bg=self.mau_menu, fg="white")

        button.config(bg=self.mau_menu_hover, fg="white")
        command()

    def tao_tieu_de_trang(self, parent, title, subtitle):
        self.xoa_noi_dung(parent)

        header = tk.Frame(parent, bg=self.mau_nen)
        header.pack(fill="x", padx=24, pady=(18, 8))

        left = tk.Frame(header, bg=self.mau_nen)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(
            left,
            text=title,
            bg=self.mau_nen,
            fg=self.mau_chu_dam,
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text=subtitle,
            bg=self.mau_nen,
            fg=self.mau_chu_phu,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 0))

        self.tao_user_box(header).pack(side="right", pady=(2, 0))

    def lay_ten_admin_hien_tai(self):
        try:
            data = doc_json("nguoi_dung.json", {})
            ma_tai_khoan = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maTaiKhoan", "") == ma_tai_khoan:
                    ma_nhan_vien = tai_khoan.get("maNhanVien", "")

                    for nhan_vien in data.get("nhanVien", []):
                        if nhan_vien.get("maNhanVien", "") == ma_nhan_vien:
                            return nhan_vien.get("tenNhanVien", "Admin")
        except Exception:
            pass

        return "Admin"

    def hien_thong_tin_admin(self):
        self.tao_tieu_de_trang(
            self.content,
            "Thông tin tài khoản",
            "Thông tin cá nhân của quản trị viên",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        data = doc_json("nguoi_dung.json", {})
        ma_tai_khoan = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")
        tai_khoan = None
        nhan_vien = None
        ten_vai_tro = "Admin"

        for item in data.get("taiKhoan", []):
            if item.get("maTaiKhoan", "") == ma_tai_khoan:
                tai_khoan = item
                break

        if tai_khoan is not None:
            ma_nhan_vien = tai_khoan.get("maNhanVien", "")
            for item in data.get("nhanVien", []):
                if item.get("maNhanVien", "") == ma_nhan_vien:
                    nhan_vien = item
                    break

            ma_vai_tro = ""
            for item in data.get("phanQuyen", []):
                if item.get("maTaiKhoan", "") == ma_tai_khoan:
                    ma_vai_tro = item.get("maVaiTro", "")
                    break

            for item in data.get("vaiTro", []):
                if item.get("maVaiTro", "") == ma_vai_tro:
                    ten_vai_tro = item.get("tenVaiTro", ten_vai_tro)
                    break

        card = self.tao_card(body)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=self.mau_card)
        inner.pack(fill="x", padx=24, pady=20)

        self.tao_label(inner, "Thông tin hệ thống", 16, self.mau_chu_dam, True).pack(anchor="w", pady=(0, 12))

        if tai_khoan is None:
            self.tao_label(inner, "Không tìm thấy tài khoản admin đang đăng nhập.", 11, self.mau_nguy_hiem).pack(anchor="w")
            return

        ten_nhan_vien = "Không xác định"
        so_dien_thoai = ""
        email = ""
        if nhan_vien is not None:
            ten_nhan_vien = nhan_vien.get("tenNhanVien", ten_nhan_vien)
            so_dien_thoai = nhan_vien.get("soDienThoai", "")
            email = nhan_vien.get("email", "")

        trang_thai = self.lay_gia_tri_trang_thai_nguoi_dung(tai_khoan.get("trangThai", ""))

        for label, value in [
            ("Mã tài khoản", tai_khoan.get("maTaiKhoan", "")),
            ("Tên tài khoản", tai_khoan.get("tenTaiKhoan", "")),
            ("Nhân viên", ten_nhan_vien),
            ("Vai trò", ten_vai_tro),
            ("Trạng thái", trang_thai),
            ("Số điện thoại", so_dien_thoai),
            ("Email", email),
        ]:
            row = tk.Frame(inner, bg=self.mau_card)
            row.pack(fill="x", pady=3)
            self.tao_dong_thong_tin(row, label, value)





    def tao_user_box(self, parent):
        user_box = tk.Frame(
            parent,
            bg=self.mau_card,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            cursor="hand2",
        )

        icon_box = tk.Frame(
            user_box,
            bg=self.mau_card_nhe,
            width=34,
            height=34,
        )
        icon_box.pack(side="left", padx=(12, 9), pady=8)
        icon_box.pack_propagate(False)

        tk.Label(
            icon_box,
            text="👤",
            bg=self.mau_card_nhe,
            fg=self.mau_menu_chon,
            font=("Segoe UI", 12),
            cursor="hand2",
        ).place(relx=0.5, rely=0.5, anchor="center")

        text_box = tk.Frame(user_box, bg=self.mau_card)
        text_box.pack(side="left", padx=(0, 14), pady=7)

        name = tk.Label(
            text_box,
            text="Xin chào, " + self.rut_gon_chu(self.lay_ten_admin_hien_tai(), 18),
            bg=self.mau_card,
            fg=self.mau_chu_dam,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )
        name.pack(anchor="w")

        role = tk.Label(
            text_box,
            text="Vai trò: Admin",
            bg=self.mau_card,
            fg=self.mau_chu_phu,
            font=("Segoe UI", 8),
            cursor="hand2",
        )
        role.pack(anchor="w", pady=(2, 0))

        user_box.bind("<Button-1>", lambda event: self.hien_thong_tin_admin())
        icon_box.bind("<Button-1>", lambda event: self.hien_thong_tin_admin())
        text_box.bind("<Button-1>", lambda event: self.hien_thong_tin_admin())
        name.bind("<Button-1>", lambda event: self.hien_thong_tin_admin())
        role.bind("<Button-1>", lambda event: self.hien_thong_tin_admin())

        return user_box


    def hien_trang_chu(self):
        self.tao_tieu_de_trang(
            self.content,
            "Trang chủ",
            "Tổng quan quản trị hệ thống kho hàng",
        )

        body = tk.Frame(self.content, bg=self.mau_nen)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 18))

        card_row = tk.Frame(body, bg=self.mau_nen)
        card_row.pack(fill="x", pady=(0, 10))
        card_row.grid_rowconfigure(0, minsize=140)

        for column in range(4):
            card_row.grid_columnconfigure(column, weight=1, uniform="card")

        self.tao_the_tong_quan(
            card_row,
            "Nhân viên",
            self.dem_nhan_vien(),
            "Tài khoản nhân sự",
            self.hien_nhan_vien,
            "👥",
            0,
        )

        self.tao_the_tong_quan(
            card_row,
            "Kho hàng",
            self.dem_so_kho(),
            "Kho đang quản lý",
            self.hien_kho,
            "🏬",
            1,
        )

        self.tao_the_tong_quan(
            card_row,
            "Hàng hóa",
            self.dem_so_hang_hoa(),
            "Sản phẩm hệ thống",
            self.hien_hang_hoa,
            "📦",
            2,
        )

        self.tao_the_tong_quan(
            card_row,
            "Tồn thấp",
            self.dem_ton_thap(),
            "Sản phẩm cần kiểm tra",
            self.hien_canh_bao_ton_thap,
            "⚠",
            3,
        )

        main = tk.Frame(body, bg=self.mau_nen)
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        left = self.tao_card(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = self.tao_card(main)
        right.grid(row=0, column=1, sticky="nsew")

        self.tao_khu_vuc_bieu_do_admin(left)
        self.tao_khu_vuc_theo_doi_admin(right, dung_cuon=False)


    def tao_the_tong_quan(self, parent, title, value, desc, command=None, icon_text="", column=None):
        card = tk.Frame(
            parent,
            bg=self.mau_card,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        card.pack_propagate(False)
        card.config(height=136)

        if column is None:
            column = len(parent.grid_slaves(row=0))

        parent.grid_rowconfigure(0, minsize=136)
        parent.grid_columnconfigure(column, weight=1)
        card.grid(row=0, column=column, sticky="nsew", padx=5)

        top = tk.Frame(card, bg=self.mau_card)
        top.pack(fill="x", padx=13, pady=(12, 0))

        if icon_text != "":
            icon = tk.Frame(
                top,
                bg=self.mau_card_nhe,
                width=30,
                height=28,
            )
            icon.pack(side="left", padx=(0, 8))
            icon.pack_propagate(False)

            tk.Label(
                icon,
                text=icon_text,
                bg=self.mau_card_nhe,
                fg=self.mau_menu_chon,
                font=("Segoe UI", 11),
            ).place(relx=0.5, rely=0.5, anchor="center")

        self.tao_label(
            top,
            title,
            10,
            self.mau_chu_dam,
            True,
            self.mau_card,
        ).pack(side="left")

        value_label = self.tao_label(
            card,
            str(value),
            21,
            self.mau_menu_chon,
            True,
            self.mau_card,
        )
        value_label.config(wraplength=210, justify="left")
        value_label.pack(anchor="w", padx=14, pady=(9, 0))

        desc_label = self.tao_label(
            card,
            desc,
            9,
            self.mau_chu_phu,
            False,
            self.mau_card,
        )
        desc_label.config(wraplength=210, justify="left")
        desc_label.pack(anchor="w", padx=14, pady=(3, 14))

        if command is not None:
            self.gan_su_kien_click(card, command)

    def tao_the_thong_ke(self, parent, value, ton_thap, command=None):
        self.tao_the_tong_quan(
            parent,
            "Tồn thấp",
            ton_thap,
            "Sản phẩm cần kiểm tra",
            command,
            "⚠",
        )


    def tao_khu_vuc_bieu_do_admin(self, parent):
        header = tk.Frame(parent, bg=self.mau_card)
        header.pack(fill="x", padx=16, pady=(12, 4))

        self.tao_label(
            header,
            "Biểu đồ quản trị",
            14,
            self.mau_chu_dam,
            True,
            self.mau_card,
        ).pack(anchor="w")

        self.tao_label(
            header,
            "Theo dõi nhanh nhân viên, kho, hàng hóa và tồn thấp.",
            9,
            self.mau_chu_phu,
            False,
            self.mau_card,
        ).pack(anchor="w", pady=(2, 0))

        chart_box = tk.Frame(parent, bg=self.mau_card)
        chart_box.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        data = [
            {"noiDung": "Nhân viên", "soLuong": self.dem_nhan_vien()},
            {"noiDung": "Kho", "soLuong": self.dem_so_kho()},
            {"noiDung": "Hàng hóa", "soLuong": self.dem_so_hang_hoa()},
            {"noiDung": "Tồn thấp", "soLuong": self.dem_ton_thap()},
        ]

        self.ve_bieu_do_thong_ke(
            chart_box,
            data,
            "Tổng quan quản trị",
            chieu_cao=2.55,
        )


    def tao_khu_vuc_theo_doi_admin(self, parent, dung_cuon=True):
        noi_dung = tk.Frame(parent, bg=self.mau_card)
        noi_dung.pack(fill="both", expand=True)

        self.tao_label(
            noi_dung,
            "Việc cần theo dõi",
            14,
            self.mau_chu_dam,
            True,
            self.mau_card,
        ).pack(anchor="w", padx=16, pady=(12, 9))

        self.tao_o_theo_doi(
            noi_dung,
            "Tài khoản hệ thống",
            "Kiểm tra trạng thái người dùng",
            str(self.dem_nhan_vien()) + " nhân viên",
        )

        self.tao_o_theo_doi(
            noi_dung,
            "Tồn kho thấp",
            "Ưu tiên kiểm tra và nhập thêm",
            str(self.dem_ton_thap()),
            canh_bao=True,
        )

        self.tao_o_theo_doi(
            noi_dung,
            "Tổng hàng hiện có",
            "Tổng số lượng trong tồn kho",
            str(self.tinh_tong_so_luong_ton()),
        )

        self.tao_o_theo_doi(
            noi_dung,
            "Phiếu nhập",
            "Tổng phiếu đang ghi nhận",
            str(len(doc_json("phieu_nhap.json", []))),
        )

        self.tao_o_theo_doi(
            noi_dung,
            "Phiếu xuất",
            "Tổng phiếu đang ghi nhận",
            str(len(doc_json("phieu_xuat.json", []))),
        )

        low_card = tk.Frame(
            noi_dung,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        low_card.pack(fill="x", padx=12, pady=(8, 6))

        self.tao_label(
            low_card,
            "Hàng tồn kho thấp",
            11,
            self.mau_chu_dam,
            True,
            self.mau_card_nhe,
        ).pack(anchor="w", padx=10, pady=(8, 5))

        danh_sach = self.lay_canh_bao_ton_thap()[:2]

        if len(danh_sach) == 0:
            self.tao_label(
                low_card,
                "Không có sản phẩm tồn thấp",
                8,
                self.mau_chu_phu,
                False,
                self.mau_card_nhe,
            ).pack(anchor="w", padx=10, pady=(0, 8))
        else:
            for item in danh_sach:
                ten = item.get("tenSanPham", "")
                ton = str(item.get("soLuongTon", 0))
                toi_thieu = str(item.get("mucTonToiThieu", 0))
                self.tao_dong_dashboard(low_card, ten, ton + " / " + toi_thieu, True)


    def tao_o_theo_doi(self, parent, title, desc, value, canh_bao=False):
        bg = self.mau_sidebar_nhat if canh_bao else self.mau_card_nhe
        border = self.mau_canh_bao if canh_bao else self.mau_vien
        value_color = self.mau_nguy_hiem if canh_bao else self.mau_menu_chon

        item = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=border,
            highlightthickness=1,
        )
        item.pack(fill="x", padx=14, pady=(0, 8))

        left = tk.Frame(item, bg=bg)
        left.pack(side="left", fill="x", expand=True, padx=12, pady=9)

        self.tao_label(
            left,
            title,
            10,
            self.mau_chu_dam,
            True,
            bg,
        ).pack(anchor="w")

        self.tao_label(
            left,
            desc,
            9,
            self.mau_chu_phu,
            False,
            bg,
        ).pack(anchor="w", pady=(2, 0))

        self.tao_label(
            item,
            value,
            12,
            value_color,
            True,
            bg,
        ).pack(side="right", padx=12)


    def tao_dong_dashboard(self, parent, left_text, right_text, canh_bao=False):
        row = tk.Frame(parent, bg=self.mau_card_nhe)
        row.pack(fill="x", padx=10, pady=(0, 5))

        fg_right = self.mau_nguy_hiem if canh_bao else self.mau_chu_phu

        left_label = self.tao_label(
            row,
            self.rut_gon_chu(left_text, 22),
            9,
            self.mau_chu_dam,
            True,
            self.mau_card_nhe,
        )
        left_label.pack(side="left", padx=8, pady=6)

        right_label = self.tao_label(
            row,
            right_text,
            9,
            fg_right,
            True,
            self.mau_card_nhe,
        )
        right_label.pack(side="right", padx=8, pady=6)

    def hien_bang_du_lieu(
        self,
        title,
        subtitle,
        columns,
        headers,
        widths,
        data,
        fields,
        placeholder="Nhập nội dung cần tìm...",
        buttons=None,
        bottom_buttons=None,
    ):
        self.tao_tieu_de_trang(self.content, title, subtitle)

        body = self.tao_khung_noi_dung(self.content)

        if buttons is None:
            buttons = []

        def load_bang(tu_khoa=""):
            ket_qua = self.loc_du_lieu(data, tu_khoa, fields)
            self.do_du_lieu_vao_bang(bang, ket_qua, fields)

        self.tao_thanh_cong_cu(
            body,
            placeholder,
            load_bang,
            buttons=buttons,
        )

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        bang = self.tao_bang(table_area, columns, headers, widths)

        self.tao_thanh_nut_duoi(body, bottom_buttons)
        load_bang("")
        return bang

    # =========================
    # MÀN HÌNH DỮ LIỆU
    # =========================
    def hien_nhan_vien(self):
        data = doc_json("nguoi_dung.json", {})
        danh_sach = self.chuan_hoa_trang_thai(data.get("nhanVien", []))

        self.bang_nhan_vien = self.hien_bang_du_lieu(
            "Danh sách nhân viên",
            "Quản lý thông tin nhân viên, khóa/mở khóa trạng thái hoạt động",
            ("maNhanVien", "tenNhanVien", "ngaySinh", "soDienThoai", "email", "trangThai"),
            ("Mã NV", "Tên nhân viên", "Ngày sinh", "Số điện thoại", "Email", "Trạng thái"),
            (100, 240, 130, 150, 260, 120),
            danh_sach,
            ["maNhanVien", "tenNhanVien", "ngaySinh", "soDienThoai", "email", "trangThai"],
            "Nhập mã, tên, số điện thoại hoặc email...",
            [
                {"text": "Thêm", "command": self.them_nhan_vien_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_nhan_vien_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_nhan_vien_admin, "color": self.mau_xoa},
            ],
            [
                {"text": "Khóa/Mở nhân viên", "command": self.khoa_mo_nhan_vien, "color": self.mau_sidebar},
            ],
        )

    def hien_tai_khoan(self):
        data = doc_json("nguoi_dung.json", {})
        danh_sach = self.chuan_hoa_trang_thai(data.get("taiKhoan", []))

        self.bang_tai_khoan = self.hien_bang_du_lieu(
            "Danh sách tài khoản",
            "Quản lý tài khoản đăng nhập và reset mật khẩu khi cần",
            ("maTaiKhoan", "tenTaiKhoan", "maNhanVien", "trangThai"),
            ("Mã TK", "Tên tài khoản", "Mã NV", "Trạng thái"),
            (120, 220, 130, 120),
            danh_sach,
            ["maTaiKhoan", "tenTaiKhoan", "maNhanVien", "trangThai"],
            "Nhập mã tài khoản, tên tài khoản hoặc mã nhân viên...",
            [
                {"text": "Thêm", "command": self.them_tai_khoan_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_tai_khoan_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_tai_khoan_admin, "color": self.mau_xoa},
            ],
            [
                {"text": "Khóa/Mở tài khoản", "command": self.khoa_mo_tai_khoan, "color": self.mau_sidebar},
                {"text": "Reset mật khẩu", "command": self.reset_mat_khau_tai_khoan, "color": self.mau_thoat},
            ],
        )

    def hien_kho(self):
        data = doc_json("kho_hang.json", {})
        danh_sach = data.get("kho", [])

        self.bang_kho = self.hien_bang_du_lieu(
            "Danh sách kho",
            "Quản lý thông tin kho hàng",
            ("maKho", "tenKho", "diaDiem", "soDienThoai"),
            ("Mã kho", "Tên kho", "Địa điểm", "Số điện thoại"),
            (120, 260, 420, 160),
            danh_sach,
            ["maKho", "tenKho", "diaDiem", "soDienThoai"],
            "Nhập mã kho, tên kho hoặc địa điểm...",
            [
                {"text": "Thêm", "command": self.them_kho_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_kho_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_kho_admin, "color": self.mau_xoa},
            ],
        )

    def hien_nhap_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(doc_json("phieu_nhap.json", []), "nhap")
        data = self.dinh_dang_danh_sach_phieu_tien(data)

        self.bang_phieu_nhap = self.hien_bang_du_lieu(
            "Nhập kho",
            "Quản lý phiếu nhập kho",
            ("maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"),
            ("Mã phiếu", "Nhà sản xuất", "Kho", "Ngày nhập", "Tổng tiền", "Trạng thái"),
            (130, 160, 100, 140, 160, 130),
            data,
            ["maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"],
            "Nhập mã phiếu, nhà sản xuất hoặc kho...",
            [
                {"text": "Thêm", "command": lambda: self.mo_form_nhap_xuat_admin("nhap"), "color": self.mau_them},
                {"text": "Chi tiết", "command": self.xem_chi_tiet_phieu_nhap, "color": self.mau_menu},
                {"text": "Sửa", "command": self.sua_phieu_nhap_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.huy_phieu_nhap_admin, "color": self.mau_xoa},
            ],
        )

    def hien_xuat_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(doc_json("phieu_xuat.json", []), "xuat")
        data = self.dinh_dang_danh_sach_phieu_tien(data)

        self.bang_phieu_xuat = self.hien_bang_du_lieu(
            "Xuất kho",
            "Quản lý phiếu xuất kho",
            ("maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"),
            ("Mã phiếu", "Kho", "Khách hàng", "Ngày xuất", "Tổng tiền", "Trạng thái"),
            (130, 100, 160, 140, 160, 130),
            data,
            ["maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"],
            "Nhập mã phiếu, khách hàng hoặc kho...",
            [
                {"text": "Thêm", "command": lambda: self.mo_form_nhap_xuat_admin("xuat"), "color": self.mau_them},
                {"text": "Chi tiết", "command": self.xem_chi_tiet_phieu_xuat, "color": self.mau_menu},
                {"text": "Sửa", "command": self.sua_phieu_xuat_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.huy_phieu_xuat_admin, "color": self.mau_xoa},
            ],
        )

    def hien_ton_kho(self):
        self.tao_tieu_de_trang(
            self.content,
            "Tồn kho",
            "Theo dõi số lượng hàng tồn trong kho",
        )

        body = self.tao_khung_noi_dung(self.content)

        self.tao_thanh_cong_cu(
            body,
            "Nhập mã kho, mã sản phẩm, tên sản phẩm, vị trí hoặc trạng thái...",
            self.tim_kiem_ton_kho_admin,
            buttons=[],
        )

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        self.bang_ton_kho = self.tao_bang(
            table_area,
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThai", "viTriHang"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Tồn", "Tồn tối thiểu", "Trạng thái", "Vị trí hàng"),
            (90, 105, 270, 80, 115, 120, 130),
        )

        self.bang_ton_kho.tag_configure("het_hang", foreground=self.mau_nguy_hiem)
        self.bang_ton_kho.tag_configure("ton_thap", foreground=self.mau_nguy_hiem)
        self.bang_ton_kho.tag_configure("binh_thuong", foreground=self.mau_chu_dam)

        self.tao_nut_thoat(body)
        self.load_ton_kho_admin("")

    def load_ton_kho_admin(self, tu_khoa=""):
        data = self.lay_du_lieu_ton_kho_day_du()

        for item in data:
            so_luong_ton = self.chuyen_so(item.get("soLuongTon", 0))
            muc_ton_toi_thieu = self.chuyen_so(item.get("mucTonToiThieu", 0))

            if so_luong_ton <= 0:
                item["trangThaiTon"] = "Hết hàng"
            elif so_luong_ton < muc_ton_toi_thieu:
                item["trangThaiTon"] = "Tồn thấp"
            else:
                item["trangThaiTon"] = "Đủ hàng"

        ket_qua = self.loc_du_lieu(
            data,
            tu_khoa,
            ["maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThaiTon", "viTriHang"],
        )

        for dong in self.bang_ton_kho.get_children():
            self.bang_ton_kho.delete(dong)

        for item in ket_qua:
            so_luong_ton = self.chuyen_so(item.get("soLuongTon", 0))
            muc_ton_toi_thieu = self.chuyen_so(item.get("mucTonToiThieu", 0))
            trang_thai = item.get("trangThaiTon", "")

            if so_luong_ton <= 0:
                tag = "het_hang"
            elif so_luong_ton < muc_ton_toi_thieu:
                tag = "ton_thap"
            else:
                tag = "binh_thuong"
                if trang_thai == "":
                    trang_thai = "Đủ hàng"

            self.bang_ton_kho.insert(
                "",
                "end",
                values=(
                    item.get("maKho", ""),
                    item.get("maSanPham", ""),
                    item.get("tenSanPham", ""),
                    item.get("soLuongTon", ""),
                    item.get("mucTonToiThieu", ""),
                    trang_thai,
                    item.get("viTriHang", ""),
                ),
                tags=(tag,),
            )

    def tim_kiem_ton_kho_admin(self, tu_khoa):
        self.load_ton_kho_admin(tu_khoa)

    def hien_kiem_kho(self):
        data = self.lay_kiem_ke_dang_hien_thi()

        self.bang_kiem_kho = self.hien_bang_du_lieu(
            "Kiểm kho",
            "Quản lý phiếu kiểm kê kho hàng",
            ("maKiemKe", "maKho", "ngayKiemKe", "ghiChu", "trangThai"),
            ("Mã kiểm kê", "Mã kho", "Ngày kiểm kê", "Ghi chú", "Trạng thái"),
            (130, 120, 160, 420, 140),
            data,
            ["maKiemKe", "maKho", "ngayKiemKe", "ghiChu", "trangThai"],
            "Nhập mã kiểm kê, mã kho hoặc ghi chú...",
            [
                {"text": "Thêm", "command": self.them_kiem_ke_admin, "color": self.mau_them},
                {"text": "Chi tiết", "command": self.xem_chi_tiet_kiem_ke, "color": self.mau_menu},
                {"text": "Sửa", "command": self.sua_kiem_ke_admin, "color": self.mau_sua},
                {"text": "Hủy", "command": self.huy_phieu_kiem_kho, "color": self.mau_xoa},
            ],
        )

    def hien_hang_hoa(self):
        data = doc_json("hang_hoa.json", {})
        danh_sach = self.chuan_hoa_trang_thai_san_pham(data.get("sanPham", []))
        danh_sach = self.dinh_dang_danh_sach_hang_hoa_tien(danh_sach)

        self.bang_hang_hoa = self.hien_bang_du_lieu(
            "Danh mục hàng hóa",
            "Quản lý sản phẩm trong hệ thống và cập nhật trạng thái kinh doanh",
            ("maSanPham", "tenSanPham", "maLoaiHang", "donGia", "mucTonToiThieu", "trangThai"),
            ("Mã SP", "Tên sản phẩm", "Loại hàng", "Đơn giá", "Tồn tối thiểu", "Trạng thái"),
            (110, 300, 120, 140, 130, 150),
            danh_sach,
            ["maSanPham", "tenSanPham", "maLoaiHang", "donGia", "mucTonToiThieu", "trangThai"],
            "Nhập mã sản phẩm, tên sản phẩm hoặc loại hàng...",
            [
                {"text": "Thêm", "command": self.them_hang_hoa_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_hang_hoa_admin, "color": self.mau_sua},
                {"text": "Đổi trạng thái", "command": self.ngung_kinh_doanh_hang_hoa_admin, "color": self.mau_sidebar},
            ],
        )

    def hien_loai_hang(self):
        data = doc_json("hang_hoa.json", {})
        danh_sach = data.get("loaiHang", [])

        self.bang_loai_hang = self.hien_bang_du_lieu(
            "Loại hàng",
            "Quản lý nhóm loại hàng hóa",
            ("maLoaiHang", "tenLoaiHang", "ghiChu"),
            ("Mã loại", "Tên loại hàng", "Ghi chú"),
            (130, 300, 420),
            danh_sach,
            ["maLoaiHang", "tenLoaiHang", "ghiChu"],
            "Nhập mã loại, tên loại hoặc ghi chú...",
            [
                {"text": "Thêm", "command": self.them_loai_hang_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_loai_hang_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_loai_hang_admin, "color": self.mau_xoa},
            ],
        )

    def hien_nha_san_xuat(self):
        data = doc_json("doi_tac.json", {})
        danh_sach = data.get("nhaSanXuat", [])

        self.bang_nha_san_xuat = self.hien_bang_du_lieu(
            "Nhà sản xuất",
            "Quản lý thông tin nhà sản xuất",
            ("maNhaSanXuat", "tenNhaSanXuat", "soDienThoai", "email", "diaChi"),
            ("Mã NSX", "Tên nhà sản xuất", "Số điện thoại", "Email", "Địa chỉ"),
            (120, 250, 150, 220, 280),
            danh_sach,
            ["maNhaSanXuat", "tenNhaSanXuat", "soDienThoai", "email", "diaChi"],
            "Nhập mã, tên, số điện thoại hoặc email...",
            [
                {"text": "Thêm", "command": self.them_nha_san_xuat_admin, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_nha_san_xuat_admin, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_nha_san_xuat_admin, "color": self.mau_xoa},
            ],
        )

    # =========================
    # THỐNG KÊ
    # =========================
    def hien_thong_ke_tong_quan(self):
        self.tao_tieu_de_trang(
            self.content,
            "Thống kê tổng quan",
            "Biểu đồ chính bên trái, bảng số liệu rút gọn bên phải để quản trị đối chiếu",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        tong_nhap = self.tinh_tong_tien("phieu_nhap.json")
        tong_xuat = self.tinh_tong_tien("phieu_xuat.json")
        gia_tri_ton = self.tinh_gia_tri_ton_kho()

        card_row = tk.Frame(body, bg=self.mau_card)
        card_row.pack(fill="x", pady=(0, 10))

        self.tao_the_tong_quan(card_row, "Tổng nhập", self.dinh_dang_so_ngan(tong_nhap), "Giá trị phiếu nhập")
        self.tao_the_tong_quan(card_row, "Tổng xuất", self.dinh_dang_so_ngan(tong_xuat), "Giá trị phiếu xuất")
        self.tao_the_tong_quan(card_row, "Giá trị tồn", self.dinh_dang_so_ngan(gia_tri_ton), "Hàng còn trong kho")
        self.tao_the_tong_quan(card_row, "Tồn thấp", self.dem_ton_thap(), "Sản phẩm cần kiểm tra")

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        left = self.tao_card(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = self.tao_card(main)
        right.grid(row=0, column=1, sticky="nsew")

        self.tao_label(left, "Biểu đồ giá trị", 16, self.mau_chu_dam, True).pack(
            anchor="w", padx=18, pady=(16, 8)
        )

        self.ve_bieu_do_thong_ke(
            left,
            [
                {"noiDung": "Nhập", "soLuong": tong_nhap},
                {"noiDung": "Xuất", "soLuong": tong_xuat},
                {"noiDung": "Tồn", "soLuong": gia_tri_ton},
            ],
            "Nhập / Xuất / Tồn",
            chieu_cao=2.55,
        )

        self.tao_label(right, "Bảng số liệu", 16, self.mau_chu_dam, True).pack(
            anchor="w", padx=18, pady=(16, 8)
        )

        data = [
            {"noiDung": "Phiếu nhập", "soLuong": len(doc_json("phieu_nhap.json", [])), "giaTri": tong_nhap, "ghiChu": "Tổng giá trị nhập kho"},
            {"noiDung": "Phiếu xuất", "soLuong": len(doc_json("phieu_xuat.json", [])), "giaTri": tong_xuat, "ghiChu": "Tổng giá trị xuất kho"},
            {"noiDung": "Kho hàng", "soLuong": self.dem_so_kho(), "giaTri": "-", "ghiChu": "Số kho đang quản lý"},
            {"noiDung": "Sản phẩm", "soLuong": self.dem_so_hang_hoa(), "giaTri": "-", "ghiChu": "Mặt hàng đang quản lý"},
            {"noiDung": "Tồn kho", "soLuong": self.tinh_tong_so_luong_ton(), "giaTri": gia_tri_ton, "ghiChu": "Tổng số lượng và giá trị tồn"},
            {"noiDung": "Tồn thấp", "soLuong": self.dem_ton_thap(), "giaTri": "-", "ghiChu": "Dưới mức tối thiểu"},
        ]

        bang = self.tao_bang(
            right,
            ("noiDung", "soLuong", "giaTri", "ghiChu"),
            ("Nội dung", "Số lượng", "Giá trị", "Ghi chú"),
            (120, 80, 120, 190),
        )

        self.do_du_lieu_vao_bang(
            bang,
            self.dinh_dang_du_lieu_tong_quan(data),
            ["noiDung", "soLuong", "giaTri", "ghiChu"],
        )

    def hien_thong_ke_nhap_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(
            doc_json("phieu_nhap.json", []),
            "nhap",
        )

        self.hien_dashboard_nhap_xuat(
            title="Thống kê nhập kho",
            subtitle="Theo dõi tổng nhập theo tháng, top phiếu nhập và danh sách đối chiếu",
            data=data,
            ma_field="maPhieuNhap",
            kho_field="maKho",
            ngay_field="ngayNhap",
            chart_title="Tổng tiền nhập theo tháng",
            top_title="Top phiếu nhập giá trị cao",
            table_title="Danh sách phiếu nhập",
            tong_label="Tổng nhập",
            so_phieu_label="Phiếu nhập",
        )

    def hien_thong_ke_xuat_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(
            doc_json("phieu_xuat.json", []),
            "xuat",
        )

        self.hien_dashboard_nhap_xuat(
            title="Thống kê xuất kho",
            subtitle="Theo dõi tổng xuất theo tháng, top phiếu xuất và danh sách đối chiếu",
            data=data,
            ma_field="maPhieuXuat",
            kho_field="maKho",
            ngay_field="ngayXuat",
            chart_title="Tổng tiền xuất theo tháng",
            top_title="Top phiếu xuất giá trị cao",
            table_title="Danh sách phiếu xuất",
            tong_label="Tổng xuất",
            so_phieu_label="Phiếu xuất",
        )

    def hien_dashboard_nhap_xuat(
        self,
        title,
        subtitle,
        data,
        ma_field,
        kho_field,
        ngay_field,
        chart_title,
        top_title,
        table_title,
        tong_label,
        so_phieu_label,
    ):
        self.tao_tieu_de_trang(self.content, title, subtitle)

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        tong_tien = self.tinh_tong_tien_tu_danh_sach(data)
        so_phieu = len(data)
        trung_binh = tong_tien / so_phieu if so_phieu > 0 else 0
        phieu_moi = self.lay_phieu_moi_nhat(data, ngay_field)

        card_row = tk.Frame(body, bg=self.mau_card)
        card_row.pack(fill="x", pady=(0, 12))

        self.tao_the_tong_quan(
            card_row,
            so_phieu_label,
            so_phieu,
            "Tổng số phiếu",
        )

        self.tao_the_tong_quan(
            card_row,
            tong_label,
            self.dinh_dang_so_ngan(tong_tien),
            "Tổng giá trị",
        )

        self.tao_the_tong_quan(
            card_row,
            "Trung bình",
            self.dinh_dang_so_ngan(trung_binh),
            "Giá trị / phiếu",
        )

        self.tao_the_tong_quan(
            card_row,
            "Mới nhất",
            phieu_moi,
            "Phiếu gần đây",
        )

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=0, minsize=275)
        main.grid_rowconfigure(1, weight=1)

        chart_card = self.tao_card(main)
        chart_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        top_card = self.tao_card(main)
        top_card.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        top_card.config(height=275)
        top_card.grid_propagate(False)

        table_card = self.tao_card(main)
        table_card.grid(row=1, column=1, sticky="nsew")

        self.tao_label(
            chart_card,
            "Biểu đồ theo tháng",
            15,
            self.mau_chu_dam,
            True,
        ).pack(anchor="w", padx=16, pady=(14, 2))

        self.tao_label(
            chart_card,
            "Biểu đồ giúp xem xu hướng tăng giảm theo từng tháng.",
            9,
            self.mau_chu_phu,
        ).pack(anchor="w", padx=16, pady=(0, 8))

        self.ve_bieu_do_thong_ke(
            chart_card,
            self.lay_thong_ke_theo_thang(data, ngay_field),
            chart_title,
            chieu_cao=3.0,
        )

        self.tao_label(
            top_card,
            top_title,
            15,
            self.mau_chu_dam,
            True,
        ).pack(anchor="w", padx=16, pady=(12, 6))

        top_data = self.lay_top_5_theo_tien(data, ma_field)

        if len(top_data) == 0:
            self.tao_label(
                top_card,
                "Chưa có dữ liệu",
                10,
                self.mau_chu_phu,
            ).pack(anchor="w", padx=16, pady=10)
        else:
            for item in top_data:
                self.tao_dong_top_phieu(
                    top_card,
                    item.get("noiDung", ""),
                    self.dinh_dang_so_ngan(item.get("soLuong", 0)),
                )

        self.tao_label(
            table_card,
            table_title,
            15,
            self.mau_chu_dam,
            True,
        ).pack(anchor="w", padx=16, pady=(14, 8))

        bang = self.tao_bang(
            table_card,
            (ma_field, kho_field, ngay_field, "tongTien", "trangThai"),
            ("Mã phiếu", "Kho", "Ngày", "Tổng tiền", "Trạng thái"),
            (110, 90, 115, 130, 120),
        )

        self.do_du_lieu_vao_bang(
            bang,
            self.dinh_dang_danh_sach_phieu(data),
            [ma_field, kho_field, ngay_field, "tongTien", "trangThai"],
        )

    def tao_dong_top_phieu(self, parent, ma_phieu, gia_tri):
        row = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        row.pack(fill="x", padx=14, pady=(0, 5))

        self.tao_label(
            row,
            ma_phieu,
            10,
            self.mau_chu_dam,
            True,
            self.mau_card_nhe,
        ).pack(side="left", padx=12, pady=6)

        self.tao_label(
            row,
            gia_tri,
            10,
            self.mau_menu,
            True,
            self.mau_card_nhe,
        ).pack(side="right", padx=12, pady=6)

    def hien_doanh_thu_theo_kho(self):
        data = self.lay_doanh_thu_theo_kho()

        self.tao_tieu_de_trang(
            self.content,
            "Doanh thu theo kho",
            "Thống kê giá trị xuất hàng theo từng kho",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        self.hien_thong_ke_bang_bieu_do_don(
            body,
            self.dinh_dang_doanh_thu_kho(data),
            ("maKho", "tenKho", "soPhieu", "tongDoanhThu"),
            ("Mã kho", "Tên kho", "Số phiếu xuất", "Doanh thu"),
            (110, 240, 130, 180),
            ["maKho", "tenKho", "soPhieu", "tongDoanhThu"],
            [
                {"noiDung": item["maKho"], "soLuong": item["tongDoanhThu"]}
                for item in data
            ],
            "Doanh thu theo kho",
        )

    def hien_canh_bao_ton_thap(self):
        data = self.lay_canh_bao_ton_thap()

        self.tao_tieu_de_trang(
            self.content,
            "Cảnh báo tồn thấp",
            "Danh sách sản phẩm có số lượng tồn nhỏ hơn mức tồn tối thiểu",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        top = tk.Frame(body, bg=self.mau_card)
        top.pack(fill="x", pady=(0, 12))

        tong_thieu = 0
        for item in data:
            tong_thieu += self.chuyen_so(item.get("canNhapThem", 0))

        self.tao_the_tong_quan(
            top,
            "Sản phẩm cảnh báo",
            len(data),
            "Cần xem xét nhập thêm",
        )

        self.tao_the_tong_quan(
            top,
            "Tổng thiếu",
            int(tong_thieu),
            "So với mức tối thiểu",
        )

        self.tao_the_tong_quan(
            top,
            "Trạng thái",
            "Cần xử lý",
            "Theo mức tồn tối thiểu",
        )

        bang = self.tao_bang(
            body,
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "canNhapThem"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Tồn hiện tại", "Tồn tối thiểu", "Cần nhập thêm"),
            (100, 120, 320, 120, 130, 130),
        )

        self.do_du_lieu_vao_bang(
            bang,
            data,
            ["maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "canNhapThem"],
        )

    def hien_thong_ke_bang_bieu_do_don(
        self,
        parent,
        table_data,
        columns,
        headers,
        widths,
        fields,
        chart_data,
        chart_title,
    ):
        main = tk.Frame(parent, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        left = self.tao_card(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = self.tao_card(main)
        right.pack(side="right", fill="both", expand=True)

        bang = self.tao_bang(left, columns, headers, widths)
        self.do_du_lieu_vao_bang(bang, table_data, fields)

        self.ve_bieu_do_thong_ke(right, chart_data, chart_title)

    def hien_thong_ke_bang_hai_bieu_do(
        self,
        parent,
        table_data,
        columns,
        headers,
        widths,
        fields,
        chart_data_1,
        chart_title_1,
        chart_data_2,
        chart_title_2,
    ):
        main = tk.Frame(parent, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        left = self.tao_card(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = self.tao_card(main)
        right.pack(side="right", fill="both", expand=True)

        bang = self.tao_bang(left, columns, headers, widths)
        self.do_du_lieu_vao_bang(bang, table_data, fields)

        self.ve_bieu_do_thong_ke(right, chart_data_1, chart_title_1, chieu_cao=2.35)
        self.ve_bieu_do_thong_ke(right, chart_data_2, chart_title_2, chieu_cao=2.35)




    def ve_bieu_do_thong_ke(self, parent, data, title, chieu_cao=3.0):
        box = tk.Frame(parent, bg=self.mau_card)
        box.pack(fill="both", expand=True, padx=10, pady=(4, 8))

        self.tao_label(
            box,
            title,
            12,
            self.mau_chu_dam,
            True,
            self.mau_card,
        ).pack(anchor="w", padx=6, pady=(0, 4))

        if len(data) == 0:
            self.tao_label(
                box,
                "Không có dữ liệu để hiển thị biểu đồ",
                10,
                self.mau_chu_phu,
                False,
                self.mau_card,
            ).pack(padx=18, pady=20)
            return

        labels = []
        values = []

        for item in data:
            labels.append(self.rut_gon_chu(item["noiDung"], 12))
            values.append(self.chuyen_so(item["soLuong"]))

        fig = Figure(figsize=(5.0, chieu_cao), dpi=100, facecolor=self.mau_card)
        ax = fig.add_subplot(111)

        ax.bar(labels, values, width=0.42, color=self.mau_menu)
        ax.tick_params(axis="x", labelrotation=20, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.18)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for index, value in enumerate(values):
            ax.text(
                index,
                value,
                self.dinh_dang_so_ngan(value),
                ha="center",
                va="bottom",
                fontsize=7,
                color=self.mau_chu_dam,
            )

        fig.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.24)

        canvas = FigureCanvasTkAgg(fig, box)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def dat_placeholder_entry(self, entry, placeholder):
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg=self.mau_chu_phu)

        def xoa_placeholder(event=None):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.mau_chu_dam)

        def khoi_phuc_placeholder(event=None):
            if entry.get().strip() == "":
                entry.delete(0, tk.END)
                entry.insert(0, placeholder)
                entry.config(fg=self.mau_chu_phu)

        entry.bind("<FocusIn>", xoa_placeholder)
        entry.bind("<FocusOut>", khoi_phuc_placeholder)

    def lay_noi_dung_entry(self, entry, placeholder):
        noi_dung = entry.get().strip()

        if noi_dung == placeholder:
            return ""

        return noi_dung


    def dinh_dang_tien_admin(self, value):
        try:
            value = str(value).strip()

            if value == "" or value == "-":
                return value

            value = value.replace(".", "").replace(",", "")
            so_tien = int(float(value))
            return "{:,}".format(so_tien).replace(",", ".")
        except Exception:
            return str(value)

    def dinh_dang_so_ngan(self, value):
        return self.dinh_dang_tien_admin(value)

    def dinh_dang_danh_sach_tien_hien_thi(self, danh_sach, truong_tien, truong_hien_thi=None):
        if truong_hien_thi is None:
            truong_hien_thi = truong_tien

        ket_qua = []

        for item in danh_sach:
            dong = dict(item)
            dong[truong_hien_thi] = self.dinh_dang_tien_admin(dong.get(truong_tien, 0))
            ket_qua.append(dong)

        return ket_qua

    def dinh_dang_danh_sach_phieu_tien(self, danh_sach):
        return self.dinh_dang_danh_sach_tien_hien_thi(danh_sach, "tongTien", "tongTien")

    def dinh_dang_danh_sach_hang_hoa_tien(self, danh_sach):
        return self.dinh_dang_danh_sach_tien_hien_thi(danh_sach, "donGia", "donGia")

    # =========================
    # NHẬT KÝ
    # =========================
    def hien_nhat_ky_dang_nhap(self):
        self.tao_tieu_de_trang(
            self.content,
            "Nhật ký đăng nhập",
            "Theo dõi lịch sử đăng nhập và đăng xuất hệ thống",
        )

        body = self.tao_khung_noi_dung(self.content)
        data = self.lay_nhat_ky_dang_nhap_admin()

        self.tong_ban_ghi_nhat_ky_dang_nhap_label = self.tao_label(
            body,
            "Tổng số bản ghi: " + str(len(data)),
            11,
            self.mau_chu_phu,
            False,
            self.mau_card,
        )
        self.tong_ban_ghi_nhat_ky_dang_nhap_label.pack(anchor="w", padx=4, pady=(0, 12))

        filter_bar = tk.Frame(body, bg=self.mau_card)
        filter_bar.pack(fill="x", pady=(0, 12))

        self.cbo_loai_nhat_ky_dang_nhap = ttk.Combobox(
            filter_bar,
            values=["Tất cả", "Đăng nhập", "Đăng xuất"],
            state="readonly",
            width=22,
            font=("Segoe UI", 10),
        )
        self.cbo_loai_nhat_ky_dang_nhap.set("Tất cả")
        self.cbo_loai_nhat_ky_dang_nhap.pack(side="left", padx=(0, 10), ipady=5)

        self.entry_tu_ngay_dang_nhap = tk.Entry(
            filter_bar,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            width=18,
        )
        self.entry_tu_ngay_dang_nhap.pack(side="left", padx=(0, 2), ipady=7)
        self.dat_placeholder_entry(self.entry_tu_ngay_dang_nhap, "Từ ngày yyyy-mm-dd")
        self.gan_rang_buoc_ngay(self.entry_tu_ngay_dang_nhap, "Từ ngày", "Từ ngày yyyy-mm-dd")

        tk.Button(
            filter_bar,
            text="📅",
            command=lambda: self.mo_lich_chon_ngay(self.entry_tu_ngay_dang_nhap),
            bg=self.mau_sua,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        self.entry_den_ngay_dang_nhap = tk.Entry(
            filter_bar,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            width=18,
        )
        self.entry_den_ngay_dang_nhap.pack(side="left", padx=(0, 2), ipady=7)
        self.dat_placeholder_entry(self.entry_den_ngay_dang_nhap, "Đến ngày yyyy-mm-dd")
        self.gan_rang_buoc_ngay(self.entry_den_ngay_dang_nhap, "Đến ngày", "Đến ngày yyyy-mm-dd")

        tk.Button(
            filter_bar,
            text="📅",
            command=lambda: self.mo_lich_chon_ngay(self.entry_den_ngay_dang_nhap),
            bg=self.mau_sua,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        self.tao_nut(
            filter_bar,
            "Lọc",
            self.loc_nhat_ky_dang_nhap_admin,
            self.mau_sua,
        ).pack(side="left", padx=(0, 10))

        self.tao_nut(
            filter_bar,
            "Làm mới",
            self.lam_moi_nhat_ky_dang_nhap_admin,
            self.mau_thoat,
        ).pack(side="left")

        search_box = tk.Frame(
            filter_bar,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        search_box.pack(side="right", ipady=1)

        tk.Label(
            search_box,
            text="🔎",
            bg=self.mau_card_nhe,
            fg=self.mau_menu,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(10, 0))

        self.entry_tim_nhat_ky_dang_nhap = tk.Entry(
            search_box,
            font=("Segoe UI", 9),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            width=36,
        )
        self.entry_tim_nhat_ky_dang_nhap.pack(side="left", padx=(8, 8), ipady=6)
        self.dat_placeholder_entry(self.entry_tim_nhat_ky_dang_nhap, "Tìm kiếm nhật ký...")

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        self.bang_nhat_ky_dang_nhap = self.tao_bang(
            table_area,
            ("maNhatKy", "maTaiKhoan", "hanhDong", "thoiGian", "trangThai"),
            ("Mã", "Tài khoản", "Hành động", "Thời gian", "Trạng thái"),
            (90, 130, 250, 220, 150),
        )

        self.tao_nut_thoat(body)

        self.entry_tim_nhat_ky_dang_nhap.bind("<Return>", lambda event: self.loc_nhat_ky_dang_nhap_admin())
        self.cbo_loai_nhat_ky_dang_nhap.bind("<<ComboboxSelected>>", lambda event: self.loc_nhat_ky_dang_nhap_admin())

        self.loc_nhat_ky_dang_nhap_admin()

    def lay_nhat_ky_dang_nhap_admin(self):
        data = self.chuan_hoa_trang_thai(doc_json("nhat_ky.json", []))
        ket_qua = []

        for item in data:
            hanh_dong = str(item.get("hanhDong", item.get("hanh_dong", ""))).lower()

            if "đăng nhập" in hanh_dong or "đăng xuất" in hanh_dong:
                ket_qua.append(item)

        return ket_qua

    def loc_nhat_ky_dang_nhap_admin(self):
        try:
            loai = self.cbo_loai_nhat_ky_dang_nhap.get()
            tu_ngay = self.lay_noi_dung_entry(self.entry_tu_ngay_dang_nhap, "Từ ngày yyyy-mm-dd")
            den_ngay = self.lay_noi_dung_entry(self.entry_den_ngay_dang_nhap, "Đến ngày yyyy-mm-dd")
            tu_khoa = self.lay_noi_dung_entry(self.entry_tim_nhat_ky_dang_nhap, "Tìm kiếm nhật ký...")

            tu_ngay, den_ngay = self.kiem_tra_khoang_ngay_loc(tu_ngay, den_ngay)

            data = self.lay_nhat_ky_dang_nhap_admin()
            ket_qua = []

            for item in data:
                if self.nhat_ky_dang_nhap_dung_bo_loc(item, loai, tu_ngay, den_ngay, tu_khoa):
                    ket_qua.append(item)

            self.tong_ban_ghi_nhat_ky_dang_nhap_label.config(
                text="Tổng số bản ghi: " + str(len(ket_qua))
            )

            self.do_du_lieu_vao_bang(
                self.bang_nhat_ky_dang_nhap,
                ket_qua,
                ["maNhatKy", "maTaiKhoan", "hanhDong", "thoiGian", "trangThai"],
            )

        except ValueError as loi:
            messagebox.showwarning("Dữ liệu không hợp lệ", str(loi))

    def nhat_ky_dang_nhap_dung_bo_loc(self, item, loai, tu_ngay, den_ngay, tu_khoa):
        hanh_dong = str(item.get("hanhDong", "")).lower()
        thoi_gian = str(item.get("thoiGian", ""))
        ngay = self.chuan_hoa_ngay_loc(thoi_gian)

        if loai != "Tất cả":
            loai_lower = loai.lower()

            if loai_lower == "đăng nhập" and "đăng nhập" not in hanh_dong:
                return False

            if loai_lower == "đăng xuất" and "đăng xuất" not in hanh_dong:
                return False

        if tu_ngay != "" and ngay != "" and ngay < tu_ngay:
            return False

        if den_ngay != "" and ngay != "" and ngay > den_ngay:
            return False

        if tu_khoa != "":
            noi_dung = " ".join([
                str(item.get("maNhatKy", "")),
                str(item.get("maTaiKhoan", "")),
                str(item.get("hanhDong", "")),
                str(item.get("thoiGian", "")),
                str(item.get("trangThai", "")),
            ]).lower()

            if tu_khoa.lower() not in noi_dung:
                return False

        return True

    def lam_moi_nhat_ky_dang_nhap_admin(self):
        self.cbo_loai_nhat_ky_dang_nhap.set("Tất cả")
        self.dat_placeholder_entry(self.entry_tu_ngay_dang_nhap, "Từ ngày yyyy-mm-dd")
        self.dat_placeholder_entry(self.entry_den_ngay_dang_nhap, "Đến ngày yyyy-mm-dd")
        self.dat_placeholder_entry(self.entry_tim_nhat_ky_dang_nhap, "Tìm kiếm nhật ký...")
        self.loc_nhat_ky_dang_nhap_admin()

    def hien_nhat_ky_thao_tac(self):
        tat_ca = self.chuan_hoa_trang_thai(doc_json("nhat_ky.json", []))
        data = []

        for item in tat_ca:
            hanh_dong = str(item.get("hanhDong", "")).lower()

            if "đăng nhập" in hanh_dong or "đăng xuất" in hanh_dong:
                continue

            data.append(item)

        self.tao_tieu_de_trang(
            self.content,
            "Nhật ký thao tác",
            "Theo dõi thao tác thêm, sửa, xóa, khóa/mở khóa và reset mật khẩu",
        )

        body = self.tao_khung_noi_dung(self.content)

        header = tk.Frame(body, bg=self.mau_card)
        header.pack(fill="x", pady=(0, 12))

        tong_label = self.tao_label(
            header,
            "Tổng số bản ghi: " + str(len(data)),
            11,
            self.mau_chu_phu,
            False,
            self.mau_card,
        )
        tong_label.pack(side="left", padx=(4, 0))

        filter_bar = tk.Frame(body, bg=self.mau_card)
        filter_bar.pack(fill="x", pady=(0, 12))

        cbo_loai = ttk.Combobox(
            filter_bar,
            values=["Tất cả", "Thêm", "Sửa", "Xóa", "Khóa/Mở khóa", "Reset mật khẩu"],
            state="readonly",
            width=22,
            font=("Segoe UI", 10),
        )
        cbo_loai.set("Tất cả")
        cbo_loai.pack(side="left", padx=(0, 10), ipady=5)

        entry_tu_ngay = tk.Entry(
            filter_bar,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            width=18,
        )
        entry_tu_ngay.pack(side="left", padx=(0, 2), ipady=7)
        self.dat_placeholder_entry(entry_tu_ngay, "Từ ngày yyyy-mm-dd")
        self.gan_rang_buoc_ngay(entry_tu_ngay, "Từ ngày", "Từ ngày yyyy-mm-dd")

        tk.Button(
            filter_bar,
            text="📅",
            command=lambda: self.mo_lich_chon_ngay(entry_tu_ngay),
            bg=self.mau_sua,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        entry_den_ngay = tk.Entry(
            filter_bar,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            width=18,
        )
        entry_den_ngay.pack(side="left", padx=(0, 2), ipady=7)
        self.dat_placeholder_entry(entry_den_ngay, "Đến ngày yyyy-mm-dd")
        self.gan_rang_buoc_ngay(entry_den_ngay, "Đến ngày", "Đến ngày yyyy-mm-dd")

        tk.Button(
            filter_bar,
            text="📅",
            command=lambda: self.mo_lich_chon_ngay(entry_den_ngay),
            bg=self.mau_sua,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        search_box = tk.Frame(
            filter_bar,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        search_box.pack(side="right", ipady=1)

        tk.Label(
            search_box,
            text="🔎",
            bg=self.mau_card_nhe,
            fg=self.mau_menu,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(10, 0))

        entry_tim = tk.Entry(
            search_box,
            font=("Segoe UI", 9),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            width=36,
        )
        entry_tim.pack(side="left", padx=(8, 8), ipady=6)
        self.dat_placeholder_entry(entry_tim, "Tìm kiếm nhật ký...")

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        bang = self.tao_bang(
            table_area,
            ("maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai"),
            ("Mã", "Tài khoản", "Hành động", "Đối tượng", "Thời gian", "Trạng thái"),
            (90, 130, 220, 180, 220, 150),
        )

        
        def loc_nhat_ky(event=None):
            loai = cbo_loai.get()
            tu_ngay = self.lay_noi_dung_entry(entry_tu_ngay, "Từ ngày yyyy-mm-dd")
            den_ngay = self.lay_noi_dung_entry(entry_den_ngay, "Đến ngày yyyy-mm-dd")
            tu_khoa = self.lay_noi_dung_entry(entry_tim, "Tìm kiếm nhật ký...")

            try:
                tu_ngay, den_ngay = self.kiem_tra_khoang_ngay_loc(tu_ngay, den_ngay)
                ket_qua = self.loc_nhat_ky_thao_tac(data, loai, tu_ngay, den_ngay, tu_khoa)
            except ValueError as loi:
                messagebox.showwarning("Dữ liệu không hợp lệ", str(loi))
                return

            tong_label.config(text="Tổng số bản ghi: " + str(len(ket_qua)))

            self.do_du_lieu_vao_bang(
                bang,
                ket_qua,
                ["maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai"],
            )

        self.tao_nut(
            filter_bar,
            "Lọc",
            loc_nhat_ky,
            self.mau_sua,
        ).pack(side="left", padx=(0, 10))

        self.tao_nut(
            filter_bar,
            "Làm mới",
            self.hien_nhat_ky_thao_tac,
            self.mau_thoat,
        ).pack(side="left")

        entry_tim.bind("<Return>", loc_nhat_ky)
        cbo_loai.bind("<<ComboboxSelected>>", loc_nhat_ky)

        self.tao_nut_thoat(body)

        loc_nhat_ky()

    # =========================
    # HÀM PHỤ GIAO DIỆN
    # =========================
    def tao_thanh_nut_duoi(self, parent, buttons=None, pady=(14, 0)):
        bottom = tk.Frame(parent, bg=self.mau_card)
        bottom.pack(side="bottom", fill="x", pady=pady)

        self.tao_nut(
            bottom,
            "Thoát",
            self.hien_trang_chu,
            self.mau_thoat,
        ).pack(side="right")

        if buttons is None:
            return

        for button in reversed(buttons):
            self.tao_nut(
                bottom,
                button["text"],
                button["command"],
                button["color"],
            ).pack(side="right", padx=(0, 8))

    def tao_nut_thoat(self, parent, pady=(14, 0)):
        self.tao_thanh_nut_duoi(parent, None, pady)

    # =========================
    # CRUD DANH MỤC ADMIN
    # =========================
    def tao_form_danh_muc_admin(self, title, fields, values=None):
        values = values or {}
        form = self.tao_cua_so_form(title, 540, 560)
        entries = {}

        for field in fields:
            key = field.get("key", "")
            label = field.get("label", key)
            field_type = field.get("type", "entry")

            if field_type == "combo":
                widget = self.tao_combobox_form(form["body"], label, field.get("values", []))
                self.chon_combobox_theo_ma(widget, values.get(key, ""))
            else:
                widget = self.tao_entry_form(form["body"], label)
                widget.insert(0, str(values.get(key, field.get("default", ""))))

                if field.get("validate", "") == "date":
                    self.gan_rang_buoc_ngay(widget, label)

            entries[key] = widget

        return form, entries

    def lay_du_lieu_form_danh_muc(self, fields, entries):
        data = {}

        for field in fields:
            key = field.get("key", "")
            field_type = field.get("type", "entry")

            if field_type == "combo":
                value = self.lay_ma_tu_combobox(entries[key].get())
            else:
                value = entries[key].get().strip()

            if field.get("required", True) and value == "":
                raise ValueError("Vui lòng nhập " + field.get("label", key).lower() + ".")

            validate = field.get("validate", "")

            if validate == "text":
                value = self.kiem_tra_chi_chu(value, field.get("label", key), field.get("required", True))
            elif validate == "phone":
                value = self.kiem_tra_so_dien_thoai(value, field.get("label", key), field.get("required", True))
            elif validate == "email":
                value = self.kiem_tra_email_gmail(value, field.get("label", key), field.get("required", True))
            elif validate == "date":
                value = self.kiem_tra_ngay(value, field.get("label", key), field.get("required", True))
            elif validate == "number" or field.get("number", False):
                value = self.kiem_tra_chi_so(value, field.get("label", key), field.get("required", True), field.get("min", None))

            data[key] = value

        return data

    def mo_form_danh_muc_admin(self, title, fields, on_save, values=None):
        form, entries = self.tao_form_danh_muc_admin(title, fields, values)

        def luu():
            try:
                data = self.lay_du_lieu_form_danh_muc(fields, entries)
                on_save(data)
                form["window"].destroy()
                messagebox.showinfo("Thành công", "Đã lưu dữ liệu.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, self.mau_them).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, self.mau_thoat).pack(side="right")

    def lay_item_dang_chon(self, bang, ten_file, danh_muc, truong_ma):
        if bang is None:
            messagebox.showwarning("Chưa có dữ liệu", "Vui lòng mở lại danh sách rồi chọn một dòng.")
            return None

        ma = self.lay_ma_dong_dang_chon(bang)

        if ma == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một dòng.")
            return None

        for item in doc_json(ten_file, {}).get(danh_muc, []):
            if item.get(truong_ma, "") == ma:
                return item

        messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu đã chọn.")
        return None

    def lay_gia_tri_trang_thai_nguoi_dung(self, value):
        trang_thai = str(value).strip().lower()

        if trang_thai in ["true", "1", "hoạt động", "hoat dong", "đang hoạt động", "dang hoat dong", "active"]:
            return "Hoạt động"

        if trang_thai in ["false", "0", "đã khóa", "da khoa", "khóa", "khoa", "inactive"]:
            return "Đã khóa"

        return str(value).strip() or "Hoạt động"

    def lay_nhan_vien_chua_co_tai_khoan(self, ma_tai_khoan_bo_qua=""):
        nguoi_dung = doc_json("nguoi_dung.json", {})
        danh_sach_ma_nhan_vien_da_co_tai_khoan = []

        for tai_khoan in nguoi_dung.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") != ma_tai_khoan_bo_qua:
                danh_sach_ma_nhan_vien_da_co_tai_khoan.append(tai_khoan.get("maNhanVien", ""))

        ket_qua = []

        for nhan_vien in nguoi_dung.get("nhanVien", []):
            ma_nhan_vien = nhan_vien.get("maNhanVien", "")

            if ma_nhan_vien not in danh_sach_ma_nhan_vien_da_co_tai_khoan:
                ket_qua.append(nhan_vien)

        return ket_qua

    def lay_vai_tro_duoc_cap(self):
        nguoi_dung = doc_json("nguoi_dung.json", {})
        ket_qua = []

        for vai_tro in nguoi_dung.get("vaiTro", []):
            ten_vai_tro = str(vai_tro.get("tenVaiTro", "")).strip().lower()

            if ten_vai_tro in ["nhân viên kho", "nhan vien kho", "nhanvienkho", "kế toán", "ke toan", "ketoan"]:
                ket_qua.append(vai_tro)

        return ket_qua

    def them_nhan_vien_admin(self):
        fields = [
            {"key": "tenNhanVien", "label": "Tên nhân viên", "validate": "text"},
            {"key": "ngaySinh", "label": "Ngày sinh", "required": False, "validate": "date"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
            {"key": "email", "label": "Email", "required": False, "validate": "email"},
            {"key": "trangThai", "label": "Trạng thái", "type": "combo", "values": ["Hoạt động", "Đã khóa"]},
        ]

        def save(data):
            self.nghiep_vu_admin.tao_nhan_vien(data)
            self.hien_nhan_vien()

        self.mo_form_danh_muc_admin("Thêm nhân viên", fields, save)

    def sua_nhan_vien_admin(self):
        item = self.lay_item_dang_chon(self.bang_nhan_vien, "nguoi_dung.json", "nhanVien", "maNhanVien")
        if item is None:
            return
        values = dict(item)
        values["trangThai"] = self.lay_gia_tri_trang_thai_nguoi_dung(item.get("trangThai", ""))

        fields = [
            {"key": "tenNhanVien", "label": "Tên nhân viên", "validate": "text"},
            {"key": "ngaySinh", "label": "Ngày sinh", "required": False, "validate": "date"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
            {"key": "email", "label": "Email", "required": False, "validate": "email"},
            {"key": "trangThai", "label": "Trạng thái", "type": "combo", "values": ["Hoạt động", "Đã khóa"]},
        ]

        def save(data):
            self.nghiep_vu_admin.cap_nhat_nhan_vien(item.get("maNhanVien", ""), data)
            self.hien_nhan_vien()

        self.mo_form_danh_muc_admin("Sửa nhân viên", fields, save, values)

    def xoa_nhan_vien_admin(self):
        item = self.lay_item_dang_chon(self.bang_nhan_vien, "nguoi_dung.json", "nhanVien", "maNhanVien")
        if item is None:
            return

        ma = item.get("maNhanVien", "")
        if not messagebox.askyesno("Xác nhận", "Xóa nhân viên " + ma + "?"):
            return

        try:
            self.nghiep_vu_admin.xoa_nhan_vien(ma)
            self.hien_nhan_vien()
            messagebox.showinfo("Thành công", "Đã xóa nhân viên.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def them_tai_khoan_admin(self):
        fields = [
            {"key": "tenTaiKhoan", "label": "Tên tài khoản"},
            {"key": "matKhau", "label": "Mật khẩu", "default": "123456"},
            {
                "key": "maNhanVien",
                "label": "Nhân viên",
                "type": "combo",
                "values": self.tao_danh_sach_chon(
                    self.lay_nhan_vien_chua_co_tai_khoan(),
                    "maNhanVien",
                    "tenNhanVien",
                ),
            },
            {
                "key": "maVaiTro",
                "label": "Vai trò",
                "type": "combo",
                "values": self.tao_danh_sach_chon(
                    self.lay_vai_tro_duoc_cap(),
                    "maVaiTro",
                    "tenVaiTro",
                ),
            },
            {"key": "trangThai", "label": "Trạng thái", "type": "combo", "values": ["Hoạt động", "Đã khóa"]},
        ]

        def save(data):
            ma_vai_tro = data.pop("maVaiTro", "")
            self.nghiep_vu_admin.tao_tai_khoan(data, ma_vai_tro)
            self.hien_tai_khoan()

        self.mo_form_danh_muc_admin("Thêm tài khoản", fields, save)

    def sua_tai_khoan_admin(self):
        item = self.lay_item_dang_chon(self.bang_tai_khoan, "nguoi_dung.json", "taiKhoan", "maTaiKhoan")
        if item is None:
            return

        nguoi_dung = doc_json("nguoi_dung.json", {})
        ma_tai_khoan = item.get("maTaiKhoan", "")
        ma_vai_tro_hien_tai = ""

        for phan_quyen in nguoi_dung.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                ma_vai_tro_hien_tai = phan_quyen.get("maVaiTro", "")
                break

        values = dict(item)
        values["maVaiTro"] = ma_vai_tro_hien_tai
        values["trangThai"] = self.lay_gia_tri_trang_thai_nguoi_dung(item.get("trangThai", ""))

        fields = [
            {"key": "tenTaiKhoan", "label": "Tên tài khoản"},
            {
                "key": "maNhanVien",
                "label": "Nhân viên",
                "type": "combo",
                "values": self.tao_danh_sach_chon(
                    self.lay_nhan_vien_chua_co_tai_khoan(ma_tai_khoan),
                    "maNhanVien",
                    "tenNhanVien",
                ),
            },
            {
                "key": "maVaiTro",
                "label": "Vai trò",
                "type": "combo",
                "values": self.tao_danh_sach_chon(
                    self.lay_vai_tro_duoc_cap(),
                    "maVaiTro",
                    "tenVaiTro",
                ),
            },
            {"key": "trangThai", "label": "Trạng thái", "type": "combo", "values": ["Hoạt động", "Đã khóa"]},
        ]

        def save(data):
            ma_vai_tro = data.pop("maVaiTro", "")
            data["matKhau"] = item.get("matKhau", "")
            self.nghiep_vu_admin.cap_nhat_tai_khoan(ma_tai_khoan, data, ma_vai_tro)
            self.hien_tai_khoan()

        self.mo_form_danh_muc_admin("Sửa tài khoản", fields, save, values)

    def xoa_tai_khoan_admin(self):
        item = self.lay_item_dang_chon(self.bang_tai_khoan, "nguoi_dung.json", "taiKhoan", "maTaiKhoan")
        if item is None:
            return

        ma = item.get("maTaiKhoan", "")
        if not messagebox.askyesno("Xác nhận", "Xóa tài khoản " + ma + "?"):
            return

        try:
            self.nghiep_vu_admin.xoa_tai_khoan(ma)
            self.hien_tai_khoan()
            messagebox.showinfo("Thành công", "Đã xóa tài khoản.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def them_kho_admin(self):
        fields = [
            {"key": "tenKho", "label": "Tên kho"},
            {"key": "diaDiem", "label": "Địa điểm"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
        ]

        def save(data):
            self.nghiep_vu_admin.them_danh_muc_json("kho_hang.json", "kho", "maKho", "KHO", data, "Kho", 3)
            self.hien_kho()

        self.mo_form_danh_muc_admin("Thêm kho", fields, save)

    def sua_kho_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_kho", None), "kho_hang.json", "kho", "maKho")
        if item is None:
            return

        fields = [
            {"key": "tenKho", "label": "Tên kho"},
            {"key": "diaDiem", "label": "Địa điểm"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
        ]

        def save(data):
            self.nghiep_vu_admin.sua_danh_muc_json("kho_hang.json", "kho", "maKho", item.get("maKho", ""), data, "Kho")
            self.hien_kho()

        self.mo_form_danh_muc_admin("Sửa kho", fields, save, item)

    def xoa_kho_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_kho", None), "kho_hang.json", "kho", "maKho")
        if item is None:
            return
        ma = item.get("maKho", "")
        if not messagebox.askyesno("Xác nhận", "Xóa kho " + ma + "?"):
            return
        try:
            self.nghiep_vu_admin.xoa_kho(ma)
            self.hien_kho()
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def them_loai_hang_admin(self):
        fields = [
            {"key": "tenLoaiHang", "label": "Tên loại hàng", "validate": "text"},
            {"key": "ghiChu", "label": "Ghi chú", "required": False},
        ]

        def save(data):
            self.nghiep_vu_admin.them_danh_muc_json("hang_hoa.json", "loaiHang", "maLoaiHang", "LH", data, "Loại hàng", 4)
            self.hien_loai_hang()

        self.mo_form_danh_muc_admin("Thêm loại hàng", fields, save)

    def sua_loai_hang_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_loai_hang", None), "hang_hoa.json", "loaiHang", "maLoaiHang")
        if item is None:
            return

        fields = [
            {"key": "tenLoaiHang", "label": "Tên loại hàng", "validate": "text"},
            {"key": "ghiChu", "label": "Ghi chú", "required": False},
        ]

        def save(data):
            self.nghiep_vu_admin.sua_danh_muc_json("hang_hoa.json", "loaiHang", "maLoaiHang", item.get("maLoaiHang", ""), data, "Loại hàng")
            self.hien_loai_hang()

        self.mo_form_danh_muc_admin("Sửa loại hàng", fields, save, item)

    def xoa_loai_hang_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_loai_hang", None), "hang_hoa.json", "loaiHang", "maLoaiHang")
        if item is None:
            return
        ma = item.get("maLoaiHang", "")
        if not messagebox.askyesno("Xác nhận", "Xóa loại hàng " + ma + "?"):
            return
        try:
            self.nghiep_vu_admin.xoa_loai_hang(ma)
            self.hien_loai_hang()
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def them_nha_san_xuat_admin(self):
        fields = [
            {"key": "tenNhaSanXuat", "label": "Tên nhà sản xuất", "validate": "text"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
            {"key": "email", "label": "Email", "required": False, "validate": "email"},
            {"key": "diaChi", "label": "Địa chỉ", "required": False},
        ]

        def save(data):
            self.nghiep_vu_admin.them_danh_muc_json("doi_tac.json", "nhaSanXuat", "maNhaSanXuat", "NSX", data, "Nhà sản xuất", 3)
            self.hien_nha_san_xuat()

        self.mo_form_danh_muc_admin("Thêm nhà sản xuất", fields, save)

    def sua_nha_san_xuat_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_nha_san_xuat", None), "doi_tac.json", "nhaSanXuat", "maNhaSanXuat")
        if item is None:
            return

        fields = [
            {"key": "tenNhaSanXuat", "label": "Tên nhà sản xuất", "validate": "text"},
            {"key": "soDienThoai", "label": "Số điện thoại", "required": False, "validate": "phone"},
            {"key": "email", "label": "Email", "required": False, "validate": "email"},
            {"key": "diaChi", "label": "Địa chỉ", "required": False},
        ]

        def save(data):
            self.nghiep_vu_admin.sua_danh_muc_json("doi_tac.json", "nhaSanXuat", "maNhaSanXuat", item.get("maNhaSanXuat", ""), data, "Nhà sản xuất")
            self.hien_nha_san_xuat()

        self.mo_form_danh_muc_admin("Sửa nhà sản xuất", fields, save, item)

    def xoa_nha_san_xuat_admin(self):
        item = self.lay_item_dang_chon(getattr(self, "bang_nha_san_xuat", None), "doi_tac.json", "nhaSanXuat", "maNhaSanXuat")
        if item is None:
            return
        ma = item.get("maNhaSanXuat", "")
        if not messagebox.askyesno("Xác nhận", "Xóa nhà sản xuất " + ma + "?"):
            return
        try:
            self.nghiep_vu_admin.xoa_nha_san_xuat(ma)
            self.hien_nha_san_xuat()
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    # =========================
    # QUẢN LÝ PHIẾU NHẬP / XUẤT CỦA ADMIN
    # =========================
    def lay_danh_sach_kho_admin(self):
        return doc_json("kho_hang.json", {}).get("kho", [])

    def lay_danh_sach_vi_tri_admin(self):
        return doc_json("kho_hang.json", {}).get("viTriKho", [])

    def lay_danh_sach_san_pham_admin(self):
        return doc_json("hang_hoa.json", {}).get("sanPham", [])

    def lay_danh_sach_nha_san_xuat_admin(self):
        return doc_json("doi_tac.json", {}).get("nhaSanXuat", [])

    def lay_danh_sach_khach_hang_admin(self):
        return doc_json("doi_tac.json", {}).get("khachHang", [])

    def tim_san_pham_admin(self, ma_san_pham):
        for san_pham in self.lay_danh_sach_san_pham_admin():
            if san_pham.get("maSanPham", "") == ma_san_pham:
                return san_pham
        return None

    def mo_form_nhap_xuat_admin(self, loai, phieu=None):
        la_nhap = loai == "nhap"
        la_sua = phieu is not None

        if la_nhap:
            title = "Sửa phiếu nhập kho" if la_sua else "Tạo phiếu nhập kho"
            doi_tac_label = "Nhà sản xuất"
            doi_tac_list = self.lay_danh_sach_nha_san_xuat_admin()
            doi_tac_ma = "maNhaSanXuat"
            doi_tac_ten = "tenNhaSanXuat"
        else:
            title = "Sửa phiếu xuất kho" if la_sua else "Tạo phiếu xuất kho"
            doi_tac_label = "Khách hàng"
            doi_tac_list = self.lay_danh_sach_khach_hang_admin()
            doi_tac_ma = "maKhachHang"
            doi_tac_ten = "tenKhachHang"

        danh_sach_kho = self.lay_danh_sach_kho_admin()
        danh_sach_san_pham_data = self.lay_danh_sach_san_pham_admin()

        if len(danh_sach_kho) == 0 or len(doi_tac_list) == 0 or len(danh_sach_san_pham_data) == 0:
            messagebox.showwarning("Thiếu dữ liệu", "Cần có kho, đối tác và sản phẩm trước khi tạo phiếu.")
            return

        form = self.tao_cua_so_form(title, 760, 700)
        khung = form["body"]

        doi_tac_cb = self.tao_combobox_form(
            khung,
            doi_tac_label,
            self.tao_danh_sach_chon(doi_tac_list, doi_tac_ma, doi_tac_ten),
        )

        kho_cb = self.tao_combobox_form(
            khung,
            "Kho",
            self.tao_danh_sach_chon(danh_sach_kho, "maKho", "tenKho"),
        )

        so_dong_entry = self.tao_entry_form(khung, "Số lượng sản phẩm trong phiếu")
        self.gan_rang_buoc_chi_nhap_so(so_dong_entry, "Số lượng sản phẩm trong phiếu")

        khung_nut_dong = tk.Frame(khung, bg=self.mau_card)
        khung_nut_dong.pack(fill="x", pady=(8, 8))

        khung_chi_tiet = tk.Frame(khung, bg=self.mau_card)
        khung_chi_tiet.pack(fill="both", expand=True)

        danh_sach_dong = []
        danh_sach_san_pham = self.tao_danh_sach_chon(danh_sach_san_pham_data, "maSanPham", "tenSanPham")
        danh_sach_vi_tri = self.tao_danh_sach_chon(self.lay_danh_sach_vi_tri_admin(), "maViTri", "tenViTri")

        def lay_so_luong_ton(ma_kho, ma_san_pham):
            for item in self.lay_du_lieu_ton_kho_day_du():
                if item.get("maKho", "") == ma_kho and item.get("maSanPham", "") == ma_san_pham:
                    return self.chuyen_so(item.get("soLuongTon", 0))
            return 0

        def lay_danh_sach_san_pham_theo_kho(ma_san_pham_hien_tai=""):
            if la_nhap:
                return danh_sach_san_pham

            ma_kho = self.lay_ma_tu_combobox(kho_cb.get())
            ket_qua = []

            for san_pham in danh_sach_san_pham_data:
                ma_san_pham = san_pham.get("maSanPham", "")
                so_luong_ton = lay_so_luong_ton(ma_kho, ma_san_pham)

                if so_luong_ton > 0 or ma_san_pham == ma_san_pham_hien_tai:
                    ket_qua.append(
                        ma_san_pham
                        + " - "
                        + san_pham.get("tenSanPham", "")
                        + " (Tồn: "
                        + str(so_luong_ton)
                        + ")"
                    )

            return ket_qua

        def cap_nhat_san_pham_theo_kho():
            for dong in danh_sach_dong:
                sp_cb = dong["sp_cb"]
                ma_hien_tai = self.lay_ma_tu_combobox(sp_cb.get())
                values = lay_danh_sach_san_pham_theo_kho(ma_hien_tai)
                sp_cb["values"] = values
                ma_hop_le = any(self.lay_ma_tu_combobox(value) == ma_hien_tai for value in values)

                if ma_hien_tai != "" and ma_hop_le:
                    self.chon_combobox_theo_ma(sp_cb, ma_hien_tai)
                else:
                    sp_cb.set("")

                if sp_cb.get() == "" and len(values) > 0:
                    sp_cb.current(0)

                cap_nhat_thong_tin_dong(dong)

        def cap_nhat_thong_tin_dong(dong):
            sp_cb = dong["sp_cb"]
            don_gia_entry = dong["don_gia_entry"]
            ma_san_pham = self.lay_ma_tu_combobox(sp_cb.get())
            san_pham = self.tim_san_pham_admin(ma_san_pham)

            if san_pham is not None:
                don_gia_entry.delete(0, tk.END)
                don_gia_entry.insert(0, str(san_pham.get("donGia", 0)))

            if dong.get("ton_label") is not None:
                ma_kho = self.lay_ma_tu_combobox(kho_cb.get())
                dong["ton_label"].config(text=str(lay_so_luong_ton(ma_kho, ma_san_pham)))

        def tao_tieu_de_chi_tiet():
            header = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            header.pack(fill="x", pady=(0, 4))

            for text, width in [("Sản phẩm", 28), ("Số lượng", 10), ("Đơn giá", 12)]:
                tk.Label(
                    header,
                    text=text,
                    bg=self.mau_card,
                    fg=self.mau_chu_phu,
                    font=("Segoe UI", 10, "bold"),
                    width=width,
                    anchor="w",
                ).pack(side="left", padx=(0, 6))

            if la_nhap:
                tk.Label(
                    header,
                    text="Vị trí",
                    bg=self.mau_card,
                    fg=self.mau_chu_phu,
                    font=("Segoe UI", 10, "bold"),
                    width=18,
                    anchor="w",
                ).pack(side="left", padx=(0, 6))
            else:
                tk.Label(
                    header,
                    text="Tồn kho",
                    bg=self.mau_card,
                    fg=self.mau_chu_phu,
                    font=("Segoe UI", 10, "bold"),
                    width=10,
                    anchor="w",
                ).pack(side="left", padx=(0, 6))

        def tao_dong_san_pham(du_lieu=None):
            row = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            row.pack(fill="x", pady=4)

            sp_cb = ttk.Combobox(row, values=lay_danh_sach_san_pham_theo_kho(), state="readonly", font=("Segoe UI", 10), width=28)
            sp_cb.pack(side="left", padx=(0, 6))

            so_luong_entry = tk.Entry(row, font=("Segoe UI", 10), width=10, bg=self.mau_card_nhe, fg=self.mau_chu_dam, bd=0, highlightbackground=self.mau_vien, highlightthickness=1)
            so_luong_entry.pack(side="left", padx=(0, 6), ipady=4)
            self.gan_rang_buoc_chi_nhap_so(so_luong_entry, "Số lượng sản phẩm")

            don_gia_entry = tk.Entry(row, font=("Segoe UI", 10), width=12, bg=self.mau_card_nhe, fg=self.mau_chu_dam, bd=0, highlightbackground=self.mau_vien, highlightthickness=1)
            don_gia_entry.pack(side="left", padx=(0, 6), ipady=4)
            self.gan_rang_buoc_chi_nhap_so(don_gia_entry, "Đơn giá sản phẩm")

            if la_nhap:
                vi_tri_cb = ttk.Combobox(row, values=danh_sach_vi_tri, state="readonly", font=("Segoe UI", 10), width=18)
                vi_tri_cb.pack(side="left", padx=(0, 6))
                if len(danh_sach_vi_tri) > 0:
                    vi_tri_cb.current(0)
                ton_label = None
            else:
                vi_tri_cb = None
                ton_label = tk.Label(row, text="0", bg=self.mau_card, fg=self.mau_chu_dam, font=("Segoe UI", 10), width=10, anchor="w")
                ton_label.pack(side="left", padx=(0, 6))

            if len(sp_cb["values"]) > 0:
                sp_cb.current(0)

            dong = {
                "sp_cb": sp_cb,
                "so_luong_entry": so_luong_entry,
                "don_gia_entry": don_gia_entry,
                "vi_tri_cb": vi_tri_cb,
                "ton_label": ton_label,
            }

            sp_cb.bind("<<ComboboxSelected>>", lambda event: cap_nhat_thong_tin_dong(dong))

            if du_lieu is not None:
                sp_cb["values"] = lay_danh_sach_san_pham_theo_kho(du_lieu.get("maSanPham", ""))
                self.chon_combobox_theo_ma(sp_cb, du_lieu.get("maSanPham", ""))
                so_luong_entry.delete(0, tk.END)
                so_luong_entry.insert(0, str(du_lieu.get("soLuong", "")))
                don_gia_entry.delete(0, tk.END)
                don_gia_entry.insert(0, str(du_lieu.get("donGia", "")))

                if la_nhap and vi_tri_cb is not None:
                    self.chon_combobox_theo_ma(vi_tri_cb, du_lieu.get("maViTri", ""))

            cap_nhat_thong_tin_dong(dong)
            danh_sach_dong.append(dong)

        def xoa_dong_chi_tiet():
            for widget in khung_chi_tiet.winfo_children():
                widget.destroy()
            danh_sach_dong.clear()

        def tao_cac_dong_chi_tiet():
            try:
                so_dong = self.kiem_tra_chi_so(so_dong_entry.get(), "Số dòng sản phẩm", True, 1)
            except ValueError as loi:
                messagebox.showwarning("Dữ liệu không hợp lệ", str(loi))
                return

            xoa_dong_chi_tiet()
            tao_tieu_de_chi_tiet()
            for _ in range(so_dong):
                tao_dong_san_pham()

        self.tao_nut(khung_nut_dong, "Tạo dòng sản phẩm", tao_cac_dong_chi_tiet, self.mau_sua).pack(side="left")

        if la_sua:
            self.chon_combobox_theo_ma(doi_tac_cb, phieu.get("maNhaSanXuat", phieu.get("maKhachHang", "")))
            self.chon_combobox_theo_ma(kho_cb, phieu.get("maKho", ""))
            chi_tiet_cu = phieu.get("chiTiet", [])
            so_dong_entry.insert(0, str(len(chi_tiet_cu)))
            tao_tieu_de_chi_tiet()
            for item in chi_tiet_cu:
                tao_dong_san_pham(item)
        else:
            so_dong_entry.insert(0, "1")
            tao_tieu_de_chi_tiet()
            tao_dong_san_pham()

        def lay_du_lieu_form():
            ma_doi_tac = self.lay_ma_tu_combobox(doi_tac_cb.get())
            ma_kho = self.lay_ma_tu_combobox(kho_cb.get())

            if ma_doi_tac == "":
                raise ValueError("Vui lòng chọn đối tác.")
            if ma_kho == "":
                raise ValueError("Vui lòng chọn kho.")
            if len(danh_sach_dong) == 0:
                raise ValueError("Vui lòng tạo ít nhất 1 dòng sản phẩm.")

            chi_tiet = []
            for dong in danh_sach_dong:
                ma_san_pham = self.lay_ma_tu_combobox(dong["sp_cb"].get())
                so_luong = self.kiem_tra_chi_so(dong["so_luong_entry"].get(), "Số lượng sản phẩm", True, 1)
                don_gia = self.kiem_tra_chi_so(dong["don_gia_entry"].get(), "Đơn giá sản phẩm", True, 1)

                if ma_san_pham == "":
                    raise ValueError("Vui lòng chọn sản phẩm.")

                if not la_nhap:
                    so_luong_ton = lay_so_luong_ton(ma_kho, ma_san_pham)
                    if so_luong_ton <= 0:
                        raise ValueError("Sản phẩm " + ma_san_pham + " đã hết hàng trong kho đã chọn.")
                    if so_luong > so_luong_ton:
                        raise ValueError(
                            "Sản phẩm "
                            + ma_san_pham
                            + " chỉ còn "
                            + str(so_luong_ton)
                            + " trong kho đã chọn."
                        )

                item = {
                    "maSanPham": ma_san_pham,
                    "soLuong": so_luong,
                    "donGia": don_gia,
                }

                if la_nhap and dong["vi_tri_cb"] is not None:
                    ma_vi_tri = self.lay_ma_tu_combobox(dong["vi_tri_cb"].get())
                    if ma_vi_tri == "":
                        raise ValueError("Vui lòng chọn vị trí lưu cho sản phẩm nhập.")
                    item["maViTri"] = ma_vi_tri

                chi_tiet.append(item)

            return ma_doi_tac, ma_kho, chi_tiet

        def luu(luu_tam):
            try:
                ma_doi_tac, ma_kho, chi_tiet = lay_du_lieu_form()

                if la_sua:
                    if la_nhap:
                        self.nghiep_vu_admin.cap_nhat_phieu_nhap(phieu.get("maPhieuNhap", ""), ma_doi_tac, ma_kho, chi_tiet, luu_tam)
                    else:
                        self.nghiep_vu_admin.cap_nhat_phieu_xuat(phieu.get("maPhieuXuat", ""), ma_doi_tac, ma_kho, chi_tiet, luu_tam)
                else:
                    if la_nhap:
                        self.nghiep_vu_admin.tao_phieu_nhap(ma_doi_tac, ma_kho, chi_tiet, luu_tam)
                    else:
                        self.nghiep_vu_admin.tao_phieu_xuat(ma_doi_tac, ma_kho, chi_tiet, luu_tam)

                form["window"].destroy()

                if la_nhap:
                    self.hien_nhap_kho()
                else:
                    self.hien_xuat_kho()

                messagebox.showinfo("Thành công", "Đã lưu phiếu.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", lambda: luu(False), self.mau_them).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Lưu tạm", lambda: luu(True), self.mau_sua).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, self.mau_thoat).pack(side="right")
        kho_cb.bind("<<ComboboxSelected>>", lambda event: cap_nhat_san_pham_theo_kho())

    def sua_phieu_nhap_admin(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_nhap, "phieu_nhap.json", "maPhieuNhap")
        if phieu is not None:
            self.mo_form_nhap_xuat_admin("nhap", phieu)

    def sua_phieu_xuat_admin(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_xuat, "phieu_xuat.json", "maPhieuXuat")
        if phieu is not None:
            self.mo_form_nhap_xuat_admin("xuat", phieu)

    def huy_phieu_nhap_admin(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_nhap, "phieu_nhap.json", "maPhieuNhap")
        if phieu is None:
            return

        ma_phieu = phieu.get("maPhieuNhap", "")
        if not messagebox.askyesno("Xác nhận", "Hủy phiếu nhập " + ma_phieu + " và hoàn tồn kho về trước phiếu?"):
            return

        try:
            self.nghiep_vu_admin.huy_phieu_nhap(ma_phieu)
            self.hien_nhap_kho()
            messagebox.showinfo("Thành công", "Đã hủy phiếu nhập.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))
        except Exception as loi:
            messagebox.showerror("Lỗi", "Không thể hủy/xóa phiếu nhập: " + str(loi))

    def huy_phieu_xuat_admin(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_xuat, "phieu_xuat.json", "maPhieuXuat")
        if phieu is None:
            return

        ma_phieu = phieu.get("maPhieuXuat", "")
        if not messagebox.askyesno("Xác nhận", "Hủy phiếu xuất " + ma_phieu + " và hoàn tồn kho về trước phiếu?"):
            return

        try:
            self.nghiep_vu_admin.huy_phieu_xuat(ma_phieu)
            self.hien_xuat_kho()
            messagebox.showinfo("Thành công", "Đã hủy phiếu xuất.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))
        except Exception as loi:
            messagebox.showerror("Lỗi", "Không thể hủy/xóa phiếu xuất: " + str(loi))

    # =========================
    # QUẢN LÝ HÀNG HÓA CỦA ADMIN
    # =========================
    def them_hang_hoa_admin(self):
        self.mo_form_hang_hoa_admin()

    def sua_hang_hoa_admin(self):
        ma_san_pham = self.lay_ma_dong_dang_chon(self.bang_hang_hoa)

        if ma_san_pham == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sản phẩm cần sửa.")
            return

        san_pham = self.tim_san_pham_admin(ma_san_pham)

        if san_pham is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm đã chọn.")
            return

        self.mo_form_hang_hoa_admin(san_pham)

    def ngung_kinh_doanh_hang_hoa_admin(self):
        ma_san_pham = self.lay_ma_dong_dang_chon(self.bang_hang_hoa)

        if ma_san_pham == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sản phẩm cần đổi trạng thái.")
            return

        san_pham = self.tim_san_pham_admin(ma_san_pham)

        if san_pham is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm đã chọn.")
            return

        trang_thai_moi = self.lay_trang_thai_hang_hoa_moi(san_pham.get("trangThai", ""))

        if not messagebox.askyesno("Xác nhận", "Chuyển sản phẩm " + ma_san_pham + " sang trạng thái " + trang_thai_moi + "?"):
            return

        try:
            san_pham_moi = self.nghiep_vu_admin.doi_trang_thai_kinh_doanh_san_pham(ma_san_pham)
            self.hien_hang_hoa()
            messagebox.showinfo("Thành công", "Đã chuyển sản phẩm sang trạng thái " + san_pham_moi.get("trangThai", "") + ".")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def mo_form_hang_hoa_admin(self, san_pham=None):
        la_sua = san_pham is not None
        data = doc_json("hang_hoa.json", {})
        loai_hang = data.get("loaiHang", [])
        don_vi_tinh = data.get("donViTinh", [])

        if len(loai_hang) == 0 or len(don_vi_tinh) == 0:
            messagebox.showwarning("Thiếu dữ liệu", "Cần có loại hàng và đơn vị tính trước khi tạo sản phẩm.")
            return

        title = "Sửa sản phẩm" if la_sua else "Thêm sản phẩm"
        form = self.tao_cua_so_form(title, 540, 560)
        khung = form["body"]

        ten_entry = self.tao_entry_form(khung, "Tên sản phẩm")

        loai_cb = self.tao_combobox_form(
            khung,
            "Loại hàng",
            self.tao_danh_sach_chon(loai_hang, "maLoaiHang", "tenLoaiHang"),
        )

        dvt_cb = self.tao_combobox_form(
            khung,
            "Đơn vị tính",
            self.tao_danh_sach_chon(don_vi_tinh, "maDonViTinh", "tenDonViTinh"),
        )

        don_gia_entry = self.tao_entry_form(khung, "Đơn giá")
        muc_ton_entry = self.tao_entry_form(khung, "Mức tồn tối thiểu")
        self.gan_rang_buoc_chi_nhap_so(don_gia_entry, "Đơn giá")
        self.gan_rang_buoc_chi_nhap_so(muc_ton_entry, "Mức tồn tối thiểu")

        if la_sua:
            ten_entry.insert(0, san_pham.get("tenSanPham", ""))
            self.chon_combobox_theo_ma(loai_cb, san_pham.get("maLoaiHang", ""))
            self.chon_combobox_theo_ma(dvt_cb, san_pham.get("maDonViTinh", ""))
            don_gia_entry.insert(0, str(san_pham.get("donGia", 0)))
            muc_ton_entry.insert(0, str(san_pham.get("mucTonToiThieu", 0)))

        def luu():
            try:
                ten = ten_entry.get().strip()
                ma_loai = self.lay_ma_tu_combobox(loai_cb.get())
                ma_dvt = self.lay_ma_tu_combobox(dvt_cb.get())
                don_gia = self.kiem_tra_chi_so(don_gia_entry.get(), "Đơn giá", True, 1)
                muc_ton = self.kiem_tra_chi_so(muc_ton_entry.get(), "Mức tồn tối thiểu", True, 0)

                if la_sua:
                    self.nghiep_vu_admin.sua_san_pham(
                        san_pham.get("maSanPham", ""),
                        ten,
                        ma_loai,
                        ma_dvt,
                        don_gia,
                        muc_ton,
                    )
                else:
                    self.nghiep_vu_admin.tao_san_pham(
                        ten,
                        ma_loai,
                        ma_dvt,
                        don_gia,
                        muc_ton,
                    )

                form["window"].destroy()
                self.hien_hang_hoa()
                messagebox.showinfo("Thành công", "Đã lưu sản phẩm.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, self.mau_them).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, self.mau_thoat).pack(side="right")

    def them_kiem_ke_admin(self):
        danh_sach_kho = self.lay_danh_sach_kho_admin()

        if len(danh_sach_kho) == 0:
            messagebox.showwarning("Thiếu dữ liệu", "Cần có kho trước khi tạo phiếu kiểm kê.")
            return

        form = self.tao_cua_so_form("Tạo phiếu kiểm kho", 760, 650)
        khung = form["body"]

        kho_cb = self.tao_combobox_form(
            khung,
            "Kho",
            self.tao_danh_sach_chon(danh_sach_kho, "maKho", "tenKho"),
        )

        ghi_chu_entry = self.tao_entry_form(khung, "Ghi chú")

        self.tao_label(khung, "Chi tiết tồn kho", 10, self.mau_chu_phu, True).pack(anchor="w", pady=(10, 4))
        khung_chi_tiet = self.tao_khung_cuon_doc(khung)
        danh_sach_dong = []

        def lay_ton_theo_kho(ma_kho):
            return [
                ton
                for ton in self.lay_du_lieu_ton_kho_day_du()
                if ton.get("maKho", "") == ma_kho
            ]

        def ve_header():
            header = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            header.pack(fill="x", pady=(0, 4))

            for text, width in [("Sản phẩm", 36), ("SL hệ thống", 14), ("SL thực tế", 14)]:
                tk.Label(
                    header,
                    text=text,
                    bg=self.mau_card,
                    fg=self.mau_chu_phu,
                    font=("Segoe UI", 10, "bold"),
                    width=width,
                    anchor="w",
                ).pack(side="left", padx=(0, 8))

        def ve_dong(ton):
            row = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            row.pack(fill="x", pady=3)

            ma_san_pham = ton.get("maSanPham", "")
            ten_san_pham = ton.get("tenSanPham", "")
            so_luong_he_thong = self.chuyen_so_nguyen(ton.get("soLuongTon", 0))

            tk.Label(
                row,
                text=ma_san_pham + " - " + ten_san_pham,
                bg=self.mau_card,
                fg=self.mau_chu_dam,
                font=("Segoe UI", 10),
                width=36,
                anchor="w",
            ).pack(side="left", padx=(0, 8))

            tk.Label(
                row,
                text=str(so_luong_he_thong),
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                font=("Segoe UI", 10),
                width=14,
                anchor="w",
                padx=8,
                pady=5,
            ).pack(side="left", padx=(0, 8))

            thuc_te_entry = tk.Entry(
                row,
                font=("Segoe UI", 10),
                width=14,
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                bd=0,
                highlightbackground=self.mau_vien,
                highlightthickness=1,
            )
            thuc_te_entry.pack(side="left", padx=(0, 8), ipady=5)
            self.gan_rang_buoc_chi_nhap_so(thuc_te_entry, "Số lượng thực tế")
            thuc_te_entry.insert(0, str(so_luong_he_thong))

            danh_sach_dong.append({
                "maSanPham": ma_san_pham,
                "entry": thuc_te_entry,
            })

        def tai_ton_kho(event=None):
            for widget in khung_chi_tiet.winfo_children():
                widget.destroy()
            danh_sach_dong.clear()

            ma_kho = self.lay_ma_tu_combobox(kho_cb.get())
            danh_sach_ton = lay_ton_theo_kho(ma_kho)

            if len(danh_sach_ton) == 0:
                self.tao_label(
                    khung_chi_tiet,
                    "Kho này chưa có tồn kho để kiểm kê.",
                    11,
                    self.mau_chu_phu,
                    True,
                ).pack(anchor="w", pady=12)
                return

            ve_header()
            for ton in danh_sach_ton:
                ve_dong(ton)

        kho_cb.bind("<<ComboboxSelected>>", tai_ton_kho)
        tai_ton_kho()

        def luu():
            try:
                ma_kho = self.lay_ma_tu_combobox(kho_cb.get())
                if ma_kho == "":
                    raise ValueError("Vui lòng chọn kho kiểm kê.")

                chi_tiet = []
                for dong in danh_sach_dong:
                    so_luong_thuc_te = self.kiem_tra_chi_so(dong["entry"].get(), "Số lượng thực tế", True, 0)
                    chi_tiet.append({
                        "maSanPham": dong["maSanPham"],
                        "soLuongThucTe": so_luong_thuc_te,
                    })

                if len(chi_tiet) == 0:
                    raise ValueError("Kho này chưa có tồn kho để kiểm kê.")

                self.nghiep_vu_admin.tao_phieu_kiem_ke(
                    ma_kho,
                    chi_tiet,
                    ghi_chu_entry.get().strip(),
                )

                form["window"].destroy()
                self.hien_kiem_kho()
                messagebox.showinfo("Thành công", "Đã tạo phiếu kiểm kho và cập nhật tồn.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, self.mau_them).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, self.mau_thoat).pack(side="right")

    def sua_kiem_ke_admin(self):
        phieu = self.lay_phieu_da_chon(self.bang_kiem_kho, "kiem_ke.json", "maKiemKe")

        if phieu is None:
            return

        self.mo_form_sua_kiem_ke_admin(phieu)

    def mo_form_sua_kiem_ke_admin(self, phieu):
        form = self.tao_cua_so_form("Sửa phiếu kiểm kho " + phieu.get("maKiemKe", ""), 760, 620)
        khung = form["body"]

        kho_value = phieu.get("maKho", "")
        self.tao_label(khung, "Kho: " + kho_value, 11, self.mau_chu_dam, True).pack(anchor="w", pady=(0, 8))

        ghi_chu_entry = self.tao_entry_form(khung, "Ghi chú")
        ghi_chu_entry.insert(0, phieu.get("ghiChu", ""))

        self.tao_label(khung, "Chi tiết kiểm kê", 10, self.mau_chu_phu, True).pack(anchor="w", pady=(10, 4))
        khung_chi_tiet = self.tao_khung_cuon_doc(khung)
        danh_sach_dong = []

        header = tk.Frame(khung_chi_tiet, bg=self.mau_card)
        header.pack(fill="x", pady=(0, 4))

        for text, width in [("Sản phẩm", 36), ("SL hệ thống", 14), ("SL thực tế", 14)]:
            tk.Label(
                header,
                text=text,
                bg=self.mau_card,
                fg=self.mau_chu_phu,
                font=("Segoe UI", 10, "bold"),
                width=width,
                anchor="w",
            ).pack(side="left", padx=(0, 8))

        for item in phieu.get("chiTiet", []):
            row = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            row.pack(fill="x", pady=3)

            ma_san_pham = item.get("maSanPham", "")
            san_pham = self.tim_san_pham_admin(ma_san_pham)
            ten_san_pham = san_pham.get("tenSanPham", "") if san_pham is not None else ""

            tk.Label(
                row,
                text=ma_san_pham + " - " + ten_san_pham,
                bg=self.mau_card,
                fg=self.mau_chu_dam,
                font=("Segoe UI", 10),
                width=36,
                anchor="w",
            ).pack(side="left", padx=(0, 8))

            tk.Label(
                row,
                text=str(item.get("soLuongHeThong", 0)),
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                font=("Segoe UI", 10),
                width=14,
                anchor="w",
                padx=8,
                pady=5,
            ).pack(side="left", padx=(0, 8))

            thuc_te_entry = tk.Entry(
                row,
                font=("Segoe UI", 10),
                width=14,
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                bd=0,
                highlightbackground=self.mau_vien,
                highlightthickness=1,
            )
            thuc_te_entry.pack(side="left", padx=(0, 8), ipady=5)
            self.gan_rang_buoc_chi_nhap_so(thuc_te_entry, "Số lượng thực tế")
            thuc_te_entry.insert(0, str(item.get("soLuongThucTe", 0)))

            danh_sach_dong.append({
                "maSanPham": ma_san_pham,
                "entry": thuc_te_entry,
            })

        def luu():
            try:
                chi_tiet = []
                for dong in danh_sach_dong:
                    so_luong_thuc_te = self.kiem_tra_chi_so(dong["entry"].get(), "Số lượng thực tế", True, 0)
                    chi_tiet.append({
                        "maSanPham": dong["maSanPham"],
                        "soLuongThucTe": so_luong_thuc_te,
                    })

                self.nghiep_vu_admin.cap_nhat_phieu_kiem_ke(
                    phieu.get("maKiemKe", ""),
                    kho_value,
                    chi_tiet,
                    ghi_chu_entry.get().strip(),
                )
                form["window"].destroy()
                self.hien_kiem_kho()
                messagebox.showinfo("Thành công", "Đã cập nhật phiếu kiểm kê.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, self.mau_them).pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, self.mau_thoat).pack(side="right")

    # =========================
    # XEM CHI TIẾT PHIẾU
    # =========================
    def xem_chi_tiet_phieu_nhap(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_nhap, "phieu_nhap.json", "maPhieuNhap")

        if phieu is not None:
            self.mo_chi_tiet_phieu(phieu, "nhap")

    def xem_chi_tiet_phieu_xuat(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_xuat, "phieu_xuat.json", "maPhieuXuat")

        if phieu is not None:
            self.mo_chi_tiet_phieu(phieu, "xuat")

    def xem_chi_tiet_kiem_ke(self):
        phieu = self.lay_phieu_da_chon(self.bang_kiem_kho, "kiem_ke.json", "maKiemKe")

        if phieu is not None:
            self.mo_chi_tiet_phieu(phieu, "kiem")

    def lay_phieu_da_chon(self, bang, ten_file, truong_ma):
        ma_phieu = self.lay_ma_dong_dang_chon(bang)

        if ma_phieu == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một dòng.")
            return None

        for item in doc_json(ten_file, []):
            if item.get(truong_ma) == ma_phieu:
                return item

        messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu đã chọn.")
        return None

    # =========================
    # HỦY PHIẾU KIỂM KHO
    # =========================
    def lay_kiem_ke_dang_hien_thi(self):
        data = self.chuan_hoa_trang_thai(doc_json("kiem_ke.json", []))
        ket_qua = []

        for item in data:
            dong = dict(item)
            trang_thai = str(dong.get("trangThai", "")).strip()

            if trang_thai == "":
                trang_thai = "Đã kiểm kê"
                dong["trangThai"] = trang_thai

            trang_thai_lower = trang_thai.lower()

            if trang_thai_lower in ["đã hủy", "da huy", "hủy", "huy"]:
                continue

            ket_qua.append(dong)

        return ket_qua

    def huy_phieu_kiem_kho(self):
        if not hasattr(self, "bang_kiem_kho"):
            messagebox.showwarning(
                "Chưa chọn dữ liệu",
                "Vui lòng chọn phiếu kiểm kho cần hủy.",
            )
            return

        ma_kiem_ke = self.lay_ma_dong_dang_chon(self.bang_kiem_kho)

        if ma_kiem_ke == "":
            messagebox.showwarning(
                "Chưa chọn dữ liệu",
                "Vui lòng chọn phiếu kiểm kho cần hủy.",
            )
            return

        phieu = None
        for item in doc_json("kiem_ke.json", []):
            if item.get("maKiemKe", "") == ma_kiem_ke:
                phieu = item
                break

        if phieu is None:
            messagebox.showerror("Lỗi", "Không tìm thấy phiếu kiểm kho đã chọn.")
            return

        if not self.la_phieu_luu_tam(phieu):
            messagebox.showwarning(
                "Không thể hủy",
                "Chỉ được hủy/xóa phiếu kiểm kho đang lưu tạm.",
            )
            return

        hoi = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa phiếu kiểm kho lưu tạm " + ma_kiem_ke + " không?",
        )

        if not hoi:
            return

        try:
            self.nghiep_vu_admin.xoa_phieu_kiem_ke(ma_kiem_ke, khoi_phuc_ton_cu=False)
            messagebox.showinfo("Thành công", "Đã xóa phiếu kiểm kho lưu tạm.")
            self.hien_kiem_kho()
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))
        except Exception as loi:
            messagebox.showerror("Lỗi", "Không thể hủy/xóa phiếu kiểm kho: " + str(loi))

    # =========================
    # QUẢN LÝ TÀI KHOẢN / NHÂN VIÊN
    # =========================
    def doc_nguoi_dung(self):
        return self.nghiep_vu_admin.doc_nguoi_dung()

    def ghi_nguoi_dung(self, data):
        self.nghiep_vu_admin.ghi_nguoi_dung(data)

    def lay_trang_thai_moi(self, trang_thai_hien_tai):
        return self.nghiep_vu_admin.lay_trang_thai_moi(trang_thai_hien_tai)

    def la_tai_khoan_admin_hien_tai(self, ma_nhan_vien="", ma_tai_khoan=""):
        return self.nghiep_vu_admin.la_tai_khoan_dang_dung(
            ma_tai_khoan=ma_tai_khoan,
            ma_nhan_vien=ma_nhan_vien,
        )

    def khoa_mo_nhan_vien(self):
        if not hasattr(self, "bang_nhan_vien"):
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn nhân viên cần khóa/mở.")
            return

        ma_nhan_vien = self.lay_ma_dong_dang_chon(self.bang_nhan_vien)

        if ma_nhan_vien == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn nhân viên cần khóa/mở.")
            return

        try:
            self.nghiep_vu_admin.khoa_mo_nhan_vien(ma_nhan_vien)
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi))
            return

        messagebox.showinfo("Thành công", "Đã cập nhật trạng thái nhân viên.")
        self.hien_nhan_vien()
        return

    def khoa_mo_tai_khoan(self):
        if not hasattr(self, "bang_tai_khoan"):
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn tài khoản cần khóa/mở.")
            return

        ma_tai_khoan = self.lay_ma_dong_dang_chon(self.bang_tai_khoan)

        if ma_tai_khoan == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn tài khoản cần khóa/mở.")
            return

        try:
            self.nghiep_vu_admin.khoa_mo_tai_khoan(ma_tai_khoan)
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi))
            return

        messagebox.showinfo("Thành công", "Đã cập nhật trạng thái tài khoản.")
        self.hien_tai_khoan()
        return

    def reset_mat_khau_tai_khoan(self):
        if not hasattr(self, "bang_tai_khoan"):
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn tài khoản cần reset mật khẩu.")
            return

        ma_tai_khoan = self.lay_ma_dong_dang_chon(self.bang_tai_khoan)

        if ma_tai_khoan == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn tài khoản cần reset mật khẩu.")
            return

        if self.la_tai_khoan_admin_hien_tai(ma_tai_khoan=ma_tai_khoan):
            messagebox.showwarning(
                "Không thể thao tác",
                "Không thể reset mật khẩu của chính tài khoản Admin đang dùng.",
            )
            return

        hoi = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn reset mật khẩu tài khoản " + ma_tai_khoan + " không?",
        )

        if not hoi:
            return

        try:
            mat_khau_moi = self.nghiep_vu_admin.reset_mat_khau_tai_khoan(ma_tai_khoan)
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi))
            return

        messagebox.showinfo("Thành công", "Mật khẩu mới là: " + mat_khau_moi)
        self.hien_tai_khoan()
        return

    def tao_ma_nhat_ky_moi(self, danh_sach):
        return self.nghiep_vu_admin.tao_ma_tu_dong(danh_sach, "maNhatKy", "NK")

    def ghi_nhat_ky(self, hanh_dong, doi_tuong, ghi_chu):
        self.nghiep_vu_admin.ghi_nhat_ky(hanh_dong, doi_tuong, ghi_chu)

    def loc_nhat_ky_thao_tac(self, danh_sach, loai, tu_ngay, den_ngay, tu_khoa):
        ket_qua = []
        tu_khoa = tu_khoa.lower().strip()

        tu_ngay, den_ngay = self.kiem_tra_khoang_ngay_loc(tu_ngay, den_ngay)

        for item in danh_sach:
            hanh_dong = str(item.get("hanhDong", "")).lower()

            if "đăng nhập" in hanh_dong or "đăng xuất" in hanh_dong:
                continue

            thoi_gian = str(item.get("thoiGian", ""))
            ngay_so_sanh = self.chuan_hoa_ngay_loc(thoi_gian)

            noi_dung = " ".join(
                str(item.get(key, ""))
                for key in ["maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai", "ghiChu"]
            ).lower()

            if loai != "Tất cả":
                if loai == "Khóa/Mở khóa":
                    if "khóa" not in hanh_dong and "mở" not in hanh_dong:
                        continue
                elif loai == "Reset mật khẩu":
                    if "reset" not in hanh_dong:
                        continue
                elif loai.lower() not in hanh_dong:
                    continue

            if tu_ngay != "" and ngay_so_sanh != "" and ngay_so_sanh < tu_ngay:
                continue

            if den_ngay != "" and ngay_so_sanh != "" and ngay_so_sanh > den_ngay:
                continue

            if tu_khoa != "" and tu_khoa not in noi_dung:
                continue

            ket_qua.append(item)

        return ket_qua

    def kiem_tra_khoang_ngay_loc(self, tu_ngay, den_ngay):
        tu_ngay = self.kiem_tra_ngay(tu_ngay, "Từ ngày", False)
        den_ngay = self.kiem_tra_ngay(den_ngay, "Đến ngày", False)

        if tu_ngay != "" and den_ngay != "" and tu_ngay > den_ngay:
            raise ValueError("Từ ngày không được lớn hơn đến ngày.")

        return tu_ngay, den_ngay

    def chuan_hoa_ngay_loc(self, thoi_gian):
        thoi_gian = str(thoi_gian)

        if len(thoi_gian) >= 10 and "/" in thoi_gian:
            ngay = thoi_gian[:10].split("/")
            if len(ngay) == 3:
                return ngay[2] + "-" + ngay[1] + "-" + ngay[0]

        if len(thoi_gian) >= 10 and "-" in thoi_gian:
            return thoi_gian[:10]

        return ""

    # =========================
    # QUẢN LÝ TRẠNG THÁI HÀNG HÓA
    # =========================
    def chuan_hoa_trang_thai_san_pham(self, danh_sach):
        ket_qua = []

        for item in danh_sach:
            dong = dict(item)
            trang_thai = self.lay_gia_tri(
                item,
                "trangThai",
                "trang_thai",
                "TRANGTHAI",
                "TrangThai",
                "trạngThái",
            )

            trang_thai_text = str(trang_thai).strip().lower()

            if trang_thai_text in ["", "true", "1", "active", "đang bán", "hoạt động", "kinh doanh"]:
                trang_thai = "Hoạt động"
            elif trang_thai_text in ["false", "0", "inactive", "ngừng kinh doanh", "ngung kinh doanh", "đã ngừng"]:
                trang_thai = "Ngừng kinh doanh"

            dong["trangThai"] = trang_thai
            ket_qua.append(dong)

        return ket_qua

    def lay_trang_thai_hang_hoa_moi(self, trang_thai_hien_tai):
        trang_thai = str(trang_thai_hien_tai).strip().lower()

        if trang_thai in ["ngừng kinh doanh", "ngung kinh doanh", "false", "0", "inactive"]:
            return "Hoạt động"

        return "Ngừng kinh doanh"

    def cap_nhat_trang_thai_hang_hoa(self):
        if not hasattr(self, "bang_hang_hoa"):
            messagebox.showwarning(
                "Chưa chọn dữ liệu",
                "Vui lòng chọn hàng hóa cần cập nhật trạng thái.",
            )
            return

        ma_san_pham = self.lay_ma_dong_dang_chon(self.bang_hang_hoa)

        if ma_san_pham == "":
            messagebox.showwarning(
                "Chưa chọn dữ liệu",
                "Vui lòng chọn hàng hóa cần cập nhật trạng thái.",
            )
            return

        data = doc_json("hang_hoa.json", {})
        danh_sach = data.get("sanPham", [])
        da_tim_thay = False
        trang_thai_moi = ""

        for item in danh_sach:
            if item.get("maSanPham") == ma_san_pham:
                trang_thai_hien_tai = self.lay_gia_tri(
                    item,
                    "trangThai",
                    "trang_thai",
                    "TRANGTHAI",
                    "TrangThai",
                    "trạngThái",
                )
                trang_thai_moi = self.lay_trang_thai_hang_hoa_moi(trang_thai_hien_tai)
                item["trangThai"] = trang_thai_moi
                da_tim_thay = True
                break

        if not da_tim_thay:
            messagebox.showerror("Lỗi", "Không tìm thấy hàng hóa đã chọn.")
            return

        hoi = messagebox.askyesno(
            "Xác nhận",
            "Cập nhật trạng thái sản phẩm " + ma_san_pham + " thành '" + trang_thai_moi + "'?"
        )

        if not hoi:
            return

        ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky(
            "Cập nhật trạng thái",
            "Hàng hóa",
            "Cập nhật trạng thái " + ma_san_pham + " thành " + trang_thai_moi,
        )

        messagebox.showinfo("Thành công", "Đã cập nhật trạng thái hàng hóa.")
        self.hien_hang_hoa()

    # =========================
    # CHUẨN HÓA DỮ LIỆU PHIẾU
    # =========================
    def sua_loi_dau_trang_thai(self, value):
        text = str(value).strip()

        if text == "":
            return ""

        lower = text.lower()

        if "lưu" in lower or "luu" in lower:
            return "Lưu tạm"

        if "hủy" in lower or "huy" in lower:
            return "Đã hủy"

        if "nh" in lower and ("?" in lower or "nhập" in lower or "nhap" in lower):
            return "Đã nhập"

        if "xu" in lower and ("?" in lower or "xuất" in lower or "xuat" in lower):
            return "Đã xuất"

        if lower in ["true", "1", "done", "success", "thành công"]:
            return "Thành công"

        return text

    def chuan_hoa_trang_thai_phieu(self, danh_sach, loai_phieu):
        ket_qua = []

        for item in danh_sach:
            dong = dict(item)
            trang_thai = self.lay_gia_tri(
                item,
                "trangThai",
                "trang_thai",
                "TRANGTHAI",
                "TrangThai",
                "trạngThái",
                "trạng thái",
            )

            trang_thai = self.sua_loi_dau_trang_thai(trang_thai)

            if trang_thai == "":
                if loai_phieu == "nhap":
                    trang_thai = "Đã nhập"
                else:
                    trang_thai = "Đã xuất"

            dong["trangThai"] = trang_thai
            ket_qua.append(dong)

        return ket_qua

    def dinh_dang_danh_sach_phieu(self, danh_sach):
        return self.dinh_dang_danh_sach_phieu_tien(danh_sach)

    def tinh_tong_tien_tu_danh_sach(self, danh_sach):
        return tinh_admin.tinh_tong_tien_tu_danh_sach(danh_sach)

    def lay_phieu_moi_nhat(self, danh_sach, ngay_field):
        return tinh_admin.lay_phieu_moi_nhat(danh_sach, ngay_field)

    # =========================
    # HÀM PHỤ DỮ LIỆU
    # =========================
    def lay_gia_tri(self, item, *keys):
        for key in keys:
            if key in item:
                return item.get(key)

        return ""

    def chuan_hoa_trang_thai(self, danh_sach):
        ket_qua = []

        for item in danh_sach:
            dong = dict(item)

            trang_thai = self.lay_gia_tri(
                item,
                "trangThai",
                "trang_thai",
                "TRANGTHAI",
                "trạngThái",
                "TrangThai",
                "trang thai",
                "trạng thái",
            )

            if trang_thai == "":
                trang_thai = dong.get("trangThai", "")

            trang_thai_text = str(trang_thai).strip().lower()

            if trang_thai_text in ["true", "1", "active", "đang hoạt động"]:
                trang_thai = "Hoạt động"
            elif trang_thai_text in ["false", "0", "inactive", "ngừng hoạt động", "đã khóa"]:
                trang_thai = "Đã khóa"

            dong["trangThai"] = trang_thai
            ket_qua.append(dong)

        return ket_qua

    def loc_du_lieu(self, danh_sach, tu_khoa, danh_sach_truong):
        tu_khoa = tu_khoa.lower().strip()
        ket_qua = []

        for item in danh_sach:
            noi_dung = ""

            for truong in danh_sach_truong:
                noi_dung += str(item.get(truong, "")) + " "

            if tu_khoa == "" or tu_khoa in noi_dung.lower():
                ket_qua.append(item)

        return ket_qua

    def dem_nhan_vien(self):
        data = doc_json("nguoi_dung.json", {})
        return len(data.get("nhanVien", []))

    def dem_so_kho(self):
        data = doc_json("kho_hang.json", {})
        return len(data.get("kho", []))

    def dem_so_hang_hoa(self):
        data = doc_json("hang_hoa.json", {})
        return len(data.get("sanPham", []))

    def dem_so_thong_ke(self):
        return 6

    def rut_gon_chu(self, text, max_len):
        text = str(text)

        if len(text) <= max_len:
            return text

        return text[:max_len] + "..."

    def lay_du_lieu_ton_kho_day_du(self):
        kho_data = doc_json("kho_hang.json", {})
        hang_data = doc_json("hang_hoa.json", {})

        return tinh_ton_kho.lap_du_lieu_ton_kho(
            kho_data.get("tonKho", []),
            hang_data.get("sanPham", []),
            kho_data.get("viTriKho", []),
        )

    def lay_canh_bao_ton_thap(self):
        kho_data = doc_json("kho_hang.json", {})
        hang_data = doc_json("hang_hoa.json", {})

        return tinh_ton_kho.lay_canh_bao_ton_thap(
            kho_data.get("tonKho", []),
            hang_data.get("sanPham", []),
            kho_data.get("viTriKho", []),
        )

    def dem_ton_thap(self):
        return len(self.lay_canh_bao_ton_thap())

    def lay_du_lieu_gia_tri_kho(self):
        kho_data = doc_json("kho_hang.json", {})
        hang_data = doc_json("hang_hoa.json", {})

        return tinh_ton_kho.lay_du_lieu_gia_tri_kho(
            kho_data.get("tonKho", []),
            hang_data.get("sanPham", []),
        )

    def tinh_tong_tien(self, ten_file):
        data = doc_json(ten_file, [])
        return tinh_admin.tinh_tong_tien_tu_danh_sach(data)

    def tinh_tong_so_luong_ton(self):
        data = self.lay_du_lieu_ton_kho_day_du()
        return tinh_admin.tinh_tong_so_luong_ton(data)

    def tinh_gia_tri_ton_kho(self):
        data = self.lay_du_lieu_gia_tri_kho()
        return tinh_admin.tinh_gia_tri_ton_kho(data)

    def dinh_dang_du_lieu_tong_quan(self, data):
        ket_qua = []

        for item in data:
            dong = dict(item)

            if dong.get("giaTri", "") != "-":
                dong["giaTri"] = self.dinh_dang_tien_admin(dong.get("giaTri", 0))

            ket_qua.append(dong)

        return ket_qua

    def lay_doanh_thu_theo_kho(self):
        data = doc_json("phieu_xuat.json", [])
        kho_data = doc_json("kho_hang.json", {})
        return tinh_admin.lay_doanh_thu_theo_kho(data, kho_data.get("kho", []))

    def dinh_dang_doanh_thu_kho(self, data):
        ket_qua = []

        for item in data:
            dong = dict(item)
            dong["tongDoanhThu"] = self.dinh_dang_tien_admin(dong.get("tongDoanhThu", 0))
            ket_qua.append(dong)

        return ket_qua

    def lay_top_5_theo_tien(self, danh_sach, truong_ma):
        return tinh_admin.lay_top_5_theo_tien(danh_sach, truong_ma)

    def lay_thong_ke_theo_thang(self, danh_sach, truong_ngay):
        return tinh_admin.lay_thong_ke_theo_thang(danh_sach, truong_ngay)

    def lay_top_5_ton_kho(self):
        data = self.lay_du_lieu_ton_kho_day_du()
        return tinh_admin.lay_top_5_ton_kho(data)

    def lay_top_5_canh_bao_ton_thap(self):
        data = self.lay_canh_bao_ton_thap()
        return tinh_admin.lay_top_5_canh_bao_ton_thap(data)

    def lay_phieu_gan_day(self, ten_file, truong_ma, truong_ngay):
        data = doc_json(ten_file, [])
        return tinh_admin.lay_phieu_gan_day(data, truong_ma, truong_ngay)

    # =========================
    # ĐĂNG XUẤT
    # =========================
    def dang_xuat(self):
        hoi = messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất không?")

        if hoi:
            self.root.destroy()

            from GUI.Login.login import hien_thi_login
            hien_thi_login()


def hien_thi_admin(tai_khoan_dang_nhap=None):
    app = GiaoDienAdmin(tai_khoan_dang_nhap)
    app.chay()


if __name__ == "__main__":
    hien_thi_admin()
