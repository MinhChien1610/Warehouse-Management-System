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
        # Lấy màu từ file mẫu, giữ nguyên layout file admin
        self.mau_nen = "#F8F5F3"

        self.mau_sidebar = "#B98E7C"
        self.mau_sidebar_dam = "#9F725F"
        self.mau_sidebar_nhat = "#F6EEEA"

        self.mau_menu = "#AD806D"
        self.mau_menu_hover = "#9F725F"
        self.mau_menu_con = "#F1E3DB"
        self.mau_menu_chon = "#AD806D"

        self.mau_card = "#FFFFFF"
        self.mau_card_nhe = "#FBF7F5"
        self.mau_vien = "#E8D8D0"

        self.mau_chu_dam = "#3F241B"
        self.mau_chu_phu = "#8D6F63"

        self.mau_them = "#10B981"
        self.mau_sua = "#AD806D"
        self.mau_xoa = "#EF4444"
        self.mau_thoat = "#9F725F"
        self.mau_tim_kiem = "#AD806D"

        self.mau_canh_bao = "#F59E0B"
        self.mau_thanh_cong = "#10B981"
        self.mau_nguy_hiem = "#DC2626"

        # Giữ tên biến cũ để các hàm trong layout không lỗi
        self.mau_blue_nhe = "#F6EEEA"
        self.mau_blue_vien = "#E8D8D0"
        self.mau_blue_sang = "#D3AC9B"

        self.mau_teal_nhe = self.mau_blue_nhe
        self.mau_teal_vien = self.mau_blue_vien
        self.mau_teal_sang = self.mau_blue_sang

        self.mau_xanh_nhe = self.mau_blue_nhe
        self.mau_xanh_vien = self.mau_blue_vien

    def cau_hinh_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=40,
            background="white",
            fieldbackground="white",
            foreground=self.mau_chu_dam,
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#F6EEEA",
            foreground=self.mau_chu_dam,
            padding=9,
            relief="flat",
        )

        style.map(
            "Treeview",
            background=[("selected", "#E8D8D0")],
            foreground=[("selected", self.mau_chu_dam)],
        )

        style.configure(
            "Vertical.TScrollbar",
            background="#D3AC9B",
            troughcolor="#F8F5F3",
            bordercolor="#F8F5F3",
            arrowcolor=self.mau_chu_dam,
        )

        style.configure(
            "Horizontal.TScrollbar",
            background="#D3AC9B",
            troughcolor="#F8F5F3",
            bordercolor="#F8F5F3",
            arrowcolor=self.mau_chu_dam,
        )

        style.configure(
            "TNotebook",
            background=self.mau_nen,
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            background=self.mau_card_nhe,
            foreground=self.mau_chu_dam,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", self.mau_menu)],
            foreground=[("selected", "white")],
        )

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
            bg="#FFFFFF",
            width=46,
            height=46,
            highlightbackground="#D3AC9B",
            highlightthickness=1,
        )
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)

        tk.Label(
            icon_box,
            text="📦",
            bg="#FFFFFF",
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
            fg="#F6EEEA",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")

        slogan = tk.Frame(
            logo,
            bg="#A97C69",
            highlightbackground="#D3AC9B",
            highlightthickness=1,
        )
        slogan.pack(fill="x", pady=(12, 0))

        tk.Label(
            slogan,
            text="Quản trị kho hàng",
            bg="#A97C69",
            fg="white",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=10, pady=(7, 1))

        tk.Label(
            slogan,
            text="Theo dõi • Báo cáo",
            bg="#A97C69",
            fg="#F6EEEA",
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
                ("Thống kê tồn kho", self.hien_thong_ke_ton_kho),
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
            pady=8,
            cursor="hand2",
            relief="flat",
        )

        button.config(command=lambda: self.chon_menu(button, command))
        button.pack(fill="x", pady=(0, 7))

        self.danh_sach_menu.append(button)
        return button


    def tao_menu_xo_sidebar(self, parent, title, danh_sach_con):
        khung = tk.Frame(parent, bg=self.mau_sidebar)
        khung.pack(fill="x", pady=(0, 7))

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
            font=("Segoe UI", 9, "bold"),
            bd=0,
            anchor="w",
            padx=14,
            pady=8,
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
                fg="#E8D8D0",
                activebackground=self.mau_menu_hover,
                activeforeground="white",
                font=("Segoe UI", 8),
                bd=0,
                anchor="w",
                padx=14,
                pady=4,
                cursor="hand2",
                relief="flat",
            )
            nut_con.config(command=lambda btn=nut_con, cmd=command: self.chon_menu(btn, cmd))
            nut_con.pack(fill="x", pady=(1, 1))
            self.danh_sach_menu.append(nut_con)


    def chon_menu(self, button, command):
        for nut in self.danh_sach_menu:
            text = str(nut.cget("text"))

            if text.startswith("      "):
                nut.config(bg=self.mau_sidebar, fg="#E8D8D0")
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
        return self.nghiep_vu_admin.lay_ten_admin_hien_tai()





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

        user_box.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        icon_box.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        text_box.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        name.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        role.bind("<Button-1>", lambda event: self.hien_tai_khoan())

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
        card.config(height=122)

        if column is None:
            column = len(parent.grid_slaves(row=0))

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
        value_label.pack(anchor="w", padx=14, pady=(7, 0))

        desc_label = self.tao_label(
            card,
            desc,
            8,
            self.mau_chu_phu,
            False,
            self.mau_card,
        )
        desc_label.config(wraplength=210, justify="left")
        desc_label.pack(anchor="w", padx=14, pady=(1, 10))

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
        bg = "#FFF7ED" if canh_bao else self.mau_card_nhe
        border = "#F59E0B" if canh_bao else self.mau_vien
        value_color = "#DC2626" if canh_bao else self.mau_menu_chon

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

        fg_right = "#DC2626" if canh_bao else self.mau_chu_phu

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
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
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
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
            ],
            [
                {"text": "Khóa/Mở tài khoản", "command": self.khoa_mo_tai_khoan, "color": self.mau_sidebar},
                {"text": "Reset mật khẩu", "command": self.reset_mat_khau_tai_khoan, "color": "#475569"},
            ],
        )

    def hien_kho(self):
        data = doc_json("kho_hang.json", {})
        danh_sach = data.get("kho", [])

        self.hien_bang_du_lieu(
            "Danh sách kho",
            "Quản lý thông tin kho hàng",
            ("maKho", "tenKho", "diaDiem", "soDienThoai"),
            ("Mã kho", "Tên kho", "Địa điểm", "Số điện thoại"),
            (120, 260, 420, 160),
            danh_sach,
            ["maKho", "tenKho", "diaDiem", "soDienThoai"],
            "Nhập mã kho, tên kho hoặc địa điểm...",
            [
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_du_lieu, "color": self.mau_xoa},
            ],
        )

    def hien_nhap_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(doc_json("phieu_nhap.json", []), "nhap")

        self.hien_bang_du_lieu(
            "Nhập kho",
            "Quản lý phiếu nhập kho",
            ("maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"),
            ("Mã phiếu", "Nhà sản xuất", "Kho", "Ngày nhập", "Tổng tiền", "Trạng thái"),
            (130, 160, 100, 140, 160, 130),
            data,
            ["maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"],
            "Nhập mã phiếu, nhà sản xuất hoặc kho...",
            [
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_du_lieu, "color": self.mau_xoa},
            ],
        )

    def hien_xuat_kho(self):
        data = self.chuan_hoa_trang_thai_phieu(doc_json("phieu_xuat.json", []), "xuat")

        self.hien_bang_du_lieu(
            "Xuất kho",
            "Quản lý phiếu xuất kho",
            ("maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"),
            ("Mã phiếu", "Kho", "Khách hàng", "Ngày xuất", "Tổng tiền", "Trạng thái"),
            (130, 100, 160, 140, 160, 130),
            data,
            ["maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"],
            "Nhập mã phiếu, khách hàng hoặc kho...",
            [
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_du_lieu, "color": self.mau_xoa},
            ],
        )

    def hien_ton_kho(self):
        data = self.lay_du_lieu_ton_kho_day_du()

        self.hien_bang_du_lieu(
            "Tồn kho",
            "Theo dõi số lượng hàng tồn trong kho",
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThai", "viTriHang"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Tồn", "Tồn tối thiểu", "Trạng thái", "Vị trí hàng"),
            (90, 105, 270, 80, 115, 120, 130),
            data,
            ["maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThai", "viTriHang"],
            "Nhập mã kho, mã sản phẩm, tên sản phẩm, vị trí hoặc trạng thái...",
        )

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
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Hủy", "command": self.huy_phieu_kiem_kho, "color": self.mau_xoa},
            ],
        )

    def hien_hang_hoa(self):
        data = doc_json("hang_hoa.json", {})
        danh_sach = self.chuan_hoa_trang_thai_san_pham(data.get("sanPham", []))

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
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
            ],
            [
                {"text": "Cập nhật trạng thái", "command": self.cap_nhat_trang_thai_hang_hoa, "color": self.mau_sidebar},
            ],
        )

    def hien_loai_hang(self):
        data = doc_json("hang_hoa.json", {})
        danh_sach = data.get("loaiHang", [])

        self.hien_bang_du_lieu(
            "Loại hàng",
            "Quản lý nhóm loại hàng hóa",
            ("maLoaiHang", "tenLoaiHang", "ghiChu"),
            ("Mã loại", "Tên loại hàng", "Ghi chú"),
            (130, 300, 420),
            danh_sach,
            ["maLoaiHang", "tenLoaiHang", "ghiChu"],
            "Nhập mã loại, tên loại hoặc ghi chú...",
            [
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_du_lieu, "color": self.mau_xoa},
            ],
        )

    def hien_nha_san_xuat(self):
        data = doc_json("doi_tac.json", {})
        danh_sach = data.get("nhaSanXuat", [])

        self.hien_bang_du_lieu(
            "Nhà sản xuất",
            "Quản lý thông tin nhà sản xuất",
            ("maNhaSanXuat", "tenNhaSanXuat", "soDienThoai", "email", "diaChi"),
            ("Mã NSX", "Tên nhà sản xuất", "Số điện thoại", "Email", "Địa chỉ"),
            (120, 250, 150, 220, 280),
            danh_sach,
            ["maNhaSanXuat", "tenNhaSanXuat", "soDienThoai", "email", "diaChi"],
            "Nhập mã, tên, số điện thoại hoặc email...",
            [
                {"text": "Thêm", "command": self.them_du_lieu, "color": self.mau_them},
                {"text": "Sửa", "command": self.sua_du_lieu, "color": self.mau_sua},
                {"text": "Xóa", "command": self.xoa_du_lieu, "color": self.mau_xoa},
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
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        chart_card = self.tao_card(main)
        chart_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        top_card = self.tao_card(main)
        top_card.grid(row=0, column=1, sticky="nsew", pady=(0, 10))

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
        ).pack(anchor="w", padx=16, pady=(14, 8))

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
        row.pack(fill="x", padx=14, pady=(0, 7))

        self.tao_label(
            row,
            ma_phieu,
            10,
            self.mau_chu_dam,
            True,
            self.mau_card_nhe,
        ).pack(side="left", padx=12, pady=9)

        self.tao_label(
            row,
            gia_tri,
            10,
            self.mau_menu,
            True,
            self.mau_card_nhe,
        ).pack(side="right", padx=12, pady=9)

    def hien_thong_ke_ton_kho(self):
        data = self.lay_du_lieu_ton_kho_day_du()
        du_lieu_top = self.lay_top_5_ton_kho()

        self.tao_tieu_de_trang(
            self.content,
            "Thống kê tồn kho",
            "Top 5 sản phẩm có số lượng tồn cao nhất",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        self.hien_thong_ke_bang_bieu_do_don(
            body,
            data,
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThai", "viTriHang"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Tồn", "Tồn tối thiểu", "Trạng thái", "Vị trí"),
            (85, 95, 220, 80, 110, 115, 120),
            ["maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "trangThai", "viTriHang"],
            du_lieu_top,
            "Top 5 sản phẩm tồn nhiều nhất",
        )

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
            ("maKho", "soPhieu", "tongDoanhThu"),
            ("Mã kho", "Số phiếu xuất", "Doanh thu"),
            (130, 130, 180),
            ["maKho", "soPhieu", "tongDoanhThu"],
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

    # =========================
    # NHẬT KÝ
    # =========================
    def hien_nhat_ky_dang_nhap(self):
        data = self.chuan_hoa_trang_thai(doc_json("nhat_ky.json", []))
        ket_qua = []

        for item in data:
            hanh_dong = str(item.get("hanhDong", item.get("hanh_dong", ""))).lower()

            if "đăng nhập" in hanh_dong or "đăng xuất" in hanh_dong:
                ket_qua.append(item)

        self.hien_bang_du_lieu(
            "Nhật ký đăng nhập",
            "Theo dõi lịch sử đăng nhập và đăng xuất",
            ("maNhatKy", "maTaiKhoan", "hanhDong", "thoiGian", "trangThai"),
            ("Mã", "Tài khoản", "Hành động", "Thời gian", "Trạng thái"),
            (90, 130, 250, 220, 150),
            ket_qua,
            ["maNhatKy", "maTaiKhoan", "hanhDong", "thoiGian", "trangThai"],
            "Nhập tài khoản, hành động hoặc thời gian...",
        )

    def hien_nhat_ky_thao_tac(self):
        data = self.chuan_hoa_trang_thai(doc_json("nhat_ky.json", []))

        self.tao_tieu_de_trang(
            self.content,
            "Nhật ký thao tác",
            "Theo dõi thao tác thêm, sửa, xóa, khóa/mở khóa và reset mật khẩu",
        )

        body = self.tao_khung_noi_dung(self.content)

        header = tk.Frame(body, bg=self.mau_card)
        header.pack(fill="x", pady=(0, 12))

        self.tao_label(
            header,
            "Tổng số bản ghi: " + str(len(data)),
            11,
            self.mau_chu_phu,
            False,
            self.mau_card,
        ).pack(side="left", padx=(4, 0))

        filter_bar = tk.Frame(body, bg=self.mau_card)
        filter_bar.pack(fill="x", pady=(0, 12))

        cbo_loai = ttk.Combobox(
            filter_bar,
            values=["Tất cả", "Thêm", "Sửa", "Xóa", "Khóa/Mở khóa", "Reset mật khẩu", "Đăng nhập", "Đăng xuất"],
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

            ket_qua = self.loc_nhat_ky_thao_tac(data, loai, tu_ngay, den_ngay, tu_khoa)

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
            "#475569",
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

    def thong_bao_chua_lam(self):
        messagebox.showinfo(
            "Thông báo",
            "Chức năng này sẽ được xử lý ở phần nghiệp vụ CRUD.",
        )

    def them_du_lieu(self):
        self.thong_bao_chua_lam()

    def sua_du_lieu(self):
        self.thong_bao_chua_lam()

    def xoa_du_lieu(self):
        self.thong_bao_chua_lam()

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

        hoi = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn hủy phiếu kiểm kho " + ma_kiem_ke + " không?",
        )

        if not hoi:
            return

        data = doc_json("kiem_ke.json", [])
        da_tim_thay = False

        for item in data:
            if item.get("maKiemKe") == ma_kiem_ke:
                item["trangThai"] = "Đã hủy"
                da_tim_thay = True
                break

        if not da_tim_thay:
            messagebox.showerror("Lỗi", "Không tìm thấy phiếu kiểm kho đã chọn.")
            return

        ghi_json("kiem_ke.json", data)

        messagebox.showinfo("Thành công", "Đã hủy phiếu kiểm kho.")
        self.hien_kiem_kho()

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

        if tu_ngay != "" and den_ngay != "" and tu_ngay > den_ngay:
            messagebox.showerror(
                "Lỗi!",
                "Vui lòng chọn lại ngày cần lọc!"
            )
            return []

        for item in danh_sach:
            hanh_dong = str(item.get("hanhDong", "")).lower()
            thoi_gian = str(item.get("thoiGian", ""))
            noi_dung = " ".join(str(item.get(key, "")) for key in ["maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai", "ghiChu"]).lower()

            if loai != "Tất cả":
                if loai == "Khóa/Mở khóa":
                    if "khóa" not in hanh_dong and "mở" not in hanh_dong:
                        continue
                elif loai == "Reset mật khẩu":
                    if "reset" not in hanh_dong:
                        continue
                else:
                    if loai.lower() not in hanh_dong:
                        continue

            ngay_so_sanh = self.chuan_hoa_ngay_loc(thoi_gian)

            if tu_ngay != "" and ngay_so_sanh != "" and ngay_so_sanh < tu_ngay:
                continue

            if den_ngay != "" and ngay_so_sanh != "" and ngay_so_sanh > den_ngay:
                continue

            if tu_khoa != "" and tu_khoa not in noi_dung:
                continue

            ket_qua.append(item)

        return ket_qua

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
        return tinh_admin.dinh_dang_danh_sach_phieu(danh_sach)

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
        return tinh_admin.dinh_dang_du_lieu_tong_quan(data)

    def lay_doanh_thu_theo_kho(self):
        data = doc_json("phieu_xuat.json", [])
        return tinh_admin.lay_doanh_thu_theo_kho(data)

    def dinh_dang_doanh_thu_kho(self, data):
        return tinh_admin.dinh_dang_doanh_thu_kho(data)

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
