import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Calculator.tonkho import lay_canh_bao_ton_thap
from GUI.Common.base import GiaoDienCoSo
from GUI.Login.login import hien_thi_login
from CRUD.NhanVienKho.nhanvienkho import NghiepVuNhanVienKho


# =========================
# XỬ LÝ FILE JSON
# =========================
def lay_thu_muc_goc():
    return GiaoDienCoSo.lay_thu_muc_goc()


def doc_json(ten_file, mac_dinh=None):
    return GiaoDienCoSo.doc_json(ten_file, mac_dinh)


def ghi_json(ten_file, data):
    GiaoDienCoSo.ghi_json(ten_file, data)


# =========================
# GIAO DIỆN NHÂN VIÊN KHO
# =========================
class GiaoDienNhanVienKho(GiaoDienCoSo):
    def __init__(self, tai_khoan_dang_nhap=None):
        super().__init__()
        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap or {}

        self.root = tk.Tk()
        self.root.title("Nhân viên kho")
        self.root.geometry("1500x850")
        self.root.minsize(1250, 720)
        self.root.configure(bg=self.mau_nen)

        self.danh_sach_menu = []
        self.notebook_kho = None
        self.toolbar_kho_area = None
        self.vung_bang_kho = None
        self.man_hinh_kho_hien_tai = "Danh sách kho"
        self.man_hinh_thong_ke_hien_tai = "Tổng quan kho"
        self.nghiep_vu_kho = NghiepVuNhanVienKho(
            lay_thu_muc_goc(),
            self.tai_khoan_dang_nhap.get("maTaiKhoan", None),
        )

        self.cau_hinh_style()
        self.tao_bo_cuc_chinh()
        self.tao_sidebar()
        self.hien_trang_chu()

    def chay(self):
        self.root.mainloop()

    # =========================
    # BỐ CỤC CHÍNH
    # =========================
    def tao_bo_cuc_chinh(self):
        self.sidebar = tk.Frame(self.root, bg=self.mau_sidebar, width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg=self.mau_nen)
        self.content.pack(side="right", fill="both", expand=True)

    def tao_sidebar(self):
        logo = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        logo.pack(fill="x", pady=(28, 14))

        self.tao_label(
            logo, "QUẢN LÝ\nKHO HÀNG", 22, "white", True, self.mau_sidebar
        ).pack()

        self.tao_label(
            logo, "Warehouse Management", 10, "#F8F0EC", False, self.mau_sidebar
        ).pack(pady=(6, 0))

        vung_menu = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        vung_menu.pack(fill="both", expand=True, padx=10)

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
        menu_window = canvas_menu.create_window(
            (0, 0),
            window=menu,
            anchor="nw",
        )

        def cap_nhat_vung_cuon(event=None):
            canvas_menu.configure(scrollregion=canvas_menu.bbox("all"))
            canvas_menu.itemconfigure(menu_window, width=canvas_menu.winfo_width())

        def cuon_menu(event):
            canvas_menu.yview_scroll(int(-1 * (event.delta / 120)), "units")

        menu.bind("<Configure>", cap_nhat_vung_cuon)
        canvas_menu.bind("<Configure>", cap_nhat_vung_cuon)
        canvas_menu.bind_all("<MouseWheel>", cuon_menu)

        self.tao_nut_menu(menu, "Trang chủ", self.hien_trang_chu)

        self.tao_menu_xo_sidebar(
            menu,
            "Kho hàng",
            [
                ("Danh sách kho", self.hien_danh_sach_kho),
                ("Nhập kho", self.hien_phieu_nhap),
                ("Xuất kho", self.hien_phieu_xuat),
                ("Tồn kho", self.hien_ton_kho),
                ("Kiểm kho", self.hien_kiem_kho),
            ],
        )

        self.tao_nut_menu(menu, "Hàng hóa", self.hien_hang_hoa)
        self.tao_nut_menu(menu, "Lịch sử", self.hien_lich_su)

        self.tao_menu_xo_sidebar(
            menu,
            "Thống kê",
            [
                ("Tổng quan kho", self.hien_thong_ke_tong_quan),
                ("Tồn kho theo kho", self.hien_thong_ke_ton_kho),
                ("Nhập theo ngày", self.hien_thong_ke_nhap_ngay),
                ("Xuất theo ngày", self.hien_thong_ke_xuat_ngay),
                ("Cảnh báo tồn thấp", self.hien_thong_ke_canh_bao),
            ],
        )

        self.tao_menu_xo_sidebar(
            menu,
            "Tài khoản",
            [
                ("Thông tin tài khoản", self.hien_tai_khoan),
                ("Đổi mật khẩu", self.hien_doi_mat_khau),
            ],
        )

        self.tao_nut(
            self.sidebar, "Đăng xuất", self.dang_xuat, "#956A58"
        ).pack(side="bottom", fill="x", padx=18, pady=20)

    def tao_nut_menu(self, parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            bg=self.mau_menu,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            anchor="w",
            padx=22,
            pady=15,
            cursor="hand2",
        )

        button.config(command=lambda: self.chon_menu(button, command))
        button.pack(fill="x", pady=(0, 14))
        self.danh_sach_menu.append(button)
        return button

    def tao_menu_xo_sidebar(self, parent, title, danh_sach_con):
        khung = tk.Frame(parent, bg=self.mau_sidebar)
        khung.pack(fill="x", pady=(0, 14))

        khung_con = tk.Frame(khung, bg="#C49B8A")
        dang_mo = {"value": False}

        def toggle_menu():
            if dang_mo["value"]:
                khung_con.pack_forget()
                dang_mo["value"] = False
                nut_cha.config(text=title + "  ▾")
            else:
                khung_con.pack(fill="x", pady=(8, 0))
                dang_mo["value"] = True
                nut_cha.config(text=title + "  ▴")

        nut_cha = tk.Button(
            khung,
            text=title + "  ▾",
            bg=self.mau_menu,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            anchor="w",
            padx=22,
            pady=15,
            cursor="hand2",
            command=toggle_menu,
        )
        nut_cha.pack(fill="x")
        self.danh_sach_menu.append(nut_cha)

        for text, command in danh_sach_con:
            nut_con = tk.Button(
                khung_con,
                text="• " + text,
                bg="#C49B8A",
                fg="white",
                activebackground="#D3AC9B",
                activeforeground="white",
                font=("Segoe UI", 11),
                bd=0,
                anchor="w",
                padx=30,
                pady=9,
                cursor="hand2",
                command=command,
            )
            nut_con.pack(fill="x", pady=1)
            self.danh_sach_menu.append(nut_con)

    def chon_menu(self, button, command):
        for nut in self.danh_sach_menu:
            nut.config(bg=self.mau_menu, fg="white")

        button.config(bg="white", fg=self.mau_chu_dam)
        command()

    # =========================
    # TRANG CHỦ
    # =========================
    def hien_trang_chu(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang_chu()
        header.pack(fill="x", padx=28, pady=(24, 12))

        body = self.tao_khung_noi_dung(self.content)

        card_row = tk.Frame(body, bg=self.mau_card)
        card_row.pack(fill="x", pady=(0, 18))

        self.tao_the_tong_quan(
            card_row, "Kho hàng", self.dem_so_kho(),
            "Số kho đang hoạt động", self.hien_kho
        )

        self.tao_the_tong_quan(
            card_row, "Hàng hóa", self.dem_so_hang_hoa(),
            "Sản phẩm đang quản lí", self.hien_hang_hoa
        )

        self.tao_the_tong_quan(
            card_row, "Tồn kho", self.tinh_tong_ton_kho(),
            "Tổng số lượng tồn", self.hien_ton_kho
        )

        self.tao_noi_dung_trang_chu(body)

    def tao_header_trang_chu(self):
        header = tk.Frame(self.content, bg=self.mau_nen)

        left_header = tk.Frame(header, bg=self.mau_nen)
        left_header.pack(side="left")

        self.tao_label(
            left_header, "Trang chủ", 30, self.mau_chu_dam, True, self.mau_nen
        ).pack(anchor="w")

        self.tao_label(
            left_header,
            "Tổng quan hệ thống quản lí kho hàng",
            13,
            self.mau_chu_phu,
            False,
            self.mau_nen,
        ).pack(anchor="w", pady=(6, 0))

        self.tao_user_box(header).pack(side="right", pady=(6, 0))
        return header

    def tao_user_box(self, parent):
        user_box = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            cursor="hand2",
        )

        icon = tk.Label(
            user_box,
            text="👤",
            bg=self.mau_card_nhe,
            fg=self.mau_menu,
            font=("Segoe UI", 14),
            cursor="hand2",
        )
        icon.pack(side="left", padx=(14, 8), pady=8)

        name = tk.Label(
            user_box,
            text="Xin chào, Nhân viên kho",
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        name.pack(side="left", padx=(0, 14), pady=8)

        user_box.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        icon.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        name.bind("<Button-1>", lambda event: self.hien_tai_khoan())

        return user_box

    def tao_noi_dung_trang_chu(self, body):
        bottom = tk.Frame(body, bg=self.mau_card)
        bottom.pack(fill="both", expand=True)

        left = self.tao_card(bottom)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = self.tao_card(bottom)
        right.pack(side="right", fill="y", ipadx=20)

        self.tao_label(
            left, "Tổng quan hệ thống", 20, self.mau_chu_dam, True
        ).pack(anchor="w", padx=22, pady=(22, 10))

        mo_ta = (
            "Đây là khu vực mặc định khi nhân viên kho đăng nhập.\n\n"
            "Có thể bấm vào các thẻ phía trên để đi nhanh tới Kho hàng, "
            "Hàng hóa hoặc Tồn kho."
        )

        label = self.tao_label(left, mo_ta, 12, self.mau_chu_phu)
        label.config(wraplength=650)
        label.pack(anchor="w", padx=22)

        self.tao_label(
            right, "Thông báo", 18, self.mau_chu_dam, True
        ).pack(anchor="w", padx=18, pady=(18, 12))

        self.tao_thong_bao(right, "Kiểm tra tồn kho định kỳ.")
        self.tao_thong_bao(right, "Cập nhật phiếu nhập và phiếu xuất đầy đủ.")
        self.tao_thong_bao(right, "Theo dõi lịch sử thao tác người dùng.")

    def tao_the_tong_quan(self, parent, title, value, desc, command=None):
        card = self.tao_card(parent)
        card.pack(side="left", fill="both", expand=True, padx=8)

        self.tao_label(card, title, 13, self.mau_chu_dam, True).pack(
            anchor="w", padx=18, pady=(18, 6)
        )

        self.tao_label(card, str(value), 30, self.mau_menu, True).pack(
            anchor="w", padx=18
        )

        self.tao_label(card, desc, 11, self.mau_chu_phu).pack(
            anchor="w", padx=18, pady=(4, 18)
        )

        if command is not None:
            self.gan_su_kien_click(card, command)

    def tao_thong_bao(self, parent, text):
        item = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        item.pack(fill="x", padx=18, pady=(0, 10))

        self.tao_label(
            item, "• " + text, 11, self.mau_chu_phu, False, self.mau_card_nhe
        ).pack(anchor="w", padx=14, pady=14)

    # =========================
    # KHO HÀNG
    # =========================
    def hien_kho(self):
        self.tao_tieu_de_trang(
            self.content,
            self.man_hinh_kho_hien_tai,
            "Quản lý danh sách kho, nhập kho, xuất kho, tồn kho và kiểm kho",
        )

        body = self.tao_khung_noi_dung(self.content)

        self.toolbar_kho_area = tk.Frame(body, bg=self.mau_card)
        self.toolbar_kho_area.pack(fill="x")

        self.tao_nut_thoat(body)

        self.vung_bang_kho = tk.Frame(body, bg=self.mau_card)
        self.vung_bang_kho.pack(fill="both", expand=True)

        self.chuyen_man_hinh_kho()

    def hien_danh_sach_kho(self):
        self.man_hinh_kho_hien_tai = "Danh sách kho"
        self.hien_kho()

    def hien_phieu_nhap(self):
        self.man_hinh_kho_hien_tai = "Nhập kho"
        self.hien_kho()

    def hien_phieu_xuat(self):
        self.man_hinh_kho_hien_tai = "Xuất kho"
        self.hien_kho()

    def hien_kiem_kho(self):
        self.man_hinh_kho_hien_tai = "Kiểm kho"
        self.hien_kho()

    def chuyen_man_hinh_kho(self, event=None):
        if not hasattr(self, "vung_bang_kho"):
            return

        self.xoa_noi_dung(self.vung_bang_kho)

        man_hinh = self.man_hinh_kho_hien_tai

        if man_hinh == "Danh sách kho":
            self.hien_bang_danh_sach_kho()
        elif man_hinh == "Nhập kho":
            self.hien_bang_phieu_nhap()
        elif man_hinh == "Xuất kho":
            self.hien_bang_phieu_xuat()
        elif man_hinh == "Tồn kho":
            self.hien_bang_ton_kho()
        elif man_hinh == "Kiểm kho":
            self.hien_bang_kiem_kho()

        self.cap_nhat_thanh_cong_cu_kho()

    def hien_bang_danh_sach_kho(self):
        self.bang_kho = self.tao_bang(
            self.vung_bang_kho,
            ("maKho", "tenKho", "diaDiem", "soDienThoai"),
            ("Mã kho", "Tên kho", "Địa điểm", "Số điện thoại"),
            (130, 260, 430, 180),
        )
        self.load_kho("")

    def hien_bang_phieu_nhap(self):
        self.bang_phieu_nhap = self.tao_bang(
            self.vung_bang_kho,
            ("maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"),
            ("Mã phiếu", "Nhà sản xuất", "Kho", "Ngày nhập", "Tổng tiền", "Trạng thái"),
            (130, 160, 100, 150, 180, 140),
        )
        self.load_phieu_nhap("")

    def hien_bang_phieu_xuat(self):
        self.bang_phieu_xuat = self.tao_bang(
            self.vung_bang_kho,
            ("maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"),
            ("Mã phiếu", "Kho", "Khách hàng", "Ngày xuất", "Tổng tiền", "Trạng thái"),
            (130, 100, 160, 150, 180, 140),
        )
        self.load_phieu_xuat("")

    def hien_bang_ton_kho(self):
        self.bang_ton_kho = self.tao_bang(
            self.vung_bang_kho,
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "maViTri"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Số lượng tồn", "Vị trí"),
            (120, 120, 420, 160, 150),
        )
        self.load_ton_kho("")

    def hien_bang_kiem_kho(self):
        self.bang_kiem_kho = self.tao_bang(
            self.vung_bang_kho,
            ("maKiemKe", "maKho", "ngayKiemKe", "ghiChu"),
            ("Mã kiểm kê", "Mã kho", "Ngày kiểm kê", "Ghi chú"),
            (140, 120, 160, 520),
        )
        self.load_kiem_kho("")

    def cap_nhat_thanh_cong_cu_kho(self, event=None):
        if self.toolbar_kho_area is None:
            return

        self.xoa_noi_dung(self.toolbar_kho_area)
        tab = self.lay_tab_kho_hien_tai()

        if tab == 0:
            self.tao_thanh_cong_cu(
                self.toolbar_kho_area,
                "Nhập mã kho, tên kho hoặc địa điểm cần tìm...",
                self.tim_kiem_kho,
                buttons=[],
            )
        elif tab == 1:
            self.tao_thanh_cong_cu(
                self.toolbar_kho_area,
                "Nhập mã phiếu nhập, nhà sản xuất hoặc kho cần tìm...",
                self.tim_kiem_phieu_nhap,
                buttons=[
                    {"text": "Thêm", "command": lambda: self.mo_form_nhap_xuat_kho("nhap"), "color": "#7D9D8C"},
                    {"text": "Sửa", "command": self.sua_phieu_nhap_da_chon, "color": "#B98E7C"},
                    {"text": "Xóa", "command": self.xoa_phieu_nhap_luu_tam_da_chon, "color": "#B56B6B"},
                ],
            )
        elif tab == 2:
            self.tao_thanh_cong_cu(
                self.toolbar_kho_area,
                "Nhập mã phiếu xuất, khách hàng hoặc kho cần tìm...",
                self.tim_kiem_phieu_xuat,
                buttons=[
                    {"text": "Thêm", "command": lambda: self.mo_form_nhap_xuat_kho("xuat"), "color": "#7D9D8C"},
                    {"text": "Sửa", "command": self.sua_phieu_xuat_da_chon, "color": "#B98E7C"},
                    {"text": "Xóa", "command": self.xoa_phieu_xuat_luu_tam_da_chon, "color": "#B56B6B"},
                ],
            )
        elif tab == 3:
            self.tao_thanh_cong_cu(
                self.toolbar_kho_area,
                "Nhập mã kho, mã sản phẩm hoặc tên sản phẩm cần tìm...",
                self.tim_kiem_ton_kho,
                buttons=[],
            )
        elif tab == 4:
            self.tao_thanh_cong_cu(
                self.toolbar_kho_area,
                "Nhập mã kiểm kê, mã kho hoặc ghi chú cần tìm...",
                self.tim_kiem_kiem_kho,
                buttons=[
                    {"text": "Thêm", "command": self.mo_form_kiem_kho, "color": "#7D9D8C"},
                    {"text": "Sửa", "command": self.sua_kiem_ke_da_chon, "color": "#B98E7C"},
                ],
            )

    def hien_ton_kho(self):
        self.man_hinh_kho_hien_tai = "Tồn kho"
        self.hien_kho()

    def lay_tab_kho_hien_tai(self):
        if not hasattr(self, "man_hinh_kho_hien_tai"):
            return -1

        man_hinh = self.man_hinh_kho_hien_tai

        if man_hinh == "Danh sách kho":
            return 0
        if man_hinh == "Nhập kho":
            return 1
        if man_hinh == "Xuất kho":
            return 2
        if man_hinh == "Tồn kho":
            return 3
        if man_hinh == "Kiểm kho":
            return 4

        return -1

    def lam_moi_du_lieu_kho(self):
        if hasattr(self, "vung_bang_kho") and self.vung_bang_kho is not None:
            self.chuyen_man_hinh_kho()

    # =========================
    # LOAD / TÌM KIẾM KHO
    # =========================
    def load_kho(self, tu_khoa=""):
        data = doc_json("kho_hang.json", {})
        danh_sach = data.get("kho", [])

        ket_qua = self.loc_du_lieu(
            danh_sach,
            tu_khoa,
            ["maKho", "tenKho", "diaDiem", "soDienThoai"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_kho,
            ket_qua,
            ["maKho", "tenKho", "diaDiem", "soDienThoai"],
        )

    def tim_kiem_kho(self, tu_khoa):
        self.load_kho(tu_khoa)

    def load_phieu_nhap(self, tu_khoa=""):
        data = doc_json("phieu_nhap.json", [])
        ket_qua = self.loc_du_lieu(
            data,
            tu_khoa,
            ["maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_phieu_nhap,
            ket_qua,
            ["maPhieuNhap", "maNhaSanXuat", "maKho", "ngayNhap", "tongTien", "trangThai"],
        )

    def tim_kiem_phieu_nhap(self, tu_khoa):
        self.load_phieu_nhap(tu_khoa)

    def load_phieu_xuat(self, tu_khoa=""):
        data = doc_json("phieu_xuat.json", [])
        ket_qua = self.loc_du_lieu(
            data,
            tu_khoa,
            ["maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_phieu_xuat,
            ket_qua,
            ["maPhieuXuat", "maKho", "maKhachHang", "ngayXuat", "tongTien", "trangThai"],
        )

    def tim_kiem_phieu_xuat(self, tu_khoa):
        self.load_phieu_xuat(tu_khoa)

    def load_ton_kho(self, tu_khoa=""):
        kho_data = doc_json("kho_hang.json", {})
        hang_data = doc_json("hang_hoa.json", {})

        danh_sach_sp = hang_data.get("sanPham", [])
        danh_sach_ton = kho_data.get("tonKho", [])

        self.xoa_du_lieu_bang(self.bang_ton_kho)
        tu_khoa = tu_khoa.lower().strip()

        for ton in danh_sach_ton:
            ma_sp = ton.get("maSanPham", "")
            ten_sp = self.tim_ten_san_pham(danh_sach_sp, ma_sp)

            noi_dung = " ".join([
                str(ton.get("maKho", "")),
                str(ma_sp),
                str(ten_sp),
                str(ton.get("soLuongTon", "")),
                str(ton.get("maViTri", "")),
            ]).lower()

            if tu_khoa != "" and tu_khoa not in noi_dung:
                continue

            self.bang_ton_kho.insert(
                "",
                "end",
                values=(
                    ton.get("maKho", ""),
                    ma_sp,
                    ten_sp,
                    ton.get("soLuongTon", ""),
                    ton.get("maViTri", ""),
                ),
            )

    def tim_kiem_ton_kho(self, tu_khoa):
        self.load_ton_kho(tu_khoa)

    def load_kiem_kho(self, tu_khoa=""):
        data = doc_json("kiem_ke.json", [])
        ket_qua = self.loc_du_lieu(
            data,
            tu_khoa,
            ["maKiemKe", "maKho", "ngayKiemKe", "ghiChu"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_kiem_kho,
            ket_qua,
            ["maKiemKe", "maKho", "ngayKiemKe", "ghiChu"],
        )

    def tim_kiem_kiem_kho(self, tu_khoa):
        self.load_kiem_kho(tu_khoa)

    # =========================
    # HÀNG HÓA
    # =========================
    def hien_hang_hoa(self):
        self.tao_tieu_de_trang(
            self.content,
            "Hàng hóa",
            "Quản lý danh sách sản phẩm trong kho",
        )

        body = self.tao_khung_noi_dung(self.content)

        self.tao_thanh_cong_cu(
            body,
            "Nhập mã sản phẩm, tên sản phẩm hoặc loại hàng cần tìm...",
            self.tim_kiem_hang_hoa,
            buttons=[
                {"text": "Thêm", "command": self.them_hang_hoa, "color": "#7D9D8C"},
                {"text": "Sửa", "command": self.sua_hang_hoa, "color": "#B98E7C"},
                {"text": "Ngừng kinh doanh", "command": self.ngung_kinh_doanh_hang_hoa, "color": "#B56B6B"},
            ],
        )

        self.tao_nut_thoat(body)

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        self.bang_hang_hoa = self.tao_bang(
            table_area,
            ("maSanPham", "tenSanPham", "maLoaiHang", "donGia", "mucTonToiThieu", "trangThai"),
            ("Mã SP", "Tên sản phẩm", "Loại hàng", "Đơn giá", "Tồn tối thiểu", "Trạng thái"),
            (120, 350, 130, 150, 130, 170),
        )

        self.load_hang_hoa("")

    def load_hang_hoa(self, tu_khoa=""):
        data = doc_json("hang_hoa.json", {})
        danh_sach = []

        for san_pham in data.get("sanPham", []):
            dong = dict(san_pham)
            if dong.get("trangThai", "") == "":
                dong["trangThai"] = "Đang kinh doanh"
            danh_sach.append(dong)

        ket_qua = self.loc_du_lieu(
            danh_sach,
            tu_khoa,
            ["maSanPham", "tenSanPham", "maLoaiHang", "donGia", "trangThai"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_hang_hoa,
            ket_qua,
            ["maSanPham", "tenSanPham", "maLoaiHang", "donGia", "mucTonToiThieu", "trangThai"],
        )

    def tim_kiem_hang_hoa(self, tu_khoa):
        self.load_hang_hoa(tu_khoa)

    def them_hang_hoa(self):
        self.mo_form_hang_hoa()

    def sua_hang_hoa(self):
        ma_san_pham = self.lay_ma_dong_dang_chon(self.bang_hang_hoa)

        if ma_san_pham == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sản phẩm cần sửa.")
            return

        san_pham = self.nghiep_vu_kho.tim_san_pham(ma_san_pham)

        if san_pham is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm đã chọn.")
            return

        self.mo_form_hang_hoa(san_pham)

    def ngung_kinh_doanh_hang_hoa(self):
        ma_san_pham = self.lay_ma_dong_dang_chon(self.bang_hang_hoa)

        if ma_san_pham == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sản phẩm cần ngừng kinh doanh.")
            return

        hoi = messagebox.askyesno(
            "Xác nhận",
            "Chuyển sản phẩm " + ma_san_pham + " sang trạng thái Ngừng kinh doanh?"
        )

        if not hoi:
            return

        try:
            self.nghiep_vu_kho.ngung_kinh_doanh_san_pham(ma_san_pham)
            self.load_hang_hoa("")

            if hasattr(self, "bang_ton_kho"):
                self.load_ton_kho()

            messagebox.showinfo(
                "Thành công",
                "Đã chuyển sản phẩm sang trạng thái Ngừng kinh doanh."
            )
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def mo_form_hang_hoa(self, san_pham=None):
        la_sua = san_pham is not None
        hang_data = doc_json("hang_hoa.json", {})

        title = "Sửa sản phẩm" if la_sua else "Thêm sản phẩm"
        form = self.tao_cua_so_form(title, 540, 560)
        khung = form["body"]

        ten_entry = self.tao_entry_form(khung, "Tên sản phẩm")

        loai_cb = self.tao_combobox_form(
            khung,
            "Loại hàng",
            self.tao_danh_sach_chon(
                hang_data.get("loaiHang", []),
                "maLoaiHang",
                "tenLoaiHang"
            ),
        )

        dvt_cb = self.tao_combobox_form(
            khung,
            "Đơn vị tính",
            self.tao_danh_sach_chon(
                hang_data.get("donViTinh", []),
                "maDonViTinh",
                "tenDonViTinh"
            ),
        )

        don_gia_entry = self.tao_entry_form(khung, "Đơn giá")
        muc_ton_entry = self.tao_entry_form(khung, "Mức tồn tối thiểu")

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
                don_gia = int(self.chuyen_so(don_gia_entry.get()))
                muc_ton = int(self.chuyen_so(muc_ton_entry.get()))

                if ten == "":
                    raise ValueError("Vui lòng nhập tên sản phẩm.")
                if ma_loai == "" or ma_dvt == "":
                    raise ValueError("Vui lòng chọn loại hàng và đơn vị tính.")
                if don_gia <= 0:
                    raise ValueError("Đơn giá phải lớn hơn 0.")
                if muc_ton < 0:
                    raise ValueError("Mức tồn tối thiểu không được âm.")

                if la_sua:
                    self.nghiep_vu_kho.sua_san_pham(
                        san_pham.get("maSanPham", ""),
                        ten,
                        ma_loai,
                        ma_dvt,
                        don_gia,
                        muc_ton,
                    )
                else:
                    self.nghiep_vu_kho.tao_san_pham(
                        ten,
                        ma_loai,
                        ma_dvt,
                        don_gia,
                        muc_ton,
                    )

                form["window"].destroy()
                self.load_hang_hoa("")

                if hasattr(self, "bang_ton_kho"):
                    self.load_ton_kho()

                messagebox.showinfo("Thành công", "Đã lưu sản phẩm.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, "#7D9D8C").pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, "#6E554C").pack(side="right")

    # =========================
    # FORM NHẬP / XUẤT KHO NHIỀU SẢN PHẨM
    # =========================
    def mo_form_nhap_xuat_kho(self, loai, phieu=None):
        la_nhap = loai == "nhap"
        la_sua = phieu is not None

        if la_nhap:
            tieu_de = "Sửa phiếu nhập kho" if la_sua else "Tạo phiếu nhập kho"
            doi_tac_label = "Nhà sản xuất"
            doi_tac_list = self.nghiep_vu_kho.lay_danh_sach_nha_san_xuat()
            doi_tac_ma = "maNhaSanXuat"
            doi_tac_ten = "tenNhaSanXuat"
        else:
            tieu_de = "Sửa phiếu xuất kho" if la_sua else "Tạo phiếu xuất kho"
            doi_tac_label = "Khách hàng"
            doi_tac_list = self.nghiep_vu_kho.lay_danh_sach_khach_hang()
            doi_tac_ma = "maKhachHang"
            doi_tac_ten = "tenKhachHang"

        form = self.tao_cua_so_form(tieu_de, 760, 700)
        khung = form["body"]

        doi_tac_cb = self.tao_combobox_form(
            khung,
            doi_tac_label,
            self.tao_danh_sach_chon(doi_tac_list, doi_tac_ma, doi_tac_ten),
        )

        kho_cb = self.tao_combobox_form(
            khung,
            "Kho",
            self.tao_danh_sach_chon(
                self.nghiep_vu_kho.lay_danh_sach_kho(),
                "maKho",
                "tenKho",
            ),
        )

        so_dong_entry = self.tao_entry_form(khung, "Số lượng sản phẩm trong phiếu")

        khung_nut_dong = tk.Frame(khung, bg=self.mau_card)
        khung_nut_dong.pack(fill="x", pady=(8, 8))

        khung_chi_tiet = tk.Frame(khung, bg=self.mau_card)
        khung_chi_tiet.pack(fill="both", expand=True)

        danh_sach_dong = []

        danh_sach_san_pham = self.tao_danh_sach_chon(
            self.nghiep_vu_kho.lay_danh_sach_san_pham(),
            "maSanPham",
            "tenSanPham",
        )

        danh_sach_vi_tri = self.tao_danh_sach_chon(
            self.nghiep_vu_kho.lay_danh_sach_vi_tri(),
            "maViTri",
            "tenViTri",
        )

        def tao_tieu_de_bang_chi_tiet():
            header = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            header.pack(fill="x", pady=(0, 4))

            tk.Label(
                header,
                text="Sản phẩm",
                bg=self.mau_card,
                fg=self.mau_chu_phu,
                font=("Segoe UI", 10, "bold"),
                width=28,
                anchor="w",
            ).pack(side="left", padx=(0, 6))

            tk.Label(
                header,
                text="Số lượng",
                bg=self.mau_card,
                fg=self.mau_chu_phu,
                font=("Segoe UI", 10, "bold"),
                width=10,
                anchor="w",
            ).pack(side="left", padx=(0, 6))

            tk.Label(
                header,
                text="Đơn giá",
                bg=self.mau_card,
                fg=self.mau_chu_phu,
                font=("Segoe UI", 10, "bold"),
                width=12,
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

        def tao_dong_san_pham(du_lieu=None):
            dong_frame = tk.Frame(khung_chi_tiet, bg=self.mau_card)
            dong_frame.pack(fill="x", pady=4)

            sp_cb = ttk.Combobox(
                dong_frame,
                values=danh_sach_san_pham,
                state="readonly",
                font=("Segoe UI", 10),
                width=28,
            )
            sp_cb.pack(side="left", padx=(0, 6))

            so_luong_entry = tk.Entry(
                dong_frame,
                font=("Segoe UI", 10),
                width=10,
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                bd=0,
                highlightbackground=self.mau_vien,
                highlightthickness=1,
            )
            so_luong_entry.pack(side="left", padx=(0, 6), ipady=4)

            don_gia_entry = tk.Entry(
                dong_frame,
                font=("Segoe UI", 10),
                width=12,
                bg=self.mau_card_nhe,
                fg=self.mau_chu_dam,
                bd=0,
                highlightbackground=self.mau_vien,
                highlightthickness=1,
            )
            don_gia_entry.pack(side="left", padx=(0, 6), ipady=4)

            if la_nhap:
                vi_tri_cb = ttk.Combobox(
                    dong_frame,
                    values=danh_sach_vi_tri,
                    state="readonly",
                    font=("Segoe UI", 10),
                    width=18,
                )
                vi_tri_cb.pack(side="left", padx=(0, 6))

                if len(danh_sach_vi_tri) > 0:
                    vi_tri_cb.current(0)
            else:
                vi_tri_cb = None

            if len(danh_sach_san_pham) > 0:
                sp_cb.current(0)

            def cap_nhat_don_gia(event=None):
                ma_san_pham = self.lay_ma_tu_combobox(sp_cb.get())
                san_pham = self.nghiep_vu_kho.tim_san_pham(ma_san_pham)

                if san_pham is not None:
                    don_gia_entry.delete(0, tk.END)
                    don_gia_entry.insert(0, str(san_pham.get("donGia", 0)))

            sp_cb.bind("<<ComboboxSelected>>", cap_nhat_don_gia)
            cap_nhat_don_gia()

            if du_lieu is not None:
                self.chon_combobox_theo_ma(sp_cb, du_lieu.get("maSanPham", ""))

                so_luong_entry.delete(0, tk.END)
                so_luong_entry.insert(0, str(du_lieu.get("soLuong", "")))

                don_gia_entry.delete(0, tk.END)
                don_gia_entry.insert(0, str(du_lieu.get("donGia", "")))

                if la_nhap and vi_tri_cb is not None:
                    self.chon_combobox_theo_ma(vi_tri_cb, du_lieu.get("maViTri", ""))

            danh_sach_dong.append({
                "frame": dong_frame,
                "sp_cb": sp_cb,
                "so_luong_entry": so_luong_entry,
                "don_gia_entry": don_gia_entry,
                "vi_tri_cb": vi_tri_cb,
            })

        def xoa_cac_dong_chi_tiet():
            for widget in khung_chi_tiet.winfo_children():
                widget.destroy()
            danh_sach_dong.clear()

        def tao_cac_dong_chi_tiet():
            so_dong = int(self.chuyen_so(so_dong_entry.get()))

            if so_dong <= 0:
                messagebox.showwarning(
                    "Dữ liệu không hợp lệ",
                    "Số lượng sản phẩm trong phiếu phải lớn hơn 0.",
                )
                return

            xoa_cac_dong_chi_tiet()
            tao_tieu_de_bang_chi_tiet()

            for i in range(so_dong):
                tao_dong_san_pham()

        self.tao_nut(
            khung_nut_dong,
            "Tạo dòng sản phẩm",
            tao_cac_dong_chi_tiet,
            "#B98E7C",
        ).pack(side="left")

        if la_sua:
            self.chon_combobox_theo_ma(
                doi_tac_cb,
                phieu.get("maNhaSanXuat", phieu.get("maKhachHang", "")),
            )
            self.chon_combobox_theo_ma(kho_cb, phieu.get("maKho", ""))

            chi_tiet_cu = phieu.get("chiTiet", [])
            so_dong_entry.insert(0, str(len(chi_tiet_cu)))

            tao_tieu_de_bang_chi_tiet()
            for item in chi_tiet_cu:
                tao_dong_san_pham(item)
        else:
            so_dong_entry.insert(0, "1")
            tao_tieu_de_bang_chi_tiet()
            tao_dong_san_pham()

        def lay_du_lieu_phieu():
            ma_doi_tac = self.lay_ma_tu_combobox(doi_tac_cb.get())
            ma_kho = self.lay_ma_tu_combobox(kho_cb.get())

            if ma_doi_tac == "":
                raise ValueError("Vui lòng chọn thông tin đối tác.")
            if ma_kho == "":
                raise ValueError("Vui lòng chọn kho.")
            if len(danh_sach_dong) == 0:
                raise ValueError("Vui lòng tạo ít nhất 1 dòng sản phẩm.")

            chi_tiet_moi = []

            for dong in danh_sach_dong:
                ma_san_pham = self.lay_ma_tu_combobox(dong["sp_cb"].get())
                so_luong = int(self.chuyen_so(dong["so_luong_entry"].get()))
                don_gia = int(self.chuyen_so(dong["don_gia_entry"].get()))

                if ma_san_pham == "":
                    raise ValueError("Vui lòng chọn sản phẩm.")
                if so_luong <= 0:
                    raise ValueError("Số lượng sản phẩm phải lớn hơn 0.")
                if don_gia <= 0:
                    raise ValueError("Đơn giá sản phẩm phải lớn hơn 0.")

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

                chi_tiet_moi.append(item)

            return ma_doi_tac, ma_kho, chi_tiet_moi

        def luu_phieu(luu_tam):
            try:
                ma_doi_tac, ma_kho, chi_tiet_moi = lay_du_lieu_phieu()

                if la_sua:
                    if la_nhap:
                        self.nghiep_vu_kho.cap_nhat_phieu_nhap(
                            phieu.get("maPhieuNhap", ""),
                            ma_doi_tac,
                            ma_kho,
                            chi_tiet_moi,
                            luu_tam,
                        )
                    else:
                        self.nghiep_vu_kho.cap_nhat_phieu_xuat(
                            phieu.get("maPhieuXuat", ""),
                            ma_doi_tac,
                            ma_kho,
                            chi_tiet_moi,
                            luu_tam,
                        )
                else:
                    if la_nhap:
                        self.nghiep_vu_kho.tao_phieu_nhap(
                            ma_doi_tac,
                            ma_kho,
                            chi_tiet_moi,
                            luu_tam=luu_tam,
                        )
                    else:
                        self.nghiep_vu_kho.tao_phieu_xuat(
                            ma_doi_tac,
                            ma_kho,
                            chi_tiet_moi,
                            luu_tam=luu_tam,
                        )

                form["window"].destroy()
                self.lam_moi_du_lieu_kho()

                if luu_tam:
                    messagebox.showinfo(
                        "Thành công",
                        "Đã lưu tạm phiếu. Bạn vẫn có thể sửa hoặc xóa phiếu này.",
                    )
                else:
                    messagebox.showinfo(
                        "Thành công",
                        "Đã lưu phiếu và cập nhật tồn kho.",
                    )
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", lambda: luu_phieu(False), "#7D9D8C").pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Lưu tạm", lambda: luu_phieu(True), "#B98E7C").pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, "#6E554C").pack(side="right")

    # =========================
    # SỬA / XÓA PHIẾU LƯU TẠM
    # =========================
    def sua_phieu_nhap_da_chon(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_nhap, "phieu_nhap.json", "maPhieuNhap")
        if phieu is None:
            return

        if not self.la_phieu_luu_tam(phieu):
            messagebox.showwarning("Không thể sửa", "Chỉ được sửa phiếu nhập đang lưu tạm.")
            return

        self.mo_form_nhap_xuat_kho("nhap", phieu)

    def sua_phieu_xuat_da_chon(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_xuat, "phieu_xuat.json", "maPhieuXuat")
        if phieu is None:
            return

        if not self.la_phieu_luu_tam(phieu):
            messagebox.showwarning("Không thể sửa", "Chỉ được sửa phiếu xuất đang lưu tạm.")
            return

        self.mo_form_nhap_xuat_kho("xuat", phieu)

    def xoa_phieu_nhap_luu_tam_da_chon(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_nhap, "phieu_nhap.json", "maPhieuNhap")
        if phieu is None:
            return

        if not self.la_phieu_luu_tam(phieu):
            messagebox.showwarning("Không thể xóa", "Chỉ được xóa phiếu nhập đang lưu tạm.")
            return

        ma_phieu = phieu.get("maPhieuNhap", "")
        hoi = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phiếu nhập lưu tạm " + ma_phieu + " không?")

        if not hoi:
            return

        try:
            self.nghiep_vu_kho.xoa_phieu_nhap(ma_phieu)
            self.lam_moi_du_lieu_kho()
            messagebox.showinfo("Thành công", "Đã xóa phiếu nhập lưu tạm.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def xoa_phieu_xuat_luu_tam_da_chon(self):
        phieu = self.lay_phieu_da_chon(self.bang_phieu_xuat, "phieu_xuat.json", "maPhieuXuat")
        if phieu is None:
            return

        if not self.la_phieu_luu_tam(phieu):
            messagebox.showwarning("Không thể xóa", "Chỉ được xóa phiếu xuất đang lưu tạm.")
            return

        ma_phieu = phieu.get("maPhieuXuat", "")
        hoi = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phiếu xuất lưu tạm " + ma_phieu + " không?")

        if not hoi:
            return

        try:
            self.nghiep_vu_kho.xoa_phieu_xuat(ma_phieu)
            self.lam_moi_du_lieu_kho()
            messagebox.showinfo("Thành công", "Đã xóa phiếu xuất lưu tạm.")
        except ValueError as loi:
            messagebox.showerror("Lỗi nghiệp vụ", str(loi))

    def la_phieu_luu_tam(self, phieu):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()
        return trang_thai in ["lưu tạm", "luu tam", "chưa xác nhận", "chua xac nhan"]

    def lay_phieu_da_chon(self, bang, ten_file, truong_ma):
        ma_phieu = self.lay_ma_dong_dang_chon(bang)

        if ma_phieu == "":
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một dòng.")
            return None

        danh_sach = doc_json(ten_file, [])

        for item in danh_sach:
            if item.get(truong_ma) == ma_phieu:
                return item

        messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu đã chọn.")
        return None

    # =========================
    # KIỂM KHO
    # =========================
    def mo_form_kiem_kho(self, phieu=None):
        la_sua = phieu is not None
        title = "Sửa phiếu kiểm kho" if la_sua else "Tạo phiếu kiểm kho"
        form = self.tao_cua_so_form(title, 540, 500)
        khung = form["body"]

        kho_cb = self.tao_combobox_form(
            khung,
            "Kho",
            self.tao_danh_sach_chon(self.nghiep_vu_kho.lay_danh_sach_kho(), "maKho", "tenKho"),
        )

        sp_cb = self.tao_combobox_form(
            khung,
            "Sản phẩm",
            self.tao_danh_sach_chon(self.nghiep_vu_kho.lay_danh_sach_san_pham(), "maSanPham", "tenSanPham"),
        )

        so_luong_entry = self.tao_entry_form(khung, "Số lượng thực tế")
        ghi_chu_entry = self.tao_entry_form(khung, "Ghi chú")

        chi_tiet = {}
        if la_sua and len(phieu.get("chiTiet", [])) > 0:
            chi_tiet = phieu.get("chiTiet", [])[0]

        if la_sua:
            self.chon_combobox_theo_ma(kho_cb, phieu.get("maKho", ""))
            self.chon_combobox_theo_ma(sp_cb, chi_tiet.get("maSanPham", ""))
            so_luong_entry.insert(0, str(chi_tiet.get("soLuongThucTe", "")))
            ghi_chu_entry.insert(0, phieu.get("ghiChu", ""))

        def luu():
            try:
                if la_sua:
                    self.nghiep_vu_kho.xoa_phieu_kiem_ke(phieu.get("maKiemKe", ""), True)

                self.nghiep_vu_kho.tao_phieu_kiem_ke(
                    self.lay_ma_tu_combobox(kho_cb.get()),
                    [{"maSanPham": self.lay_ma_tu_combobox(sp_cb.get()), "soLuongThucTe": int(self.chuyen_so(so_luong_entry.get()))}],
                    ghi_chu_entry.get().strip(),
                )

                form["window"].destroy()
                self.lam_moi_du_lieu_kho()
                messagebox.showinfo("Thành công", "Đã lưu phiếu kiểm kho.")
            except ValueError as loi:
                messagebox.showerror("Lỗi nghiệp vụ", str(loi))

        self.tao_nut(form["bottom"], "Lưu", luu, "#7D9D8C").pack(side="right", padx=(8, 0))
        self.tao_nut(form["bottom"], "Hủy", form["window"].destroy, "#6E554C").pack(side="right")

    def sua_kiem_ke_da_chon(self):
        phieu = self.lay_phieu_da_chon(self.bang_kiem_kho, "kiem_ke.json", "maKiemKe")
        if phieu is None:
            return

        if self.la_phieu_da_chot(phieu):
            messagebox.showwarning("Không thể sửa", "Chỉ được sửa phiếu kiểm kê khi phiếu chưa chốt.")
            return

        self.mo_form_kiem_kho(phieu)

    def la_phieu_da_chot(self, phieu):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()
        return "chốt" in trang_thai or "chot" in trang_thai

    # =========================
    # LỊCH SỬ
    # =========================
    def hien_lich_su(self):
        self.tao_tieu_de_trang(
            self.content,
            "Lịch sử",
            "Theo dõi lịch sử nhập kho, xuất kho và nhật ký hệ thống",
        )

        body = self.tao_khung_noi_dung(self.content)

        self.tao_thanh_cong_cu(
            body,
            "Nhập hành động, tài khoản hoặc trạng thái cần tìm...",
            self.tim_kiem_nhat_ky,
            buttons=[],
        )

        self.tao_nut_thoat(body)

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        self.bang_nhat_ky = self.tao_bang(
            table_area,
            ("maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai"),
            ("Mã", "Tài khoản", "Hành động", "Đối tượng", "Thời gian", "Trạng thái"),
            (90, 130, 230, 180, 220, 150),
        )

        self.load_nhat_ky("")

    def load_nhat_ky(self, tu_khoa=""):
        data = doc_json("nhat_ky.json", [])
        ket_qua = self.loc_du_lieu(
            data,
            tu_khoa,
            ["maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai"],
        )

        self.do_du_lieu_vao_bang(
            self.bang_nhat_ky,
            ket_qua,
            ["maNhatKy", "maTaiKhoan", "hanhDong", "doiTuong", "thoiGian", "trangThai"],
        )

    def tim_kiem_nhat_ky(self, tu_khoa):
        self.load_nhat_ky(tu_khoa)

    # =========================
    # THỐNG KÊ
    # =========================
    def hien_thong_ke(self):
        self.tao_tieu_de_trang(
            self.content,
            self.man_hinh_thong_ke_hien_tai,
            "Theo dõi tồn kho, nhập kho, xuất kho và cảnh báo hàng sắp hết",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body, pady=(14, 0))

        noi_dung = self.tao_vung_cuon_thong_ke(body)

        if self.man_hinh_thong_ke_hien_tai == "Tổng quan kho":
            self.ve_tab_tong_quan(noi_dung)
        elif self.man_hinh_thong_ke_hien_tai == "Tồn kho theo kho":
            self.ve_tab_ton_kho_theo_kho(noi_dung)
        elif self.man_hinh_thong_ke_hien_tai == "Nhập theo ngày":
            self.ve_tab_nhap_theo_ngay(noi_dung)
        elif self.man_hinh_thong_ke_hien_tai == "Xuất theo ngày":
            self.ve_tab_xuat_theo_ngay(noi_dung)
        elif self.man_hinh_thong_ke_hien_tai == "Cảnh báo tồn thấp":
            self.ve_tab_canh_bao_ton_thap(noi_dung)

    def hien_thong_ke_tong_quan(self):
        self.man_hinh_thong_ke_hien_tai = "Tổng quan kho"
        self.hien_thong_ke()

    def hien_thong_ke_ton_kho(self):
        self.man_hinh_thong_ke_hien_tai = "Tồn kho theo kho"
        self.hien_thong_ke()

    def hien_thong_ke_nhap_ngay(self):
        self.man_hinh_thong_ke_hien_tai = "Nhập theo ngày"
        self.hien_thong_ke()

    def hien_thong_ke_xuat_ngay(self):
        self.man_hinh_thong_ke_hien_tai = "Xuất theo ngày"
        self.hien_thong_ke()

    def hien_thong_ke_canh_bao(self):
        self.man_hinh_thong_ke_hien_tai = "Cảnh báo tồn thấp"
        self.hien_thong_ke()

    def tao_vung_cuon_thong_ke(self, parent):
        canvas = tk.Canvas(parent, bg=self.mau_card, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        noi_dung = tk.Frame(canvas, bg=self.mau_card)
        window_id = canvas.create_window((0, 0), window=noi_dung, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, pady=(8, 0))
        scrollbar.pack(side="right", fill="y", pady=(8, 0))

        def cap_nhat_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def cap_nhat_chieu_rong(event):
            canvas.itemconfigure(window_id, width=event.width)

        noi_dung.bind("<Configure>", cap_nhat_scroll)
        canvas.bind("<Configure>", cap_nhat_chieu_rong)

        return noi_dung

    def tao_tab_cuon_thong_ke(self, notebook, ten_tab):
        tab = tk.Frame(notebook, bg=self.mau_card)
        notebook.add(tab, text=ten_tab)

        canvas = tk.Canvas(tab, bg=self.mau_card, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)

        noi_dung = tk.Frame(canvas, bg=self.mau_card)
        window_id = canvas.create_window((0, 0), window=noi_dung, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def cap_nhat_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def cap_nhat_chieu_rong(event):
            canvas.itemconfigure(window_id, width=event.width)

        noi_dung.bind("<Configure>", cap_nhat_scroll)
        canvas.bind("<Configure>", cap_nhat_chieu_rong)

        return noi_dung

    def tao_khung_tab_thong_ke(self, parent, title, subtitle):
        header = tk.Frame(parent, bg=self.mau_card)
        header.pack(fill="x", padx=18, pady=(16, 8))

        self.tao_label(header, title, 18, self.mau_chu_dam, True).pack(anchor="w")

        subtitle_label = self.tao_label(header, subtitle, 11, self.mau_chu_phu)
        subtitle_label.config(wraplength=900, justify="left")
        subtitle_label.pack(anchor="w", pady=(3, 0))

        body = tk.Frame(parent, bg=self.mau_card)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        return body

    def tao_hang_the_thong_ke(self, parent):
        row = tk.Frame(parent, bg=self.mau_card)
        row.pack(fill="x", pady=(0, 14))

        for cot in range(3):
            row.grid_columnconfigure(cot, weight=1, uniform="stat_cards")

        return row

    def tao_the_thong_ke_nho(self, parent, title, value, desc):
        so_cot = parent.grid_size()[0]

        card = self.tao_card(parent)
        card.grid(row=0, column=so_cot, sticky="nsew", padx=6)

        self.tao_label(card, title, 11, self.mau_chu_phu, True).pack(anchor="w", padx=14, pady=(12, 3))

        value_label = self.tao_label(card, str(value), 18, self.mau_menu, True)
        value_label.config(wraplength=240, justify="left")
        value_label.pack(anchor="w", padx=14)

        desc_label = self.tao_label(card, desc, 10, self.mau_chu_phu)
        desc_label.config(wraplength=240, justify="left")
        desc_label.pack(anchor="w", padx=14, pady=(2, 12))

    def ve_tab_tong_quan(self, parent):
        body = self.tao_khung_tab_thong_ke(
            parent,
            "Tổng quan kho hàng",
            "Tóm tắt số kho, số mặt hàng, tổng tồn kho và số sản phẩm dưới mức tồn tối thiểu",
        )

        so_kho = self.dem_so_kho()
        so_hang = self.dem_so_hang_hoa()
        ton_kho = self.tinh_tong_ton_kho()
        canh_bao = len(self.lay_canh_bao_ton_thap())

        row = self.tao_hang_the_thong_ke(body)

        self.tao_the_thong_ke_nho(row, "Số kho", so_kho, "Kho đang quản lý")
        self.tao_the_thong_ke_nho(row, "Sản phẩm", so_hang, "Mặt hàng trong hệ thống")
        self.tao_the_thong_ke_nho(row, "Cần nhập thêm", canh_bao, "Sản phẩm tồn thấp")

        self.ve_bieu_do_cot(
            body,
            "Tổng quan kho",
            ["Kho", "Sản phẩm", "Tồn kho", "Tồn thấp"],
            [so_kho, so_hang, ton_kho, canh_bao],
        )

    def ve_tab_ton_kho_theo_kho(self, parent):
        body = self.tao_khung_tab_thong_ke(
            parent,
            "Tồn kho theo kho",
            "Theo dõi tổng số lượng hàng tồn tại từng kho để hỗ trợ kiểm kho và điều chuyển",
        )

        thong_ke = self.tinh_ton_kho_theo_kho()
        labels = [item["tenKho"] for item in thong_ke]
        values = [item["tongTon"] for item in thong_ke]

        row = self.tao_hang_the_thong_ke(body)

        tong_ton = sum(values)
        kho_co_hang = sum(1 for value in values if value > 0)
        ton_cao_nhat = max(values) if len(values) > 0 else 0

        self.tao_the_thong_ke_nho(row, "Tổng tồn", tong_ton, "Tổng số lượng trong kho")
        self.tao_the_thong_ke_nho(row, "Kho có hàng", kho_co_hang, "Kho đang có tồn")
        self.tao_the_thong_ke_nho(row, "Tồn cao nhất", ton_cao_nhat, "Số lượng lớn nhất/kho")

        self.ve_bieu_do_cot(body, "Số lượng tồn theo kho", labels, values)

    def ve_tab_nhap_theo_ngay(self, parent):
        data = doc_json("phieu_nhap.json", [])
        self.ve_tab_theo_ngay(
            parent,
            "Nhập kho theo ngày",
            "Theo dõi số phiếu nhập và giá trị hàng nhập theo từng ngày",
            data,
            "ngayNhap",
            "Số phiếu nhập",
            "Ngày có nhập kho",
            "Giá trị nhập",
            "Tổng tiền nhập theo ngày",
        )

    def ve_tab_xuat_theo_ngay(self, parent):
        data = doc_json("phieu_xuat.json", [])
        self.ve_tab_theo_ngay(
            parent,
            "Xuất kho theo ngày",
            "Theo dõi số phiếu xuất và giá trị hàng xuất theo từng ngày",
            data,
            "ngayXuat",
            "Số phiếu xuất",
            "Ngày có xuất kho",
            "Giá trị xuất",
            "Tổng tiền xuất theo ngày",
        )

    def ve_tab_theo_ngay(
        self,
        parent,
        title,
        subtitle,
        data,
        truong_ngay,
        ten_the_so_phieu,
        mo_ta_so_ngay,
        mo_ta_tong_tien,
        ten_bieu_do,
    ):
        body = self.tao_khung_tab_thong_ke(parent, title, subtitle)
        thong_ke = {}

        for item in data:
            ngay = item.get(truong_ngay, "Không rõ")
            tong_tien = self.chuyen_so(item.get("tongTien", 0))
            thong_ke[ngay] = thong_ke.get(ngay, 0) + tong_tien

        labels = list(thong_ke.keys())
        values = list(thong_ke.values())

        row = self.tao_hang_the_thong_ke(body)

        self.tao_the_thong_ke_nho(row, ten_the_so_phieu, len(data), "Tổng phiếu")
        self.tao_the_thong_ke_nho(row, "Số ngày", len(labels), mo_ta_so_ngay)
        self.tao_the_thong_ke_nho(row, "Tổng tiền", self.dinh_dang_tien(sum(values)), mo_ta_tong_tien)

        self.ve_bieu_do_cot(body, ten_bieu_do, labels, values, True)

    def ve_tab_canh_bao_ton_thap(self, parent):
        body = self.tao_khung_tab_thong_ke(
            parent,
            "Cảnh báo tồn kho thấp",
            "Danh sách sản phẩm có số lượng tồn nhỏ hơn mức tồn tối thiểu",
        )

        danh_sach = self.lay_canh_bao_ton_thap()
        row = self.tao_hang_the_thong_ke(body)

        self.tao_the_thong_ke_nho(row, "Sản phẩm cảnh báo", len(danh_sach), "Cần xem xét nhập thêm")
        self.tao_the_thong_ke_nho(row, "Tổng thiếu", self.tinh_tong_so_luong_can_nhap(danh_sach), "So với mức tối thiểu")
        self.tao_the_thong_ke_nho(row, "Trạng thái", "Cần xử lý" if len(danh_sach) > 0 else "Ổn định", "Theo mức tồn tối thiểu")

        table_card = self.tao_card(body)
        table_card.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        if len(danh_sach) == 0:
            self.tao_label(
                table_card,
                "Không có sản phẩm nào dưới mức tồn tối thiểu",
                13,
                self.mau_chu_phu,
                True,
            ).pack(expand=True, pady=40)
            return

        bang = self.tao_bang(
            table_card,
            ("maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "canNhapThem"),
            ("Mã kho", "Mã SP", "Tên sản phẩm", "Tồn hiện tại", "Tồn tối thiểu", "Cần nhập thêm"),
            (110, 120, 360, 130, 130, 140),
        )

        self.do_du_lieu_vao_bang(
            bang,
            danh_sach,
            ["maKho", "maSanPham", "tenSanPham", "soLuongTon", "mucTonToiThieu", "canNhapThem"],
        )

    def ve_bieu_do_cot(self, parent, title, labels, values, la_tien=False):
        chart_box = self.tao_card(parent)
        chart_box.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        chart_inner = tk.Frame(chart_box, bg=self.mau_card, height=360)
        chart_inner.pack(fill="both", expand=True, padx=12, pady=10)
        chart_inner.pack_propagate(False)

        if len(labels) == 0:
            self.tao_label(
                chart_inner,
                "Không có dữ liệu để thống kê",
                13,
                self.mau_chu_phu,
                True,
            ).pack(expand=True)
            return

        chieu_rong = max(7.2, min(14, len(labels) * 0.8))
        fig = Figure(figsize=(chieu_rong, 3.2), dpi=100, facecolor=self.mau_card)
        ax = fig.add_subplot(111)

        labels_ngan = [self.rut_gon_chu(label, 12) for label in labels]
        x = list(range(len(labels_ngan)))

        bars = ax.bar(x, values, color="#AD806D", width=0.45)

        ax.set_xticks(x)
        ax.set_xticklabels(
            labels_ngan,
            rotation=35 if len(labels_ngan) > 4 else 0,
            ha="right" if len(labels_ngan) > 4 else "center",
        )

        ax.set_title(title, fontsize=11, fontweight="bold", color=self.mau_chu_dam, pad=8)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.18)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        max_value = max(values) if len(values) > 0 else 0
        if max_value > 0:
            ax.set_ylim(0, max_value * 1.25)

        for bar in bars:
            height = bar.get_height()
            text = self.dinh_dang_so_ngan(height) if la_tien else self.dinh_dang_so(height)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                text,
                ha="center",
                va="bottom",
                fontsize=7,
                color=self.mau_chu_dam,
            )

        fig.subplots_adjust(left=0.09, right=0.98, top=0.86, bottom=0.28)

        canvas = FigureCanvasTkAgg(fig, chart_inner)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # =========================
    # TÀI KHOẢN
    # =========================
    def hien_tai_khoan(self):
        self.tao_tieu_de_trang(
            self.content,
            "Thông tin tài khoản",
            "Thông tin cá nhân và phân công kho",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        data = doc_json("nguoi_dung.json", None)

        if data is None:
            messagebox.showerror("Lỗi", "Không thể đọc file nguoi_dung.json!")
            return

        tai_khoan = self.tim_tai_khoan_nhan_vien_kho(data)

        if tai_khoan is None:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản nhân viên kho!")
            return

        ma_nhan_vien = tai_khoan.get("maNhanVien", "")
        ma_tai_khoan = tai_khoan.get("maTaiKhoan", "")

        nhan_vien = self.tim_nhan_vien_theo_ma(data, ma_nhan_vien)
        kho_duoc_phan_cong = self.tim_kho_duoc_phan_cong(data, ma_tai_khoan)

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        self.tao_card_tai_khoan_ben_trai(main, tai_khoan, nhan_vien)
        self.tao_card_tai_khoan_ben_phai(main, tai_khoan, nhan_vien, kho_duoc_phan_cong)

    def tao_card_tai_khoan_ben_trai(self, parent, tai_khoan, nhan_vien):
        left = self.tao_card(parent)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.config(width=320)
        left.pack_propagate(False)

        avatar = tk.Frame(
            left,
            bg=self.mau_card_nhe,
            width=120,
            height=120,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        avatar.pack(pady=(34, 18))
        avatar.pack_propagate(False)

        tk.Label(
            avatar,
            text="👤",
            bg=self.mau_card_nhe,
            fg=self.mau_menu,
            font=("Segoe UI", 48),
        ).place(relx=0.5, rely=0.5, anchor="center")

        ten_nhan_vien = "Không xác định"
        if nhan_vien is not None:
            ten_nhan_vien = nhan_vien.get("tenNhanVien", "Không xác định")

        self.tao_label(left, ten_nhan_vien, 17, self.mau_chu_dam, True).pack(anchor="center")
        self.tao_label(left, "Nhân viên kho", 11, self.mau_chu_phu).pack(anchor="center", pady=(4, 18))

        if tai_khoan.get("trangThai") is True:
            status_text = "ĐANG HOẠT ĐỘNG"
            status_bg = "#E8F5E9"
            status_fg = "#2E7D32"
        else:
            status_text = "ĐÃ KHÓA"
            status_bg = "#FFEBEE"
            status_fg = "#C62828"

        tk.Label(
            left,
            text=status_text,
            bg=status_bg,
            fg=status_fg,
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=6,
        ).pack(anchor="center")

    def tao_card_tai_khoan_ben_phai(self, parent, tai_khoan, nhan_vien, kho_duoc_phan_cong):
        right = tk.Frame(parent, bg=self.mau_card)
        right.pack(side="right", fill="both", expand=True)

        system_card = self.tao_card(right)
        system_card.pack(fill="x", pady=(0, 14))

        system_inner = tk.Frame(system_card, bg=self.mau_card)
        system_inner.pack(fill="x", padx=24, pady=20)

        self.tao_label(system_inner, "Thông tin hệ thống", 16, self.mau_chu_dam, True).pack(anchor="w", pady=(0, 12))

        self.tao_dong_thong_tin(system_inner, "Mã tài khoản", tai_khoan.get("maTaiKhoan", ""))
        self.tao_dong_thong_tin(system_inner, "Tên tài khoản", tai_khoan.get("tenTaiKhoan", ""))
        self.tao_dong_thong_tin(system_inner, "Vai trò", "Nhân viên kho")
        self.tao_dong_thong_tin(system_inner, "Kho phụ trách", kho_duoc_phan_cong)

        info_card = self.tao_card(right)
        info_card.pack(fill="x")

        info_inner = tk.Frame(info_card, bg=self.mau_card)
        info_inner.pack(fill="x", padx=24, pady=20)

        self.tao_label(info_inner, "Thông tin cá nhân", 16, self.mau_chu_dam, True).pack(anchor="w", pady=(0, 12))

        if nhan_vien is None:
            self.tao_label(info_inner, "Không có dữ liệu nhân viên liên kết", 11, "#C62828").pack(anchor="w")
            return

        self.tao_dong_thong_tin(info_inner, "Mã nhân viên", nhan_vien.get("maNhanVien", ""))
        self.tao_dong_thong_tin(info_inner, "Ngày sinh", nhan_vien.get("ngaySinh", ""))
        self.tao_dong_thong_tin(info_inner, "Email", nhan_vien.get("email", ""))
        self.tao_dong_thong_tin(info_inner, "Số điện thoại", nhan_vien.get("soDienThoai", ""))

    def hien_doi_mat_khau(self):
        self.tao_tieu_de_trang(
            self.content,
            "Đổi mật khẩu",
            "Cập nhật mật khẩu đăng nhập của tài khoản nhân viên kho",
        )

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        khung_giua = tk.Frame(body, bg=self.mau_card)
        khung_giua.pack(fill="both", expand=True)

        form_card = tk.Frame(
            khung_giua,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        form_card.pack(anchor="n", pady=(28, 0), ipadx=22, ipady=10)

        self.tao_label(
            form_card,
            "ĐỔI MẬT KHẨU",
            22,
            self.mau_chu_dam,
            True,
            self.mau_card_nhe,
        ).pack(anchor="w", padx=30, pady=(28, 6))

        mo_ta = "Vui lòng nhập mật khẩu hiện tại và mật khẩu mới để cập nhật tài khoản."
        label_mo_ta = self.tao_label(
            form_card,
            mo_ta,
            11,
            self.mau_chu_phu,
            False,
            self.mau_card_nhe,
        )
        label_mo_ta.config(wraplength=460)
        label_mo_ta.pack(anchor="w", padx=30, pady=(0, 20))

        mat_khau_cu_entry = self.tao_o_mat_khau(
            form_card,
            "Mật khẩu hiện tại",
            False,
        )

        mat_khau_moi_entry = self.tao_o_mat_khau(
            form_card,
            "Mật khẩu mới",
            True,
        )

        xac_nhan_entry = self.tao_o_mat_khau(
            form_card,
            "Xác nhận mật khẩu mới",
            True,
        )

        ghi_chu = self.tao_label(
            form_card,
            "Gợi ý: mật khẩu mới nên có ít nhất 6 ký tự để an toàn hơn.",
            10,
            self.mau_chu_phu,
            False,
            self.mau_card_nhe,
        )
        ghi_chu.pack(anchor="w", padx=30, pady=(2, 12))

        khung_nut = tk.Frame(form_card, bg=self.mau_card_nhe)
        khung_nut.pack(fill="x", padx=30, pady=(8, 28))

        self.tao_nut(
            khung_nut,
            "Lưu mật khẩu",
            lambda: self.luu_mat_khau_moi(
                mat_khau_cu_entry.get(),
                mat_khau_moi_entry.get(),
                xac_nhan_entry.get(),
            ),
            "#7D9D8C",
        ).pack(side="right", padx=(8, 0))

        self.tao_nut(
            khung_nut,
            "Hủy",
            self.hien_tai_khoan,
            "#6E554C",
        ).pack(side="right")

    def tao_o_mat_khau(self, parent, label_text, co_nut_mat):
        self.tao_label(
            parent,
            label_text,
            10,
            self.mau_chu_phu,
            True,
            self.mau_card_nhe,
        ).pack(anchor="w", padx=30, pady=(8, 4))

        row = tk.Frame(parent, bg=self.mau_card_nhe)
        row.pack(fill="x", padx=30, pady=(0, 10))

        entry = tk.Entry(
            row,
            font=("Segoe UI", 11),
            bg="white",
            fg=self.mau_chu_dam,
            bd=0,
            show="*",
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            width=42,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=9)

        if co_nut_mat:
            dang_hien = {"value": False}

            def doi_trang_thai_mat():
                if dang_hien["value"]:
                    entry.config(show="*")
                    nut_mat.config(text="👁")
                    dang_hien["value"] = False
                else:
                    entry.config(show="")
                    nut_mat.config(text="🙈")
                    dang_hien["value"] = True

            nut_mat = tk.Button(
                row,
                text="👁",
                command=doi_trang_thai_mat,
                bg="white",
                fg=self.mau_chu_phu,
                activebackground="white",
                activeforeground=self.mau_chu_dam,
                bd=0,
                font=("Segoe UI", 11),
                cursor="hand2",
                width=4,
            )
            nut_mat.pack(side="right", ipady=7)

        return entry

    def luu_mat_khau_moi(self, mat_khau_cu, mat_khau_moi, xac_nhan):
        data = doc_json("nguoi_dung.json", None)

        if data is None:
            messagebox.showerror("Lỗi", "Không thể đọc file người dùng.")
            return

        tai_khoan = self.tim_tai_khoan_nhan_vien_kho(data)

        if tai_khoan is None:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản nhân viên kho.")
            return

        mat_khau_hien_tai = str(tai_khoan.get("matKhau", ""))

        if mat_khau_cu.strip() == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập mật khẩu hiện tại.")
            return

        if mat_khau_moi.strip() == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập mật khẩu mới.")
            return

        if mat_khau_cu != mat_khau_hien_tai:
            messagebox.showerror("Sai mật khẩu", "Mật khẩu hiện tại không đúng.")
            return

        if len(mat_khau_moi) < 6:
            messagebox.showwarning("Mật khẩu yếu", "Mật khẩu mới nên có ít nhất 6 ký tự.")
            return

        if mat_khau_moi != xac_nhan:
            messagebox.showwarning("Không khớp", "Xác nhận mật khẩu mới không khớp.")
            return

        if mat_khau_moi == mat_khau_cu:
            messagebox.showwarning("Không thay đổi", "Mật khẩu mới không được trùng mật khẩu cũ.")
            return

        tai_khoan["matKhau"] = mat_khau_moi
        ghi_json("nguoi_dung.json", data)

        messagebox.showinfo("Thành công", "Đã đổi mật khẩu thành công.")
        self.hien_tai_khoan()

    # =========================
    # HÀM PHỤ GIAO DIỆN
    # =========================
    def tao_nut_thoat(self, parent, pady=(16, 0)):
        bottom = tk.Frame(parent, bg=self.mau_card)
        bottom.pack(side="bottom", fill="x", pady=pady)

        self.tao_nut(
            bottom,
            "Thoát",
            self.hien_trang_chu,
            "#6E554C",
        ).pack(side="right")

    def tao_dong_thong_tin(self, parent, label_text, value_text):
        row = tk.Frame(parent, bg=self.mau_card)
        row.pack(fill="x", pady=7)

        self.tao_label(row, label_text + ":", 11, self.mau_chu_phu, True).pack(side="left")
        self.tao_label(row, str(value_text), 11, self.mau_chu_dam).pack(side="left", padx=(12, 0))

    def gan_su_kien_click(self, widget, command):
        widget.config(cursor="hand2")
        widget.bind("<Button-1>", lambda event: command())

        for child in widget.winfo_children():
            child.config(cursor="hand2")
            child.bind("<Button-1>", lambda event: command())

    # =========================
    # HÀM PHỤ DỮ LIỆU
    # =========================
    def xoa_du_lieu_bang(self, bang):
        for row in bang.get_children():
            bang.delete(row)

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

    def tim_vai_tro_theo_ma(self, data, ma_vai_tro):
        for vai_tro in data.get("vaiTro", []):
            if vai_tro.get("maVaiTro") == ma_vai_tro:
                return vai_tro.get("tenVaiTro", "")
        return ""

    def tim_tai_khoan_theo_ma(self, data, ma_tai_khoan):
        for tk_item in data.get("taiKhoan", []):
            if tk_item.get("maTaiKhoan") == ma_tai_khoan:
                return tk_item
        return None

    def tim_tai_khoan_nhan_vien_kho(self, data):
        ma_tai_khoan_hien_tai = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

        if ma_tai_khoan_hien_tai != "":
            tai_khoan = self.tim_tai_khoan_theo_ma(data, ma_tai_khoan_hien_tai)

            if tai_khoan is not None:
                return tai_khoan

        for phan_quyen in data.get("phanQuyen", []):
            ma_tai_khoan = phan_quyen.get("maTaiKhoan", "")
            ma_vai_tro = phan_quyen.get("maVaiTro", "")
            ten_vai_tro = self.tim_vai_tro_theo_ma(data, ma_vai_tro)

            if ten_vai_tro in ["NhanVienKho", "Nhân viên kho"]:
                return self.tim_tai_khoan_theo_ma(data, ma_tai_khoan)
        return None

    def tim_nhan_vien_theo_ma(self, data, ma_nhan_vien):
        for nv in data.get("nhanVien", []):
            if nv.get("maNhanVien") == ma_nhan_vien:
                return nv
        return None

    def tim_kho_duoc_phan_cong(self, data, ma_tai_khoan):
        danh_sach_kho = []

        for pc in data.get("phanCongKho", []):
            dung_tai_khoan = pc.get("maTaiKhoan") == ma_tai_khoan
            dang_hoat_dong = pc.get("trangThai") is True

            if dung_tai_khoan and dang_hoat_dong:
                danh_sach_kho.append(pc.get("maKho", ""))

        if len(danh_sach_kho) == 0:
            return "Chưa phân công"
        return ", ".join(danh_sach_kho)

    def dem_so_kho(self):
        data = doc_json("kho_hang.json", {})
        return len(data.get("kho", []))

    def dem_so_hang_hoa(self):
        data = doc_json("hang_hoa.json", {})
        return len(data.get("sanPham", []))

    def tinh_tong_ton_kho(self):
        data = doc_json("kho_hang.json", {})
        tong = 0
        for item in data.get("tonKho", []):
            tong += self.chuyen_so(item.get("soLuongTon", 0))
        return int(tong)

    def tinh_ton_kho_theo_kho(self):
        kho_data = doc_json("kho_hang.json", {})
        danh_sach_kho = kho_data.get("kho", [])
        danh_sach_ton = kho_data.get("tonKho", [])

        thong_ke = {}

        for kho in danh_sach_kho:
            ma_kho = kho.get("maKho", "")
            thong_ke[ma_kho] = {
                "maKho": ma_kho,
                "tenKho": kho.get("tenKho", ma_kho),
                "tongTon": 0,
            }

        for ton in danh_sach_ton:
            ma_kho = ton.get("maKho", "")
            so_luong = self.chuyen_so(ton.get("soLuongTon", 0))

            if ma_kho not in thong_ke:
                thong_ke[ma_kho] = {
                    "maKho": ma_kho,
                    "tenKho": ma_kho,
                    "tongTon": 0,
                }

            thong_ke[ma_kho]["tongTon"] += so_luong

        return list(thong_ke.values())

    def lay_canh_bao_ton_thap(self):
        kho_data = doc_json("kho_hang.json", {})
        hang_data = doc_json("hang_hoa.json", {})

        return lay_canh_bao_ton_thap(
            kho_data.get("tonKho", []),
            hang_data.get("sanPham", []),
            kho_data.get("viTriKho", []),
        )

    def tinh_tong_so_luong_can_nhap(self, danh_sach):
        tong = 0
        for item in danh_sach:
            tong += self.chuyen_so(item.get("canNhapThem", 0))
        return int(tong)

    def tim_ten_san_pham(self, danh_sach_sp, ma_sp):
        for sp in danh_sach_sp:
            if sp.get("maSanPham") == ma_sp:
                return sp.get("tenSanPham", "")
        return ""

    def tim_san_pham_theo_ma(self, danh_sach_sp, ma_sp):
        for sp in danh_sach_sp:
            if sp.get("maSanPham") == ma_sp:
                return sp
        return None

    # =========================
    # HÀM ĐỊNH DẠNG
    # =========================
    def rut_gon_chu(self, text, max_len):
        text = str(text)
        if len(text) <= max_len:
            return text
        return text[:max_len] + "..."

    # =========================
    # ĐĂNG XUẤT
    # =========================
    def dang_xuat(self):
        hoi = messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất không?")

        if hoi:
            self.root.destroy()
            hien_thi_login()


def hien_thi_nhan_vien_kho(tai_khoan_dang_nhap=None):
    app = GiaoDienNhanVienKho(tai_khoan_dang_nhap)
    app.chay()


if __name__ == "__main__":
    hien_thi_nhan_vien_kho()
