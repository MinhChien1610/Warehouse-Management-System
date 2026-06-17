from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from Class.tonkho import TonKho
from Class.phieunhap import PhieuNhap
from Class.phieuxuat import PhieuXuat
from Class.kiemke import KiemKe
from Calculator.phieu import tinh_tong_tien_chi_tiet
from Calculator.common import chuyen_so_nguyen
from Calculator.tonkho import lay_canh_bao_ton_thap as tinh_canh_bao_ton_thap
from Calculator.tonkho import lap_du_lieu_ton_kho


class KhoHang:
    def lay_thu_muc_goc(self):
        thu_muc = os.path.dirname(os.path.abspath(__file__))

        while True:
            if os.path.exists(os.path.join(thu_muc, "Data")):
                return thu_muc

            thu_muc_cha = os.path.dirname(thu_muc)

            if thu_muc_cha == thu_muc:
                return os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))
                    )
                )

            thu_muc = thu_muc_cha

    def lay_duong_dan_file(self, ten_file: str):
        return os.path.join(self.thu_muc_data, ten_file)

    def doc_json(self, ten_file: str, mac_dinh: Any):
        duong_dan = self.lay_duong_dan_file(ten_file)

        if not os.path.exists(duong_dan):
            return deepcopy(mac_dinh)

        for encoding in ["utf-8-sig", "utf-8"]:
            try:
                with open(duong_dan, "r", encoding=encoding) as file:
                    return json.load(file)
            except json.JSONDecodeError:
                continue

        return deepcopy(mac_dinh)

    def ghi_json(self, ten_file: str, data: Any):
        duong_dan = self.lay_duong_dan_file(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # =========================
    # TÀI KHOẢN HIỆN TẠI
    # =========================

    def lay_ma_tai_khoan_nhan_vien_kho(self):
        data = self.doc_json("nguoi_dung.json", {})

        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            ma_vai_tro = vai_tro.get("maVaiTro", "")
            ten_vai_tro = vai_tro.get("tenVaiTro", "")
            vai_tro_map[ma_vai_tro] = ten_vai_tro

        for phan_quyen in data.get("phanQuyen", []):
            ma_vai_tro = phan_quyen.get("maVaiTro", "")
            ten_vai_tro = vai_tro_map.get(ma_vai_tro, "")

            if ten_vai_tro in ["NhanVienKho", "Nhân viên kho"]:
                return phan_quyen.get("maTaiKhoan", "")

        return ""

    def lay_danh_sach_ma_kho_duoc_phan_cong(self):
        data = self.doc_json("nguoi_dung.json", {})
        danh_sach = []

        for phan_cong in data.get("phanCongKho", []):
            dung_tai_khoan = phan_cong.get("maTaiKhoan") == self.ma_tai_khoan
            dang_hoat_dong = phan_cong.get("trangThai") is True

            if dung_tai_khoan and dang_hoat_dong:
                ma_kho = phan_cong.get("maKho", "")
                if ma_kho != "" and ma_kho not in danh_sach:
                    danh_sach.append(ma_kho)

        return danh_sach

    def loc_theo_kho_duoc_phan_cong(self, danh_sach, truong_kho="maKho"):
        danh_sach_ma_kho = self.lay_danh_sach_ma_kho_duoc_phan_cong()

        if len(danh_sach_ma_kho) == 0:
            return []

        return [
            item
            for item in danh_sach
            if item.get(truong_kho, "") in danh_sach_ma_kho
        ]

    # =========================
    # DANH MỤC
    # =========================

    def lay_danh_sach_kho(self):
        data = self.doc_json("kho_hang.json", {})
        return self.loc_theo_kho_duoc_phan_cong(data.get("kho", []))

    def lay_danh_sach_vi_tri(self, ma_kho: str = ""):
        data = self.doc_json("kho_hang.json", {})
        danh_sach = data.get("viTriKho", [])

        if ma_kho == "":
            return self.loc_theo_kho_duoc_phan_cong(danh_sach)

        if ma_kho not in self.lay_danh_sach_ma_kho_duoc_phan_cong():
            return []

        return [item for item in danh_sach if item.get("maKho") == ma_kho]

    def lay_danh_sach_san_pham(self):
        data = self.doc_json("hang_hoa.json", {})
        return data.get("sanPham", [])

    def lay_danh_sach_nha_san_xuat(self):
        data = self.doc_json("doi_tac.json", {})
        return data.get("nhaSanXuat", [])

    def lay_danh_sach_khach_hang(self):
        data = self.doc_json("doi_tac.json", {})
        return data.get("khachHang", [])

    def tim_san_pham(self, ma_san_pham: str):
        for san_pham in self.lay_danh_sach_san_pham():
            if san_pham.get("maSanPham") == ma_san_pham:
                return san_pham

        return None

    def la_san_pham_dang_kinh_doanh(self, san_pham):
        trang_thai = str(san_pham.get("trangThai", "")).strip().lower()
        return trang_thai not in [
            "ngừng kinh doanh",
            "ngung kinh doanh",
            "đã ngừng",
            "da ngung",
            "false",
            "0",
            "inactive",
        ]

    # =========================
    # HÀNG HÓA
    # =========================

    def tim_kho(self, ma_kho: str):
        for kho in self.lay_danh_sach_kho():
            if kho.get("maKho") == ma_kho:
                return kho

        return None

    def lay_ton_kho(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})
        ket_qua = lap_du_lieu_ton_kho(
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("tonKho", [])),
            hang_data.get("sanPham", []),
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("viTriKho", [])),
        )

        for ton in ket_qua:
            ton["maViTri"] = ton.get("viTriHang", "")

        return ket_qua

    def lay_so_luong_ton(self, ma_kho: str, ma_san_pham: str):
        kho_data = self.doc_json("kho_hang.json", {})

        for ton in kho_data.get("tonKho", []):
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                return self.chuyen_so_nguyen(ton.get("soLuongTon", 0))

        return 0

    def cap_nhat_ton_kho(
        self,
        ma_kho: str,
        ma_san_pham: str,
        so_luong_thay_doi: int,
        ma_vi_tri: str = "",
    ):
        kho_data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = kho_data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                so_luong_cu = self.chuyen_so_nguyen(ton.get("soLuongTon", 0))
                so_luong_moi = so_luong_cu + so_luong_thay_doi

                if so_luong_moi < 0:
                    raise ValueError("Số lượng tồn kho không đủ.")

                ton["soLuongTon"] = so_luong_moi

                if ma_vi_tri != "":
                    ton["maViTri"] = ma_vi_tri

                self.ghi_json("kho_hang.json", kho_data)
                return

        if so_luong_thay_doi < 0:
            raise ValueError("Sản phẩm chưa có tồn kho nên không thể xuất hàng.")

        danh_sach_ton.append(
            TonKho(ma_kho, ma_san_pham, so_luong_thay_doi, ma_vi_tri).to_dict()
        )

        self.ghi_json("kho_hang.json", kho_data)

    def dat_lai_ton_kho(self, ma_kho: str, ma_san_pham: str, so_luong_moi: int):
        if so_luong_moi < 0:
            raise ValueError("Số lượng tồn mới không hợp lệ.")

        kho_data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = kho_data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            dung_kho = ton.get("maKho") == ma_kho
            dung_san_pham = ton.get("maSanPham") == ma_san_pham

            if dung_kho and dung_san_pham:
                ton["soLuongTon"] = so_luong_moi
                self.ghi_json("kho_hang.json", kho_data)
                return

        danh_sach_ton.append(
            TonKho(ma_kho, ma_san_pham, so_luong_moi).to_dict()
        )

        self.ghi_json("kho_hang.json", kho_data)

    def lay_canh_bao_ton_thap(self):
        kho_data = self.doc_json("kho_hang.json", {})
        hang_data = self.doc_json("hang_hoa.json", {})
        ket_qua = tinh_canh_bao_ton_thap(
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("tonKho", [])),
            hang_data.get("sanPham", []),
            self.loc_theo_kho_duoc_phan_cong(kho_data.get("viTriKho", [])),
        )

        for ton in ket_qua:
            ton["maViTri"] = ton.get("viTriHang", "")

        return ket_qua

    # =========================
    # PHIẾU NHẬP
    # =========================

    def tao_phieu_nhap(
        self,
        ma_nha_san_xuat: str,
        ma_kho: str,
        chi_tiet: List[Dict[str, Any]],
        ngay_nhap=None,
        luu_tam: bool = False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        data = self.doc_json("phieu_nhap.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuNhap", "PN")
        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        phieu = PhieuNhap(
            ma_phieu,
            ma_nha_san_xuat,
            ma_kho,
            self.ma_tai_khoan,
            ngay_nhap or self.lay_ngay_hien_tai(),
            self.tinh_tong_tien(chi_tiet_chuan),
            "Lưu tạm" if luu_tam else "Đã nhập",
            chi_tiet_chuan,
        ).to_dict()

        data.append(phieu)
        self.ghi_json("phieu_nhap.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_nhap(phieu)

        hanh_dong = "Lưu tạm phiếu nhập" if luu_tam else "Thêm phiếu nhập"
        self.ghi_nhat_ky(hanh_dong, "Phiếu nhập", hanh_dong + " " + ma_phieu)

        return phieu

    def cap_nhat_phieu_nhap(
        self,
        ma_phieu_nhap: str,
        ma_nha_san_xuat: str,
        ma_kho: str,
        chi_tiet: List[Dict[str, Any]],
        luu_tam: bool = False,
    ):
        data = self.doc_json("phieu_nhap.json", [])
        phieu = self.tim_phieu(data, "maPhieuNhap", ma_phieu_nhap)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được sửa phiếu nhập đang lưu tạm.")

        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        phieu["maNhaSanXuat"] = ma_nha_san_xuat
        phieu["maKho"] = ma_kho
        phieu["tongTien"] = self.tinh_tong_tien(chi_tiet_chuan)
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã nhập"
        phieu["chiTiet"] = chi_tiet_chuan

        self.ghi_json("phieu_nhap.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_nhap(phieu)

        hanh_dong = "Cập nhật phiếu nhập tạm" if luu_tam else "Xác nhận phiếu nhập"
        self.ghi_nhat_ky(hanh_dong, "Phiếu nhập", hanh_dong + " " + ma_phieu_nhap)

        return phieu

    def cap_nhat_ton_theo_phieu_nhap(self, phieu: Dict[str, Any]):
        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                self.chuyen_so_nguyen(item.get("soLuong", 0)),
                item.get("maViTri", ""),
            )

    # =========================
    # PHIẾU XUẤT
    # =========================

    def xoa_phieu_nhap(self, ma_phieu_nhap: str):
        data = self.doc_json("phieu_nhap.json", [])
        phieu, con_lai = self.tach_phieu(data, "maPhieuNhap", ma_phieu_nhap)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được xóa phiếu nhập đang lưu tạm.")

        self.ghi_json("phieu_nhap.json", con_lai)
        self.ghi_nhat_ky(
            "Xóa phiếu nhập tạm",
            "Phiếu nhập",
            "Xóa phiếu nhập tạm " + ma_phieu_nhap,
        )

        return phieu

    def tao_phieu_xuat(
        self,
        ma_khach_hang: str,
        ma_kho: str,
        chi_tiet: List[Dict[str, Any]],
        ngay_xuat=None,
        luu_tam: bool = False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        if not luu_tam:
            self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

        data = self.doc_json("phieu_xuat.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuXuat", "PX")

        phieu = PhieuXuat(
            ma_phieu,
            ma_kho,
            ma_khach_hang,
            self.ma_tai_khoan,
            ngay_xuat or self.lay_ngay_hien_tai(),
            self.tinh_tong_tien(chi_tiet_chuan),
            "Lưu tạm" if luu_tam else "Đã xuất",
            chi_tiet_chuan,
        ).to_dict()

        data.append(phieu)
        self.ghi_json("phieu_xuat.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_xuat(phieu)

        hanh_dong = "Lưu tạm phiếu xuất" if luu_tam else "Thêm phiếu xuất"
        self.ghi_nhat_ky(hanh_dong, "Phiếu xuất", hanh_dong + " " + ma_phieu)

        return phieu

    def cap_nhat_phieu_xuat(
        self,
        ma_phieu_xuat: str,
        ma_khach_hang: str,
        ma_kho: str,
        chi_tiet: List[Dict[str, Any]],
        luu_tam: bool = False,
    ):
        data = self.doc_json("phieu_xuat.json", [])
        phieu = self.tim_phieu(data, "maPhieuXuat", ma_phieu_xuat)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được sửa phiếu xuất đang lưu tạm.")

        self.kiem_tra_kho_ton_tai(ma_kho)
        self.kiem_tra_chi_tiet_hang(chi_tiet)

        chi_tiet_chuan = self.chuan_hoa_chi_tiet(chi_tiet)

        if not luu_tam:
            self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

        phieu["maKhachHang"] = ma_khach_hang
        phieu["maKho"] = ma_kho
        phieu["tongTien"] = self.tinh_tong_tien(chi_tiet_chuan)
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã xuất"
        phieu["chiTiet"] = chi_tiet_chuan

        self.ghi_json("phieu_xuat.json", data)

        if not luu_tam:
            self.cap_nhat_ton_theo_phieu_xuat(phieu)

        hanh_dong = "Cập nhật phiếu xuất tạm" if luu_tam else "Xác nhận phiếu xuất"
        self.ghi_nhat_ky(hanh_dong, "Phiếu xuất", hanh_dong + " " + ma_phieu_xuat)

        return phieu

    def kiem_tra_du_ton_khi_xuat(self, ma_kho: str, chi_tiet: List[Dict[str, Any]]):
        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))
            so_luong_ton = self.lay_so_luong_ton(ma_kho, ma_san_pham)

            if so_luong_ton < so_luong:
                raise ValueError("Không đủ tồn kho để xuất sản phẩm " + ma_san_pham)

    def cap_nhat_ton_theo_phieu_xuat(self, phieu: Dict[str, Any]):
        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                -self.chuyen_so_nguyen(item.get("soLuong", 0)),
            )

    # =========================
    # KIỂM KÊ
    # =========================

    def xoa_phieu_xuat(self, ma_phieu_xuat: str):
        data = self.doc_json("phieu_xuat.json", [])
        phieu, con_lai = self.tach_phieu(data, "maPhieuXuat", ma_phieu_xuat)

        if not self.la_phieu_luu_tam(phieu):
            raise ValueError("Chỉ được xóa phiếu xuất đang lưu tạm.")

        self.ghi_json("phieu_xuat.json", con_lai)
        self.ghi_nhat_ky(
            "Xóa phiếu xuất tạm",
            "Phiếu xuất",
            "Xóa phiếu xuất tạm " + ma_phieu_xuat,
        )

        return phieu

    def la_phieu_luu_tam(self, phieu: Dict[str, Any]):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()

        return trang_thai in [
            "lưu tạm",
            "luu tam",
            "l?u t?m",
            "chưa xác nhận",
            "chua xac nhan",
        ]

    def tao_phieu_kiem_ke(
        self,
        ma_kho: str,
        chi_tiet: List[Dict[str, Any]],
        ghi_chu: str = "",
        ngay_kiem_ke=None,
        luu_tam: bool = False,
    ):
        self.kiem_tra_kho_ton_tai(ma_kho)

        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết kiểm kê không được rỗng.")

        chi_tiet_chuan = self.chuan_hoa_chi_tiet_kiem_ke(ma_kho, chi_tiet)

        data = self.doc_json("kiem_ke.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maKiemKe", "KK")

        phieu = KiemKe(
            ma_phieu,
            ma_kho,
            ngay_kiem_ke or self.lay_ngay_hien_tai(),
            ghi_chu,
            chi_tiet_chuan,
        ).to_dict()
        phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã kiểm kê"

        data.append(phieu)
        self.ghi_json("kiem_ke.json", data)

        if not luu_tam:
            for item in chi_tiet_chuan:
                self.dat_lai_ton_kho(
                    ma_kho,
                    item.get("maSanPham", ""),
                    self.chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
                )

        hanh_dong = "Lưu tạm kiểm kê" if luu_tam else "Kiểm kê kho"
        self.ghi_nhat_ky(hanh_dong, "Kiểm kê", "Tạo phiếu kiểm kê " + ma_phieu)

        return phieu

    def xoa_phieu_kiem_ke(self, ma_kiem_ke: str, khoi_phuc_ton_cu: bool = True):
        data = self.doc_json("kiem_ke.json", [])
        phieu, con_lai = self.tach_phieu(data, "maKiemKe", ma_kiem_ke)

        if khoi_phuc_ton_cu:
            for item in phieu.get("chiTiet", []):
                self.dat_lai_ton_kho(
                    phieu.get("maKho", ""),
                    item.get("maSanPham", ""),
                    self.chuyen_so_nguyen(item.get("soLuongHeThong", 0)),
                )

        self.ghi_json("kiem_ke.json", con_lai)
        self.ghi_nhat_ky("Xóa phiếu kiểm kê", "Kiểm kê", "Xóa phiếu kiểm kê " + ma_kiem_ke)

        return phieu

    # =========================
    # NHẬT KÝ
    # =========================

    def kiem_tra_kho_ton_tai(self, ma_kho: str):
        if self.tim_kho(ma_kho) is None:
            raise ValueError("Mã kho không tồn tại: " + ma_kho)

    def kiem_tra_san_pham_ton_tai(self, ma_san_pham: str):
        san_pham = self.tim_san_pham(ma_san_pham)
        if san_pham is None:
            raise ValueError("Mã sản phẩm không tồn tại: " + ma_san_pham)
        return san_pham

    def kiem_tra_chi_tiet_hang(self, chi_tiet: List[Dict[str, Any]]):
        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết phiếu không được rỗng.")

        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))
            don_gia = self.chuyen_so_nguyen(item.get("donGia", 0))

            if ma_san_pham == "":
                raise ValueError("Mã sản phẩm không được rỗng.")

            if so_luong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0.")

            if don_gia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0.")

            san_pham = self.kiem_tra_san_pham_ton_tai(ma_san_pham)

            if not self.la_san_pham_dang_kinh_doanh(san_pham):
                raise ValueError("Sản phẩm " + ma_san_pham + " đã ngừng kinh doanh, không thể chọn vào phiếu.")

    # =========================
    # CHUẨN HÓA DỮ LIỆU
    # =========================

    def chuan_hoa_chi_tiet(self, chi_tiet: List[Dict[str, Any]]):
        ket_qua_map = {}

        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = self.chuyen_so_nguyen(item.get("soLuong", 0))

            if ma_san_pham in ket_qua_map:
                ket_qua_map[ma_san_pham]["soLuong"] += so_luong
                continue

            dong = {
                "maSanPham": ma_san_pham,
                "soLuong": so_luong,
                "donGia": self.chuyen_so_nguyen(item.get("donGia", 0)),
            }

            if item.get("maViTri", "") != "":
                dong["maViTri"] = item.get("maViTri", "")

            ket_qua_map[ma_san_pham] = dong

        return list(ket_qua_map.values())

    def chuan_hoa_chi_tiet_kiem_ke(self, ma_kho: str, chi_tiet: List[Dict[str, Any]]):
        ket_qua = []
        san_pham_da_chon = set()

        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong_thuc_te = self.chuyen_so_nguyen(item.get("soLuongThucTe", 0))

            if ma_san_pham == "":
                raise ValueError("Vui lòng chọn sản phẩm kiểm kê.")

            if so_luong_thuc_te < 0:
                raise ValueError("Số lượng thực tế không được âm.")

            if ma_san_pham in san_pham_da_chon:
                raise ValueError("Sản phẩm " + ma_san_pham + " bị trùng trong phiếu kiểm kê.")

            san_pham_da_chon.add(ma_san_pham)
            self.kiem_tra_san_pham_ton_tai(ma_san_pham)

            ket_qua.append({
                "maSanPham": ma_san_pham,
                "soLuongHeThong": self.lay_so_luong_ton(ma_kho, ma_san_pham),
                "soLuongThucTe": so_luong_thuc_te,
            })

        return ket_qua

    def tinh_tong_tien(self, chi_tiet):
        return tinh_tong_tien_chi_tiet(chi_tiet)

    def tach_phieu(
        self,
        danh_sach: List[Dict[str, Any]],
        truong_ma: str,
        ma_phieu: str,
    ):
        phieu_can_xoa = None
        danh_sach_con_lai = []

        for phieu in danh_sach:
            if phieu.get(truong_ma) == ma_phieu:
                phieu_can_xoa = phieu
            else:
                danh_sach_con_lai.append(phieu)

        if phieu_can_xoa is None:
            raise ValueError("Không tìm thấy phiếu: " + ma_phieu)

        return phieu_can_xoa, danh_sach_con_lai

    def tao_ma_tu_dong(
        self,
        danh_sach: List[Dict[str, Any]],
        truong_ma: str,
        tien_to: str,
    ):
        so_lon_nhat = 0

        for item in danh_sach:
            ma = str(item.get(truong_ma, ""))

            if ma.startswith(tien_to):
                phan_so = ma.replace(tien_to, "")

                if phan_so.isdigit():
                    so_lon_nhat = max(so_lon_nhat, int(phan_so))

        return tien_to + str(so_lon_nhat + 1).zfill(4)

    def chuyen_so_nguyen(self, value: Any):
        return chuyen_so_nguyen(value)

    def lay_ngay_hien_tai(self):
        return date.today().strftime("%Y-%m-%d")

    def lay_thoi_gian_hien_tai(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
