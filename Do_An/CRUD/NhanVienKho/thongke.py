from __future__ import annotations

from Calculator.tonkho import tinh_tong_ton_kho as tinh_tong_ton_kho_calculator
from Calculator.tonkho import tinh_ton_kho_theo_kho as tinh_ton_kho_theo_kho_calculator
from Calculator.tonkho import lay_canh_bao_ton_thap as lay_canh_bao_ton_thap_calculator
from Calculator.tonkho import tinh_tong_so_luong_can_nhap as tinh_tong_so_luong_can_nhap_calculator
from Calculator.thongke import thong_ke_tien_theo_ngay


class ThongKe:
    def dem_so_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return len(data.get("kho", []))

    def dem_so_hang_hoa(self):
        data = self.doc_json("hang_hoa.json", {})
        return len(data.get("sanPham", []))

    def tinh_tong_ton_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return tinh_tong_ton_kho_calculator(data.get("tonKho", []))

    def tinh_ton_kho_theo_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return tinh_ton_kho_theo_kho_calculator(
            data.get("kho", []),
            data.get("tonKho", []),
        )

    def lay_canh_bao_ton_thap(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})
        return lay_canh_bao_ton_thap_calculator(
            kho_data.get("tonKho", []),
            hang_data.get("sanPham", []),
        )

    def tinh_tong_so_luong_can_nhap(self, danh_sach):
        return tinh_tong_so_luong_can_nhap_calculator(danh_sach)

    def thong_ke_phieu_theo_ngay(self, ten_file, truong_ngay):
        data = self.doc_json(ten_file, [])
        return thong_ke_tien_theo_ngay(data, truong_ngay)
