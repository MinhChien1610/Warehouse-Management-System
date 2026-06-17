from __future__ import annotations

from Calculator.tonkho import tinh_tong_ton_kho as tinh_tong_ton_kho_calculator
from Calculator.tonkho import tinh_ton_kho_theo_kho as tinh_ton_kho_theo_kho_calculator
from Calculator.tonkho import lay_canh_bao_ton_thap as lay_canh_bao_ton_thap_calculator
from Calculator.tonkho import tinh_tong_so_luong_can_nhap as tinh_tong_so_luong_can_nhap_calculator
from Calculator.thongke import thong_ke_tien_theo_ngay


class ThongKe:
    # =========================
    # MENU THỐNG KÊ
    # =========================

    def lay_menu_thong_ke(self):
        vai_tro = getattr(self, "ten_vai_tro", "")

        if vai_tro == "Admin":
            return [
                ("Tổng quan kho", self.hien_thong_ke_tong_quan),
                ("Nhập theo ngày", self.hien_thong_ke_nhap_ngay),
                ("Xuất theo ngày", self.hien_thong_ke_xuat_ngay),
                ("Cảnh báo tồn thấp", self.hien_thong_ke_canh_bao),
            ]

        if vai_tro == "Kế toán":
            return [
                ("Nhập theo ngày", self.hien_thong_ke_nhap_ngay),
                ("Xuất theo ngày", self.hien_thong_ke_xuat_ngay),
            ]

        return []

    # =========================
    # PHÂN QUYỀN DỮ LIỆU
    # =========================

    def lay_du_lieu_thong_ke(self, danh_sach):
        vai_tro = getattr(self, "ten_vai_tro", "")

        if vai_tro == "Admin":
            return danh_sach

        return self.loc_theo_kho_duoc_phan_cong(danh_sach)

    # =========================
    # TỔNG QUAN
    # =========================

    def dem_so_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return len(
            self.lay_du_lieu_thong_ke(
                data.get("kho", [])
            )
        )

    def dem_so_hang_hoa(self):
        data = self.doc_json("kho_hang.json", {})

        danh_sach_ma_san_pham = set()

        for ton in self.lay_du_lieu_thong_ke(
            data.get("tonKho", [])
        ):
            ma_san_pham = ton.get("maSanPham", "")

            if ma_san_pham != "":
                danh_sach_ma_san_pham.add(ma_san_pham)

        return len(danh_sach_ma_san_pham)

    def tinh_tong_ton_kho(self):
        data = self.doc_json("kho_hang.json", {})

        return tinh_tong_ton_kho_calculator(
            self.lay_du_lieu_thong_ke(
                data.get("tonKho", [])
            )
        )

    def tinh_ton_kho_theo_kho(self):
        data = self.doc_json("kho_hang.json", {})

        return tinh_ton_kho_theo_kho_calculator(
            self.lay_du_lieu_thong_ke(
                data.get("kho", [])
            ),
            self.lay_du_lieu_thong_ke(
                data.get("tonKho", [])
            ),
        )

    def lay_canh_bao_ton_thap(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})

        return lay_canh_bao_ton_thap_calculator(
            self.lay_du_lieu_thong_ke(
                kho_data.get("tonKho", [])
            ),
            hang_data.get("sanPham", []),
        )

    # =========================
    # NHẬP / XUẤT
    # =========================

    def tinh_tong_so_luong_can_nhap(self, danh_sach):
        return tinh_tong_so_luong_can_nhap_calculator(danh_sach)

    def thong_ke_phieu_theo_ngay(
        self,
        ten_file,
        truong_ngay,
    ):
        data = self.doc_json(ten_file, [])

        return thong_ke_tien_theo_ngay(
            self.lay_du_lieu_thong_ke(data),
            truong_ngay,
        )