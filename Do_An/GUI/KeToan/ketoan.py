import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from Calculator.thongke import thong_ke_tien_theo_ngay
from Calculator.tonkho import lap_du_lieu_ton_kho, tinh_tong_ton_kho
from GUI.Common.base import GiaoDienCoSo


# =========================
# FILE JSON
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
# GIAO DIỆN KẾ TOÁN
# =========================
class GiaoDienKeToan(GiaoDienCoSo):
    def __init__(self, tai_khoan_dang_nhap=None):
        super().__init__()
        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap or {}
        self.ap_dung_theme_ke_toan()

        self.root = tk.Tk()
        self.root.title("Kế toán")
        self.root.geometry("1280x720")
        self.root.minsize(1120, 640)
        self.root.configure(bg=self.mau_nen)

        self.danh_sach_menu = []

        self.cau_hinh_style()
        self.tao_bo_cuc_chinh()
        self.tao_sidebar()
        self.hien_trang_chu()


    def cau_hinh_style(self):
        super().cau_hinh_style()

    def chay(self):
        self.root.mainloop()


    def ap_dung_theme_ke_toan(self):
        self.khoi_tao_mau_sac()


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
            text="💰",
            bg=self.mau_card,
            fg=self.mau_menu_chon,
            font=("Segoe UI", 19),
        ).place(relx=0.5, rely=0.5, anchor="center")

        text_logo = tk.Frame(top_logo, bg=self.mau_sidebar)
        text_logo.pack(side="left", padx=(10, 0))

        tk.Label(
            text_logo,
            text="KẾ TOÁN",
            bg=self.mau_sidebar,
            fg="white",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            text_logo,
            text="Accounting",
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
            text="Chứng từ kho hàng",
            bg=self.mau_sidebar_dam,
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=(7, 1))

        tk.Label(
            slogan,
            text="Nhập • Xuất • Doanh thu",
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

        thanh_cuon_menu = ttk.Scrollbar(vung_menu, orient="vertical", command=canvas_menu.yview)
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
            "📄  Chứng từ",
            [
                ("Phiếu nhập", self.hien_phieu_nhap),
                ("Phiếu xuất", self.hien_phieu_xuat),
            ],
        )

        self.tao_nut_menu(menu, "📦  Tồn kho", self.hien_ton_kho)

        self.tao_menu_xo_sidebar(
            menu,
            "📊  Thống kê",
            [
                ("Tổng quan", self.hien_thong_ke_tong_quan),
                ("Thống kê nhập kho", self.hien_thong_ke_nhap),
                ("Thống kê xuất kho", self.hien_thong_ke_xuat),
                ("Doanh thu", self.hien_doanh_thu),
            ],
        )

        self.tao_menu_tai_khoan_sidebar(menu, self.hien_tai_khoan, self.doi_mat_khau)

        bottom = tk.Frame(self.sidebar, bg=self.mau_sidebar)
        bottom.pack(side="bottom", fill="x", padx=12, pady=(6, 12))

        self.tao_nut(
            bottom,
            "Đăng xuất",
            self.dang_xuat,
            self.mau_sidebar_dam,
        ).pack(fill="x")

    def hien_trang_chu(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Trang chủ kế toán",
            "Tổng quan chứng từ, doanh thu và giá trị tồn kho",
        )
        header.pack(fill="x", padx=24, pady=(18, 8))

        body = self.tao_khung_noi_dung(self.content)

        tong_nhap = self.tong_tien("phieu_nhap.json")
        tong_xuat = self.tong_tien("phieu_xuat.json")
        gia_tri_ton = self.tinh_gia_tri_ton_kho()
        tong_phieu_hom_nay = self.dem_phieu_hom_nay()

        card_row = tk.Frame(body, bg=self.mau_card)
        card_row.pack(fill="x", pady=(0, 12))

        for column in range(4):
            card_row.grid_columnconfigure(column, weight=1, uniform="card")

        self.tao_the_tong_quan(
            card_row,
            "Tổng nhập",
            self.dinh_dang_tien_the(tong_nhap),
            "Giá trị phiếu nhập",
            self.hien_thong_ke_nhap,
            0,
        )

        self.tao_the_tong_quan(
            card_row,
            "Tổng xuất",
            self.dinh_dang_tien_the(tong_xuat),
            "Giá trị phiếu xuất",
            self.hien_thong_ke_xuat,
            1,
        )

        self.tao_the_tong_quan(
            card_row,
            "Giá trị tồn",
            self.dinh_dang_tien_the(gia_tri_ton),
            "Ước tính hàng còn trong kho",
            self.hien_ton_kho,
            2,
        )

        self.tao_the_tong_quan(
            card_row,
            "Phiếu hôm nay",
            tong_phieu_hom_nay,
            "Phiếu nhập + phiếu xuất",
            None,
            3,
        )

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=3, uniform="dashboard")
        main.grid_columnconfigure(1, weight=2, uniform="dashboard")
        main.grid_rowconfigure(0, weight=1)

        left = self.tao_card(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = self.tao_card(main)
        right.grid(row=0, column=1, sticky="nsew")

        self.tao_label(
            left,
            "Biểu đồ nhập xuất",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", padx=16, pady=(14, 4))

        self.tao_label(
            left,
            "Theo dõi nhanh tổng giá trị chứng từ để kế toán đối chiếu.",
            size=9,
            color=self.mau_chu_phu,
        ).pack(anchor="w", padx=16, pady=(0, 6))

        self.ve_bieu_do_cot_canvas(
            left,
            "Tổng quan giá trị",
            ["Nhập", "Xuất", "Tồn"],
            [tong_nhap, tong_xuat, gia_tri_ton],
            True,
            chieu_cao=105,
        )

        table_card = tk.Frame(left, bg=self.mau_card)
        table_card.pack(fill="both", expand=True, padx=16, pady=(6, 12))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_columnconfigure(1, weight=1)

        self.tao_bang_nho_dashboard(
            table_card,
            0,
            "Phiếu nhập gần đây",
            "phieu_nhap.json",
            "maPhieuNhap",
            "ngayNhap",
        )

        self.tao_bang_nho_dashboard(
            table_card,
            1,
            "Phiếu xuất gần đây",
            "phieu_xuat.json",
            "maPhieuXuat",
            "ngayXuat",
        )

        self.tao_label(
            right,
            "Việc cần theo dõi",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", padx=16, pady=(14, 8))

        doi_chieu = self.dinh_dang_tien_the(tong_xuat - tong_nhap)
        self.tao_muc_theo_doi(right, "Chênh lệch nhập/xuất", doi_chieu, "Đối chiếu doanh thu")
        self.tao_muc_theo_doi(right, "Phiếu hôm nay", tong_phieu_hom_nay, "Cần kiểm tra trạng thái")
        self.tao_muc_theo_doi(right, "Tồn kho thấp", len([item for item in self.lay_du_lieu_ton_kho() if item.get("canhBao") == "Tồn thấp"]), "Ưu tiên kiểm tra")

        self.tao_bang_ton_thap(right, 3)
        self.tao_bang_nhat_ky_ke_toan(right)

    def hien_phieu_nhap(self):
        self.hien_bang_chung_tu(
            "Phiếu nhập",
            "Theo dõi danh sách phiếu nhập kho",
            "phieu_nhap.json",
            ("maPhieuNhap", "tenKho", "ngayNhap", "tongTien", "trangThai"),
            ("Mã phiếu", "Tên kho", "Ngày nhập", "Tổng tiền", "Trạng thái"),
            (140, 280, 150, 180, 140),
            ["maPhieuNhap", "tenKho", "ngayNhap", "tongTien", "trangThai"],
        )

    def hien_phieu_xuat(self):
        self.hien_bang_chung_tu(
            "Phiếu xuất",
            "Theo dõi danh sách phiếu xuất kho",
            "phieu_xuat.json",
            ("maPhieuXuat", "tenKho", "ngayXuat", "tongTien", "trangThai"),
            ("Mã phiếu", "Tên kho", "Ngày xuất", "Tổng tiền", "Trạng thái"),
            (140, 280, 150, 180, 140),
            ["maPhieuXuat", "tenKho", "ngayXuat", "tongTien", "trangThai"],
        )

    def hien_bang_chung_tu(self, title, subtitle, ten_file, columns, headings, widths, keys):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(title, subtitle)
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)

        data_hien_tai = {"data": []}
        bang_luu = {"bang": None}

        def load(tu_khoa=""):
            data = self.lay_du_lieu_phieu(ten_file)
            ket_qua = self.loc_du_lieu(data, tu_khoa, keys)
            data_hien_tai["data"] = ket_qua

            if bang_luu["bang"] is not None:
                self.do_du_lieu_chung_tu(bang_luu["bang"], ket_qua, keys)

        def tim_kiem(tu_khoa):
            load(tu_khoa)

        def xem_chi_tiet():
            bang = bang_luu["bang"]
            ma_phieu = self.lay_ma_dong_dang_chon(bang)

            if ma_phieu == "":
                messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một phiếu.")
                return

            self.hien_chi_tiet_phieu(ma_phieu, data_hien_tai["data"], columns[0])

        self.tao_thanh_cong_cu(
            body,
            "Nhập mã phiếu, kho hoặc trạng thái cần tìm...",
            tim_kiem,
            buttons=[
                {
                    "text": "Xem chi tiết",
                    "command": xem_chi_tiet,
                    "color": self.mau_sua,
                },
            ],
        )

        self.tao_nut_thoat(body)

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        bang = self.tao_bang(table_area, columns, headings, widths)
        bang_luu["bang"] = bang

        load("")

    def hien_chi_tiet_phieu(self, ma_phieu, danh_sach, truong_ma):
        phieu = None

        for item in danh_sach:
            if item.get(truong_ma, "") == ma_phieu:
                phieu = item

        if phieu is None:
            messagebox.showerror("Lỗi", "Không tìm thấy phiếu đã chọn.")
            return

        form = self.tao_cua_so_form("Chi tiết phiếu " + ma_phieu, 620, 520, self.root)
        body = form["body"]

        self.tao_dong_thong_tin(body, "Mã phiếu", ma_phieu)
        self.tao_dong_thong_tin(body, "Kho", phieu.get("maKho", ""))
        self.tao_dong_thong_tin(body, "Tổng tiền", self.dinh_dang_tien_khong_don_vi(phieu.get("tongTien", 0)))
        self.tao_dong_thong_tin(body, "Trạng thái", phieu.get("trangThai", ""))

        self.tao_label(
            body,
            "Danh sách sản phẩm",
            size=13,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", pady=(14, 8))

        bang = self.tao_bang(
            body,
            ("maSanPham", "soLuong", "donGia", "maViTri"),
            ("Mã SP", "Số lượng", "Đơn giá", "Vị trí"),
            (130, 110, 150, 130),
        )

        self.do_du_lieu_vao_bang(
            bang,
            phieu.get("chiTiet", []),
            ["maSanPham", "soLuong", "donGia", "maViTri"],
        )

        self.tao_nut_luu_huy(
            form["bottom"],
            form["window"].destroy,
            form["window"].destroy,
            "Đóng",
            "Hủy",
        )

    def do_du_lieu_chung_tu(self, bang, data, keys):
        self.xoa_du_lieu_bang(bang)

        for item in data:
            values = []

            for key in keys:
                if key == "tongTien":
                    values.append(self.dinh_dang_tien_khong_don_vi(item.get(key, 0)))
                else:
                    values.append(item.get(key, ""))

            bang.insert("", "end", values=values)

    # =========================
    # TỒN KHO
    # =========================
    def hien_ton_kho(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Tồn kho",
            "Theo dõi số lượng tồn và giá trị hàng còn trong kho",
        )
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        data_ton = self.lay_du_lieu_ton_kho()
        tong_mat_hang = len(data_ton)
        tong_so_luong = tinh_tong_ton_kho(data_ton)
        tong_gia_tri = sum(self.chuyen_so(item.get("giaTriTon", 0)) for item in data_ton)
        sap_het_hang = len([item for item in data_ton if item.get("canhBao", "") == "Tồn thấp"])

        row = tk.Frame(body, bg=self.mau_card)
        row.pack(fill="x", pady=(0, 14))

        self.tao_the_tong_quan(row, "Mặt hàng", tong_mat_hang, "Số sản phẩm có tồn")
        self.tao_the_tong_quan(row, "Tổng tồn", self.dinh_dang_so(tong_so_luong), "Tổng số lượng còn")
        self.tao_the_tong_quan(row, "Giá trị tồn", self.dinh_dang_tien_the(tong_gia_tri), "Số tiền ước tính")
        self.tao_the_tong_quan(row, "Tồn thấp", sap_het_hang, "Cần kiểm tra")

        def tim_kiem(tu_khoa):
            ket_qua = self.loc_du_lieu(
                data_ton,
                tu_khoa,
                ["maSanPham", "tenSanPham", "maKho", "canhBao"],
            )
            self.do_du_lieu_ton_kho(bang, ket_qua)

        self.tao_thanh_cong_cu(
            body,
            "Nhập mã sản phẩm, tên sản phẩm hoặc kho cần tìm...",
            tim_kiem,
            buttons=[],
        )

        table_area = tk.Frame(body, bg=self.mau_card)
        table_area.pack(fill="both", expand=True)

        bang = self.tao_bang(
            table_area,
            ("maSanPham", "tenSanPham", "maKho", "soLuongTon", "donGia", "giaTriTon", "canhBao"),
            ("Mã SP", "Tên sản phẩm", "Kho", "Tồn", "Đơn giá", "Giá trị tồn", "Cảnh báo"),
            (110, 230, 110, 90, 130, 150, 120),
        )

        bang.tag_configure("ton_thap", foreground=self.mau_nguy_hiem)
        bang.tag_configure("sap_het", foreground=self.mau_nguy_hiem)
        bang.tag_configure("het_hang", foreground=self.mau_nguy_hiem)
        bang.tag_configure("binh_thuong", foreground=self.mau_chu_dam)

        self.do_du_lieu_ton_kho(bang, data_ton)

    def lay_du_lieu_ton_kho(self):
        du_lieu_kho = doc_json("kho_hang.json", {})
        du_lieu_hang = doc_json("hang_hoa.json", {})
        danh_sach_ma_kho = self.lay_danh_sach_ma_kho_duoc_phan_cong()

        return lap_du_lieu_ton_kho(
            self.loc_theo_kho_duoc_phan_cong(du_lieu_kho.get("tonKho", []), danh_sach_ma_kho),
            du_lieu_hang.get("sanPham", []),
            self.loc_theo_kho_duoc_phan_cong(du_lieu_kho.get("viTriKho", []), danh_sach_ma_kho),
        )

    def do_du_lieu_ton_kho(self, bang, data):
        self.xoa_du_lieu_bang(bang)

        for item in data:
            canh_bao = str(item.get("canhBao", "")).strip().lower()
            so_luong_ton = self.chuyen_so(item.get("soLuongTon", 0))

            if so_luong_ton <= 0 or "hết" in canh_bao or "het" in canh_bao:
                tag = "het_hang"
            elif "sắp" in canh_bao or "sap" in canh_bao:
                tag = "sap_het"
            elif "thấp" in canh_bao or "thap" in canh_bao:
                tag = "ton_thap"
            else:
                tag = "binh_thuong"

            bang.insert(
                "",
                "end",
                values=(
                    item.get("maSanPham", ""),
                    item.get("tenSanPham", ""),
                    item.get("maKho", ""),
                    self.dinh_dang_so(item.get("soLuongTon", 0)),
                    self.dinh_dang_tien_khong_don_vi(item.get("donGia", 0)),
                    self.dinh_dang_tien_khong_don_vi(item.get("giaTriTon", 0)),
                    item.get("canhBao", ""),
                ),
                tags=(tag,),
            )

    def tinh_gia_tri_ton_kho(self):
        tong = 0

        for item in self.lay_du_lieu_ton_kho():
            tong += self.chuyen_so(item.get("giaTriTon", 0))

        return tong

    # =========================
    # THỐNG KÊ
    # =========================
    def hien_thong_ke_nhap(self):
        self.hien_thong_ke_don(
            "Thống kê phiếu nhập",
            "Tổng hợp số lượng và giá trị nhập kho",
            "phieu_nhap.json",
            "Phiếu nhập",
        )

    def hien_thong_ke_xuat(self):
        self.hien_thong_ke_don(
            "Thống kê phiếu xuất",
            "Tổng hợp số lượng và giá trị xuất kho",
            "phieu_xuat.json",
            "Phiếu xuất",
        )

    def hien_doanh_thu(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Doanh thu",
            "Theo dõi chênh lệch giá trị xuất và nhập",
        )
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)

        tong_nhap = self.tong_tien("phieu_nhap.json")
        tong_xuat = self.tong_tien("phieu_xuat.json")
        chenhlech = tong_xuat - tong_nhap

        row = tk.Frame(body, bg=self.mau_card)
        row.pack(fill="x", pady=(0, 16))

        self.tao_the_tong_quan(row, "Tổng nhập", self.dinh_dang_tien_the(tong_nhap), "Giá trị nhập kho", self.hien_thong_ke_nhap)
        self.tao_the_tong_quan(row, "Tổng xuất", self.dinh_dang_tien_the(tong_xuat), "Giá trị xuất kho", self.hien_thong_ke_xuat)
        self.tao_the_tong_quan(row, "Chênh lệch", self.dinh_dang_tien_the(chenhlech), "Xuất - nhập")

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=3, uniform="doanhthu")
        main.grid_columnconfigure(1, weight=2, uniform="doanhthu")
        main.grid_rowconfigure(0, weight=1)

        chart_area = self.tao_card(main)
        chart_area.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.tao_label(
            chart_area,
            "Biểu đồ giá trị nhập xuất",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", padx=16, pady=(14, 0))

        self.ve_bieu_do_cot_canvas(
            chart_area,
            "Tổng nhập / Tổng xuất / Chênh lệch",
            ["Tổng nhập", "Tổng xuất", "Chênh lệch"],
            [tong_nhap, tong_xuat, chenhlech],
            True,
            chieu_cao=250,
        )

        table_card = self.tao_card(main)
        table_card.grid(row=0, column=1, sticky="nsew")

        self.tao_label(
            table_card,
            "Chứng từ gần đây",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", padx=16, pady=(14, 8))

        table_area = tk.Frame(table_card, bg=self.mau_card)
        table_area.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        bang = self.tao_bang(
            table_area,
            ("loai", "maPhieu", "ngay", "tongTien", "trangThai"),
            ("Loại", "Mã phiếu", "Ngày", "Tổng tiền", "Trạng thái"),
            (92, 105, 95, 120, 105),
        )
        self.do_du_lieu_chung_tu_gan_day(bang)

        self.tao_nut_thoat(body)

    def hien_thong_ke_tong_quan(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Thống kê tổng quan",
            "Biểu đồ chính bên trái, bảng số liệu rút gọn bên phải để kế toán dễ đối chiếu",
        )
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)

        tong_nhap = self.tong_tien("phieu_nhap.json")
        tong_xuat = self.tong_tien("phieu_xuat.json")
        gia_tri_ton = self.tinh_gia_tri_ton_kho()

        row = tk.Frame(body, bg=self.mau_card)
        row.pack(fill="x", pady=(0, 12))
        self.tao_the_tong_quan(row, "Tổng nhập", self.dinh_dang_tien_the(tong_nhap), "Giá trị phiếu nhập")
        self.tao_the_tong_quan(row, "Tổng xuất", self.dinh_dang_tien_the(tong_xuat), "Giá trị phiếu xuất")
        self.tao_the_tong_quan(row, "Giá trị tồn", self.dinh_dang_tien_the(gia_tri_ton), "Hàng còn trong kho")

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=3, uniform="thongke")
        main.grid_columnconfigure(1, weight=2, uniform="thongke")
        main.grid_rowconfigure(0, weight=1)

        left = self.tao_card(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = self.tao_card(main)
        right.grid(row=0, column=1, sticky="nsew")

        self.tao_label(left, "Biểu đồ giá trị", size=17, color=self.mau_chu_dam, bold=True).pack(anchor="w", padx=18, pady=(18, 0))
        self.ve_bieu_do_cot_canvas(
            left,
            "Nhập / Xuất / Tồn",
            ["Nhập", "Xuất", "Tồn"],
            [tong_nhap, tong_xuat, gia_tri_ton],
            True,
            chieu_cao=230,
        )

        self.tao_label(right, "Bảng số liệu", size=17, color=self.mau_chu_dam, bold=True).pack(anchor="w", padx=18, pady=(18, 8))

        table_area = tk.Frame(right, bg=self.mau_card)
        table_area.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        bang = self.tao_bang(
            table_area,
            ("noiDung", "soLuong", "giaTri", "ghiChu"),
            ("Nội dung", "Số lượng", "Giá trị", "Ghi chú"),
            (150, 90, 145, 180),
        )

        du_lieu = self.lay_du_lieu_bang_thong_ke_tong_quan()
        self.xoa_du_lieu_bang(bang)
        for item in du_lieu:
            bang.insert("", "end", values=(
                item.get("noiDung", ""),
                item.get("soLuong", ""),
                item.get("giaTri", ""),
                item.get("ghiChu", ""),
            ))

        self.tao_nut_thoat(body)

    def hien_thong_ke_don(self, title, subtitle, ten_file, ten_loai):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(title, subtitle)
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)

        tong_phieu = self.dem_phieu(ten_file)
        tong_tien = self.tong_tien(ten_file)
        trung_binh = self.tinh_trung_binh(tong_tien, tong_phieu)

        row = tk.Frame(body, bg=self.mau_card)
        row.pack(fill="x", pady=(0, 12))
        self.tao_the_tong_quan(row, ten_loai, tong_phieu, "Tổng số phiếu")
        self.tao_the_tong_quan(row, "Tổng tiền", self.dinh_dang_tien_the(tong_tien), "Tổng giá trị")
        self.tao_the_tong_quan(row, "Trung bình", self.dinh_dang_tien_khong_don_vi(round(trung_binh)), "Giá trị/phiếu")

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=3, uniform="thongke_don")
        main.grid_columnconfigure(1, weight=2, uniform="thongke_don")
        main.grid_rowconfigure(0, weight=1)

        left = self.tao_card(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = self.tao_card(main)
        right.grid(row=0, column=1, sticky="nsew")

        thong_ke_ngay = self.thong_ke_theo_ngay(ten_file)
        self.tao_label(left, "Biểu đồ theo ngày", size=17, color=self.mau_chu_dam, bold=True).pack(anchor="w", padx=18, pady=(18, 0))
        self.ve_bieu_do_cot_canvas(
            left,
            "Tổng tiền theo ngày",
            thong_ke_ngay["labels"],
            thong_ke_ngay["values"],
            True,
            chieu_cao=240,
        )

        self.tao_label(right, "Bảng số liệu", size=17, color=self.mau_chu_dam, bold=True).pack(anchor="w", padx=18, pady=(18, 8))

        table_area = tk.Frame(right, bg=self.mau_card)
        table_area.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        bang = self.tao_bang(
            table_area,
            ("maPhieu", "ngay", "kho", "tongTien", "trangThai"),
            ("Mã phiếu", "Ngày", "Kho", "Tổng tiền", "Trạng thái"),
            (105, 105, 85, 135, 110),
        )

        data = self.lay_du_lieu_phieu(ten_file)
        self.do_du_lieu_thong_ke(bang, data)

        self.tao_nut_thoat(body)

    # =========================
    # TÀI KHOẢN
    # =========================
    def hien_tai_khoan(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Thông tin tài khoản",
            "Thông tin cá nhân và vai trò kế toán",
        )
        header.pack(fill="x", padx=28, pady=(22, 10))

        body = self.tao_khung_noi_dung(self.content)
        self.tao_nut_thoat(body)

        data = doc_json("nguoi_dung.json", {})
        tai_khoan = self.tim_tai_khoan_ke_toan(data)

        if tai_khoan is None:
            self.tao_label(
                body,
                "Không tìm thấy tài khoản kế toán.",
                size=13,
                color=self.mau_nguy_hiem,
                bold=True,
            ).pack(anchor="w", padx=22, pady=22)
            return

        ma_nhan_vien = tai_khoan.get("maNhanVien", "")
        nhan_vien = self.tim_nhan_vien_theo_ma(data, ma_nhan_vien)

        main = tk.Frame(body, bg=self.mau_card)
        main.pack(fill="both", expand=True)

        self.tao_card_tai_khoan_ben_trai(main, tai_khoan, nhan_vien)
        self.tao_card_tai_khoan_ben_phai(main, tai_khoan, nhan_vien)

    def tao_card_tai_khoan_ben_trai(self, parent, tai_khoan, nhan_vien):
        left = self.tao_card(parent)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.config(width=320)
        left.pack_propagate(False)

        avatar = tk.Frame(
            left,
            bg=self.mau_card_nhe,
            width=112,
            height=112,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        avatar.pack(pady=(30, 16))
        avatar.pack_propagate(False)

        self.tao_label(
            avatar,
            "👤",
            size=44,
            color=self.mau_menu_chon,
            bg=self.mau_card_nhe,
        ).place(relx=0.5, rely=0.5, anchor="center")

        ten_hien_thi = tai_khoan.get("tenTaiKhoan", "Kế toán")

        if nhan_vien is not None:
            ten_hien_thi = nhan_vien.get("tenNhanVien", ten_hien_thi)

        self.tao_label(
            left,
            ten_hien_thi,
            size=17,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="center")

        self.tao_label(
            left,
            "Kế toán",
            size=11,
            color=self.mau_chu_phu,
        ).pack(anchor="center", pady=(4, 18))

        if self.tai_khoan_dang_hoat_dong(tai_khoan):
            status_text = "ĐANG HOẠT ĐỘNG"
            status_bg = self.mau_sidebar_nhat
            status_fg = self.mau_thanh_cong
        else:
            status_text = "ĐÃ KHÓA"
            status_bg = self.mau_card_nhe
            status_fg = self.mau_nguy_hiem

        tk.Label(
            left,
            text=status_text,
            bg=status_bg,
            fg=status_fg,
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=6,
        ).pack(anchor="center")

    def tao_card_tai_khoan_ben_phai(self, parent, tai_khoan, nhan_vien):
        right = tk.Frame(parent, bg=self.mau_card)
        right.pack(side="right", fill="both", expand=True)

        system_card = self.tao_card(right)
        system_card.pack(fill="x", pady=(0, 14))

        system_inner = tk.Frame(system_card, bg=self.mau_card)
        system_inner.pack(fill="x", padx=24, pady=20)

        self.tao_label(
            system_inner,
            "Thông tin hệ thống",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", pady=(0, 12))

        self.tao_dong_thong_tin(system_inner, "Mã tài khoản", tai_khoan.get("maTaiKhoan", ""))
        self.tao_dong_thong_tin(system_inner, "Tên tài khoản", tai_khoan.get("tenTaiKhoan", ""))
        self.tao_dong_thong_tin(system_inner, "Vai trò", "Kế toán")
        self.tao_dong_thong_tin(system_inner, "Trạng thái", self.lay_trang_thai_tai_khoan(tai_khoan))

        info_card = self.tao_card(right)
        info_card.pack(fill="x")

        info_inner = tk.Frame(info_card, bg=self.mau_card)
        info_inner.pack(fill="x", padx=24, pady=20)

        self.tao_label(
            info_inner,
            "Thông tin cá nhân",
            size=16,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", pady=(0, 12))

        if nhan_vien is None:
            self.tao_label(
                info_inner,
                "Không có dữ liệu nhân viên liên kết",
                size=11,
                color=self.mau_nguy_hiem,
            ).pack(anchor="w")
            return

        self.tao_dong_thong_tin(info_inner, "Mã nhân viên", nhan_vien.get("maNhanVien", ""))
        self.tao_dong_thong_tin(info_inner, "Ngày sinh", nhan_vien.get("ngaySinh", ""))
        self.tao_dong_thong_tin(info_inner, "Email", nhan_vien.get("email", ""))
        self.tao_dong_thong_tin(info_inner, "Số điện thoại", nhan_vien.get("soDienThoai", ""))

    def doi_mat_khau(self):
        self.xoa_noi_dung(self.content)

        header = self.tao_header_trang(
            "Đổi mật khẩu",
            "Cập nhật mật khẩu đăng nhập cho tài khoản kế toán",
        )
        header.pack(fill="x", padx=28, pady=(22, 10))

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
            size=22,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card_nhe,
        ).pack(anchor="w", padx=30, pady=(28, 6))

        mo_ta = self.tao_label(
            form_card,
            "Vui lòng nhập mật khẩu hiện tại và mật khẩu mới để cập nhật tài khoản.",
            size=11,
            color=self.mau_chu_phu,
            bg=self.mau_card_nhe,
        )
        mo_ta.config(wraplength=460)
        mo_ta.pack(anchor="w", padx=30, pady=(0, 20))

        mat_khau_cu_entry = self.tao_o_mat_khau(form_card, "Mật khẩu hiện tại", False)
        mat_khau_moi_entry = self.tao_o_mat_khau(form_card, "Mật khẩu mới", True)
        xac_nhan_entry = self.tao_o_mat_khau(form_card, "Xác nhận mật khẩu mới", True)

        ghi_chu = self.tao_label(
            form_card,
            "Gợi ý: mật khẩu mới nên có ít nhất 6 ký tự để an toàn hơn.",
            size=10,
            color=self.mau_chu_phu,
            bg=self.mau_card_nhe,
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
            self.mau_them,
        ).pack(side="right", padx=(8, 0))

        self.tao_nut(
            khung_nut,
            "Hủy",
            self.hien_tai_khoan,
            self.mau_thoat,
        ).pack(side="right")

    def luu_mat_khau_moi(self, mat_khau_cu, mat_khau_moi, xac_nhan):
        data = doc_json("nguoi_dung.json", None)

        if data is None:
            messagebox.showerror("Lỗi", "Không thể đọc file người dùng.")
            return

        tai_khoan = self.tim_tai_khoan_ke_toan(data)

        if tai_khoan is None:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản kế toán.")
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
    # HELPER UI
    # =========================

    def tao_header_trang(self, title, subtitle):
        header = tk.Frame(self.content, bg=self.mau_nen)

        left_header = tk.Frame(header, bg=self.mau_nen)
        left_header.pack(side="left", fill="x", expand=True)

        self.tao_label(
            left_header,
            title,
            size=24,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_nen,
        ).pack(anchor="w")

        self.tao_label(
            left_header,
            subtitle,
            size=9,
            color=self.mau_chu_phu,
            bg=self.mau_nen,
        ).pack(anchor="w", pady=(2, 0))

        self.tao_user_box(header).pack(side="right", pady=(2, 0))

        return header


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

        icon = self.tao_label(
            icon_box,
            "👤",
            size=12,
            color=self.mau_menu_chon,
            bg=self.mau_card_nhe,
        )
        icon.place(relx=0.5, rely=0.5, anchor="center")

        text_box = tk.Frame(user_box, bg=self.mau_card)
        text_box.pack(side="left", padx=(0, 14), pady=7)

        name = self.tao_label(
            text_box,
            "Xin chào, Kế toán",
            size=9,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        )
        name.pack(anchor="w")

        role = self.tao_label(
            text_box,
            "Vai trò: Kế toán",
            size=8,
            color=self.mau_chu_phu,
            bg=self.mau_card,
        )
        role.pack(anchor="w", pady=(2, 0))

        user_box.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        icon.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        name.bind("<Button-1>", lambda event: self.hien_tai_khoan())
        role.bind("<Button-1>", lambda event: self.hien_tai_khoan())

        return user_box

    def tao_the_tong_quan(self, parent, title, value, desc, command=None, column=None):
        card = self.tao_card(parent)
        card.config(height=136)
        card.pack_propagate(False)

        if column is None:
            column = len(parent.grid_slaves(row=0))

        parent.grid_columnconfigure(column, weight=1)
        card.grid(row=0, column=column, sticky="nsew", padx=5)

        title_label = self.tao_label(
            card,
            title,
            size=10,
            color=self.mau_chu_dam,
            bold=True,
        )
        title_label.pack(anchor="w", padx=14, pady=(12, 4))

        value_label = self.tao_label(
            card,
            str(value),
            size=15,
            color=self.mau_menu_chon,
            bold=True,
        )
        value_label.config(wraplength=260, justify="left")
        value_label.pack(anchor="w", padx=14)

        desc_label = self.tao_label(
            card,
            desc,
            size=8,
            color=self.mau_chu_phu,
        )
        desc_label.config(wraplength=260, justify="left")
        desc_label.pack(anchor="w", padx=14, pady=(4, 10))

        if command is not None:
            self.gan_su_kien_click(card, command)

    def tao_loi_tat(self, parent, icon, title, desc, command):
        item = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
            cursor="hand2",
        )
        item.pack(fill="x", padx=18, pady=(0, 10))

        self.tao_label(
            item,
            icon,
            size=20,
            color=self.mau_menu_chon,
            bg=self.mau_card_nhe,
        ).pack(side="left", padx=(14, 10), pady=12)

        text_frame = tk.Frame(item, bg=self.mau_card_nhe)
        text_frame.pack(side="left", fill="x", expand=True, pady=10)

        self.tao_label(
            text_frame,
            title,
            size=11,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card_nhe,
        ).pack(anchor="w")

        self.tao_label(
            text_frame,
            desc,
            size=9,
            color=self.mau_chu_phu,
            bg=self.mau_card_nhe,
        ).pack(anchor="w", pady=(2, 0))

        self.gan_su_kien_click(item, command)


    def tao_muc_theo_doi(self, parent, title, value, desc):
        item = tk.Frame(
            parent,
            bg=self.mau_nhan_nhe,
            highlightbackground=self.mau_canh_bao,
            highlightthickness=1,
        )
        item.pack(fill="x", padx=16, pady=(0, 8))

        left = tk.Frame(item, bg=self.mau_nhan_nhe)
        left.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=8)

        self.tao_label(
            left,
            title,
            size=9,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_nhan_nhe,
        ).pack(anchor="w")

        self.tao_label(
            left,
            desc,
            size=8,
            color=self.mau_chu_phu,
            bg=self.mau_nhan_nhe,
        ).pack(anchor="w", pady=(2, 0))

        self.tao_label(
            item,
            str(value),
            size=10,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_nhan_nhe,
        ).pack(side="right", padx=(8, 12), pady=8)

    def tao_bang_nho_dashboard(self, parent, column, title, ten_file, key_ma, key_ngay):
        card = tk.Frame(
            parent,
            bg=self.mau_card,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 8) if column == 0 else (8, 0))

        self.tao_label(
            card,
            title,
            size=12,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        ).pack(anchor="w", padx=14, pady=(12, 8))

        data = self.lay_du_lieu_phieu(ten_file)
        data = data[-2:]

        if len(data) == 0:
            self.tao_label(
                card,
                "Chưa có dữ liệu",
                size=10,
                color=self.mau_chu_phu,
                bg=self.mau_card,
            ).pack(anchor="w", padx=14, pady=(0, 12))
            return

        for item in reversed(data):
            row = tk.Frame(card, bg=self.mau_card_nhe)
            row.pack(fill="x", padx=14, pady=(0, 8))

            self.tao_label(
                row,
                item.get(key_ma, ""),
                size=10,
                color=self.mau_chu_dam,
                bold=True,
                bg=self.mau_card_nhe,
            ).pack(side="left", padx=(10, 0), pady=7)

            self.tao_label(
                row,
                item.get(key_ngay, ""),
                size=9,
                color=self.mau_chu_phu,
                bg=self.mau_card_nhe,
            ).pack(side="right", padx=(0, 10), pady=7)

    def tao_thong_bao(self, parent, text):
        item = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        item.pack(fill="x", padx=18, pady=(0, 10))

        label = self.tao_label(
            item,
            "• " + text,
            size=10,
            color=self.mau_chu_phu,
            bg=self.mau_card_nhe,
        )
        label.config(wraplength=260, justify="left")
        label.pack(anchor="w", padx=14, pady=12)

    def tao_nut_thoat(self, parent):
        bottom = tk.Frame(parent, bg=self.mau_card)
        bottom.pack(side="bottom", fill="x", pady=(14, 0))

        self.tao_nut(
            bottom,
            "Thoát",
            self.hien_trang_chu,
            self.mau_thoat,
        ).pack(side="right")

    def tao_o_mat_khau(self, parent, label_text, co_mat=False):
        self.tao_label(
            parent,
            label_text,
            size=10,
            color=self.mau_chu_phu,
            bold=True,
            bg=self.mau_card_nhe,
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

        if co_mat:
            dang_hien = {"value": False}

            def doi_an_hien():
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
                command=doi_an_hien,
                bg="white",
                fg=self.mau_chu_phu,
                activebackground="white",
                activeforeground=self.mau_chu_dam,
                bd=0,
                width=4,
                font=("Segoe UI", 11),
                cursor="hand2",
            )
            nut_mat.pack(side="right", ipady=7)

        return entry

    def tao_dong_thong_tin(self, parent, label_text, value_text):
        row = tk.Frame(parent, bg=self.mau_card)
        row.pack(fill="x", pady=6)

        self.tao_label(
            row,
            label_text + ":",
            size=11,
            color=self.mau_chu_phu,
            bold=True,
        ).pack(side="left")

        self.tao_label(
            row,
            str(value_text),
            size=11,
            color=self.mau_chu_dam,
        ).pack(side="left", padx=(12, 0))

    def gan_su_kien_click(self, widget, command):
        widget.config(cursor="hand2")
        widget.bind("<Button-1>", lambda event: command())

        for child in widget.winfo_children():
            child.config(cursor="hand2")
            child.bind("<Button-1>", lambda event: command())

    def ve_bieu_do_cot_canvas(self, parent, title, labels, values, la_tien=False, chieu_cao=210):
        chart_card = self.tao_card(parent)
        chart_card.pack(fill="x", padx=16, pady=(10, 0))

        self.tao_label(
            chart_card,
            title,
            size=13,
            color=self.mau_chu_dam,
            bold=True,
        ).pack(anchor="w", padx=14, pady=(9, 2))

        canvas = tk.Canvas(
            chart_card,
            bg=self.mau_card,
            height=chieu_cao,
            highlightthickness=0,
        )
        canvas.pack(fill="x", padx=14, pady=(0, 8))

        def ve_lai(event=None):
            canvas.delete("all")
            chieu_rong = canvas.winfo_width()

            if event is not None:
                chieu_rong = event.width

            chieu_rong = max(chieu_rong, 320)

            if len(labels) == 0 or len(values) == 0:
                canvas.create_text(
                    chieu_rong / 2,
                    chieu_cao / 2,
                    text="Không có dữ liệu để thống kê",
                    fill=self.mau_chu_phu,
                    font=("Segoe UI", 11, "bold"),
                )
                return

            gia_tri = []
            for value in values:
                gia_tri.append(abs(self.chuyen_so(value)))

            max_value = max(gia_tri)
            if max_value <= 0:
                max_value = 1

            le_trai = 42
            y_goc = chieu_cao - 38
            chieu_cao_bieu_do = max(36, y_goc - 28)
            so_cot = len(labels)
            vung_ve = max(chieu_rong - 76, 220)
            khoang = max(18, vung_ve / max(so_cot, 1))
            rong_cot = min(42, max(8, int(khoang * 0.46)))

            canvas.create_line(le_trai, 20, le_trai, y_goc, fill=self.mau_vien)
            canvas.create_line(le_trai, y_goc, chieu_rong - 18, y_goc, fill=self.mau_vien)

            for index in range(so_cot):
                value = self.chuyen_so(values[index])
                cao = int(abs(value) / max_value * chieu_cao_bieu_do)
                x_giua = le_trai + khoang * index + khoang / 2
                x1 = x_giua - rong_cot / 2
                x2 = x_giua + rong_cot / 2
                y1 = y_goc - cao
                y2 = y_goc

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.mau_menu_chon,
                    outline="",
                )

                if la_tien:
                    text_value = self.dinh_dang_so_ngan(value)
                else:
                    text_value = self.dinh_dang_so(value)

                canvas.create_text(
                    x_giua,
                    max(12, y1 - 9),
                    text=text_value,
                    fill=self.mau_chu_dam,
                    font=("Segoe UI", 7 if so_cot > 8 else 8),
                )

                if so_cot <= 12 or index % 2 == 0:
                    canvas.create_text(
                        x_giua,
                        y_goc + 18,
                        text=self.rut_gon_chu(labels[index], 10 if so_cot <= 8 else 6),
                        fill=self.mau_chu_phu,
                        font=("Segoe UI", 7 if so_cot > 8 else 8),
                    )

        canvas.bind("<Configure>", ve_lai)
        canvas.after(50, ve_lai)

    def rut_gon_chu(self, text, max_len):
        text = str(text)

        if len(text) <= max_len:
            return text

        return text[:max_len] + "..."

    def tao_bang_ton_thap(self, parent, gioi_han=4):
        card = tk.Frame(parent, bg=self.mau_card, highlightbackground=self.mau_vien, highlightthickness=1)
        card.pack(fill="x", padx=18, pady=(0, 12))

        self.tao_label(
            card,
            "Hàng tồn kho thấp",
            size=13,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        ).pack(anchor="w", padx=14, pady=(12, 6))

        data = self.lay_du_lieu_ton_kho()
        data = [item for item in data if item.get("canhBao") == "Tồn thấp"]
        data = sorted(data, key=lambda item: self.chuyen_so(item.get("soLuongTon", 0)))[:gioi_han]

        if len(data) == 0:
            self.tao_label(
                card,
                "Không có sản phẩm tồn thấp.",
                size=10,
                color=self.mau_chu_phu,
                bg=self.mau_card,
            ).pack(anchor="w", padx=14, pady=(0, 12))
            return

        for item in data:
            row = tk.Frame(card, bg=self.mau_card_nhe)
            row.pack(fill="x", padx=14, pady=(0, 8))

            ten = self.rut_gon_chu(item.get("tenSanPham", ""), 26)
            self.tao_label(row, ten, size=10, color=self.mau_chu_dam, bold=True, bg=self.mau_card_nhe).pack(side="left", padx=(10, 0), pady=7)

            so_luong = self.dinh_dang_so(item.get("soLuongTon", 0))
            toi_thieu = self.dinh_dang_so(item.get("mucTonToiThieu", 0))
            self.tao_label(row, so_luong + " / " + toi_thieu, size=9, color=self.mau_nguy_hiem, bold=True, bg=self.mau_card_nhe).pack(side="right", padx=(0, 10), pady=7)

    def tao_bang_nhat_ky_ke_toan(self, parent):
        card = tk.Frame(parent, bg=self.mau_card, highlightbackground=self.mau_vien, highlightthickness=1)
        card.pack(fill="x", padx=18, pady=(0, 12))

        self.tao_label(
            card,
            "Nhật ký liên quan chứng từ",
            size=13,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        ).pack(anchor="w", padx=14, pady=(12, 6))

        data = doc_json("nhat_ky.json", [])
        data = [item for item in data if item.get("doiTuong", "") in ["Phiếu nhập", "Phiếu xuất", "Kiểm kê", "Hàng hóa"]]
        data = sorted(data, key=lambda item: item.get("thoiGian", ""), reverse=True)[:4]

        if len(data) == 0:
            self.tao_label(card, "Chưa có nhật ký phù hợp.", size=10, color=self.mau_chu_phu, bg=self.mau_card).pack(anchor="w", padx=14, pady=(0, 12))
            return

        for item in data:
            row = tk.Frame(card, bg=self.mau_card_nhe)
            row.pack(fill="x", padx=14, pady=(0, 8))
            text = self.rut_gon_chu(item.get("hanhDong", ""), 28)
            self.tao_label(row, text, size=10, color=self.mau_chu_dam, bg=self.mau_card_nhe).pack(side="left", padx=(10, 0), pady=7)
            self.tao_label(row, item.get("thoiGian", "")[:10], size=9, color=self.mau_chu_phu, bg=self.mau_card_nhe).pack(side="right", padx=(0, 10), pady=7)

    def lay_du_lieu_bang_thong_ke_tong_quan(self):
        phieu_nhap = self.lay_du_lieu_phieu("phieu_nhap.json")
        phieu_xuat = self.lay_du_lieu_phieu("phieu_xuat.json")
        du_lieu_kho = doc_json("kho_hang.json", {})
        du_lieu_hang = doc_json("hang_hoa.json", {})
        kiem_ke = self.lay_du_lieu_kiem_ke()

        tong_nhap = self.tong_tien("phieu_nhap.json")
        tong_xuat = self.tong_tien("phieu_xuat.json")
        ton_kho = self.lay_du_lieu_ton_kho()
        tong_ton = sum(self.chuyen_so(item.get("soLuongTon", 0)) for item in ton_kho)
        gia_tri_ton = sum(self.chuyen_so(item.get("giaTriTon", 0)) for item in ton_kho)
        danh_sach_kho = self.loc_theo_kho_duoc_phan_cong(du_lieu_kho.get("kho", []))

        return [
            {"noiDung": "Phiếu nhập", "soLuong": len(phieu_nhap), "giaTri": self.dinh_dang_tien_khong_don_vi(tong_nhap), "ghiChu": "Tổng giá trị nhập kho"},
            {"noiDung": "Phiếu xuất", "soLuong": len(phieu_xuat), "giaTri": self.dinh_dang_tien_khong_don_vi(tong_xuat), "ghiChu": "Tổng giá trị xuất kho"},
            {"noiDung": "Kho hàng", "soLuong": len(danh_sach_kho), "giaTri": "-", "ghiChu": "Số kho được phân công"},
            {"noiDung": "Sản phẩm", "soLuong": len(du_lieu_hang.get("sanPham", [])), "giaTri": "-", "ghiChu": "Mặt hàng đang quản lý"},
            {"noiDung": "Tồn kho", "soLuong": self.dinh_dang_so(tong_ton), "giaTri": self.dinh_dang_tien_khong_don_vi(gia_tri_ton), "ghiChu": "Tổng số lượng và giá trị tồn"},
            {"noiDung": "Kiểm kê", "soLuong": len(kiem_ke), "giaTri": "-", "ghiChu": "Phiếu kiểm kê đã ghi nhận"},
        ]

    # =========================
    # DATA HELPER
    # =========================
    def trang_thai_dang_hoat_dong(self, value):
        if value is True:
            return True

        value = str(value).strip().lower()
        return value in ["true", "1", "hoạt động", "hoat dong", "đang hoạt động", "dang hoat dong", "active"]

    def lay_danh_sach_ma_kho_duoc_phan_cong(self):
        ma_tai_khoan = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

        if ma_tai_khoan == "":
            return []

        nguoi_dung = doc_json("nguoi_dung.json", {})
        ket_qua = []

        for phan_cong in nguoi_dung.get("phanCongKho", []):
            dung_tai_khoan = phan_cong.get("maTaiKhoan", "") == ma_tai_khoan
            dang_hoat_dong = self.trang_thai_dang_hoat_dong(phan_cong.get("trangThai", True))
            ma_kho = phan_cong.get("maKho", "")

            if dung_tai_khoan and dang_hoat_dong and ma_kho != "" and ma_kho not in ket_qua:
                ket_qua.append(ma_kho)

        return ket_qua

    def loc_theo_kho_duoc_phan_cong(self, danh_sach, danh_sach_ma_kho=None):
        if danh_sach_ma_kho is None:
            danh_sach_ma_kho = self.lay_danh_sach_ma_kho_duoc_phan_cong()

        ket_qua = []

        for item in danh_sach:
            if item.get("maKho", "") in danh_sach_ma_kho:
                ket_qua.append(item)

        return ket_qua

    def lay_du_lieu_phieu(self, ten_file):
        data = self.loc_theo_kho_duoc_phan_cong(doc_json(ten_file, []))
        ket_qua = []

        for item in data:
            dong = dict(item)
            ma_kho = dong.get("maKho", "")
            dong["tenKho"] = self.lay_ten_kho(ma_kho)
            ket_qua.append(dong)

        return ket_qua

    def lay_ten_kho(self, ma_kho):
        kho_data = doc_json("kho_hang.json", {})

        for kho in kho_data.get("kho", []):
            if kho.get("maKho", "") == ma_kho:
                ten_kho = kho.get("tenKho", ma_kho)
                return ma_kho + " - " + ten_kho

        return ma_kho

    def lay_du_lieu_kiem_ke(self):
        return self.loc_theo_kho_duoc_phan_cong(doc_json("kiem_ke.json", []))

    def do_du_lieu_thong_ke(self, bang, data):
        self.xoa_du_lieu_bang(bang)

        for item in data:
            ma_phieu = item.get("maPhieuNhap", item.get("maPhieuXuat", ""))
            ngay = item.get("ngayNhap", item.get("ngayXuat", ""))

            bang.insert(
                "",
                "end",
                values=(
                    ma_phieu,
                    ngay,
                    item.get("maKho", ""),
                    self.dinh_dang_tien_khong_don_vi(item.get("tongTien", 0)),
                    item.get("trangThai", ""),
                ),
            )

    def do_du_lieu_chung_tu_gan_day(self, bang):
        self.xoa_du_lieu_bang(bang)

        danh_sach = []

        for item in self.lay_du_lieu_phieu("phieu_nhap.json"):
            danh_sach.append({
                "loai": "Phiếu nhập",
                "maPhieu": item.get("maPhieuNhap", ""),
                "ngay": item.get("ngayNhap", ""),
                "tongTien": item.get("tongTien", 0),
                "trangThai": item.get("trangThai", ""),
            })

        for item in self.lay_du_lieu_phieu("phieu_xuat.json"):
            danh_sach.append({
                "loai": "Phiếu xuất",
                "maPhieu": item.get("maPhieuXuat", ""),
                "ngay": item.get("ngayXuat", ""),
                "tongTien": item.get("tongTien", 0),
                "trangThai": item.get("trangThai", ""),
            })

        danh_sach = sorted(danh_sach, key=lambda item: item.get("ngay", ""), reverse=True)[:5]

        for item in danh_sach:
            bang.insert(
                "",
                "end",
                values=(
                    item.get("loai", ""),
                    item.get("maPhieu", ""),
                    item.get("ngay", ""),
                    self.dinh_dang_tien_khong_don_vi(item.get("tongTien", 0)),
                    item.get("trangThai", ""),
                ),
            )

    def loc_du_lieu(self, danh_sach, tu_khoa, keys):
        tu_khoa = tu_khoa.lower().strip()
        ket_qua = []

        for item in danh_sach:
            noi_dung = ""

            for key in keys:
                noi_dung += str(item.get(key, "")) + " "

            if tu_khoa == "" or tu_khoa in noi_dung.lower():
                ket_qua.append(item)

        return ket_qua

    def thong_ke_theo_ngay(self, ten_file):
        data = self.lay_du_lieu_phieu(ten_file)
        truong_ngay = "ngayNhap"

        if ten_file == "phieu_xuat.json":
            truong_ngay = "ngayXuat"

        return thong_ke_tien_theo_ngay(data, truong_ngay)

    def dem_phieu_hom_nay(self):
        from datetime import date

        hom_nay = date.today().isoformat()
        tong = 0

        for ten_file, key_ngay in [("phieu_nhap.json", "ngayNhap"), ("phieu_xuat.json", "ngayXuat")]:
            data = self.lay_du_lieu_phieu(ten_file)

            for item in data:
                if str(item.get(key_ngay, ""))[:10] == hom_nay:
                    tong += 1

        return tong

    def dem_phieu(self, ten_file):
        data = self.lay_du_lieu_phieu(ten_file)
        return len(data)

    def tong_tien(self, ten_file):
        data = self.lay_du_lieu_phieu(ten_file)
        tong = 0

        for item in data:
            tong += self.chuyen_so(item.get("tongTien", 0))

        return tong

    def tinh_trung_binh(self, tong, so_luong):
        if so_luong == 0:
            return 0

        return tong / so_luong

    def dinh_dang_tien_khong_don_vi(self, value):
        return "{:,}".format(int(self.chuyen_so(value))).replace(",", ".")

    def dinh_dang_tien_the(self, value):
        so = self.chuyen_so(value)
        dau = "-" if so < 0 else ""
        so = abs(so)

        if so >= 1000000000:
            return dau + f"{so / 1000000000:.1f}".replace(".", ",") + " tỷ"

        if so >= 1000000:
            return dau + f"{so / 1000000:.1f}".replace(".", ",") + " triệu"

        if so >= 1000:
            return dau + f"{so / 1000:.0f}".replace(".", ",") + " nghìn"

        return dau + self.dinh_dang_so(so) + " đ"

    def tim_tai_khoan_ke_toan(self, data):
        ma_tai_khoan_hien_tai = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

        if ma_tai_khoan_hien_tai != "":
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maTaiKhoan", "") == ma_tai_khoan_hien_tai:
                    return tai_khoan

        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            vai_tro_map[vai_tro.get("maVaiTro", "")] = vai_tro.get("tenVaiTro", "")

        for phan_quyen in data.get("phanQuyen", []):
            ten_vai_tro = vai_tro_map.get(phan_quyen.get("maVaiTro", ""), "")

            if ten_vai_tro in ["KeToan", "Kế toán"]:
                ma_tai_khoan = phan_quyen.get("maTaiKhoan", "")

                for tai_khoan in data.get("taiKhoan", []):
                    if tai_khoan.get("maTaiKhoan", "") == ma_tai_khoan:
                        return tai_khoan

        return None

    def tim_nhan_vien_theo_ma(self, data, ma_nhan_vien):
        for nhan_vien in data.get("nhanVien", []):
            if nhan_vien.get("maNhanVien", "") == ma_nhan_vien:
                return nhan_vien

        return None

    def lay_trang_thai_tai_khoan(self, tai_khoan):
        if self.tai_khoan_dang_hoat_dong(tai_khoan):
            return "Đang hoạt động"

        return "Đã khóa"

    def tai_khoan_dang_hoat_dong(self, tai_khoan):
        trang_thai = str(tai_khoan.get("trangThai", "")).strip().lower()

        return trang_thai in [
            "true",
            "1",
            "hoạt động",
            "hoat dong",
            "đang hoạt động",
            "dang hoat dong",
            "active",
        ]

    # =========================
    # NHẬT KÝ ĐĂNG XUẤT
    # =========================
    def tao_ma_nhat_ky_moi(self, danh_sach):
        so_lon_nhat = 0

        for item in danh_sach:
            ma = str(item.get("maNhatKy", "")).replace("NK", "")

            if ma.isdigit():
                so_lon_nhat = max(so_lon_nhat, int(ma))

        return "NK" + str(so_lon_nhat + 1).zfill(4)

    def ghi_nhat_ky_dang_xuat(self):
        data = doc_json("nhat_ky.json", [])
        ma_tai_khoan = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

        data.append({
            "maNhatKy": self.tao_ma_nhat_ky_moi(data),
            "maTaiKhoan": ma_tai_khoan,
            "hanhDong": "Đăng xuất",
            "doiTuong": "Tài khoản",
            "thoiGian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trangThai": "Thành công",
            "ghiChu": "Kế toán đăng xuất hệ thống",
        })

        ghi_json("nhat_ky.json", data)

    # =========================
    # ĐĂNG XUẤT
    # =========================
    def dang_xuat(self):
        hoi = messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất không?")

        if hoi:
            self.ghi_nhat_ky_dang_xuat()
            self.root.destroy()

            from GUI.Login.login import hien_thi_login
            hien_thi_login()


def hien_thi_ke_toan(tai_khoan_dang_nhap=None):
    app = GiaoDienKeToan(tai_khoan_dang_nhap)
    app.chay()


if __name__ == "__main__":
    hien_thi_ke_toan()
