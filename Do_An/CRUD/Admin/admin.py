from __future__ import annotations

import json
import os
from datetime import datetime

from CRUD.Admin.nhanvien import NhanVien
from CRUD.Admin.taikhoan import TaiKhoan
from CRUD.Admin.danhmuc import DanhMuc
from CRUD.Shared.khohang import KhoHang
from CRUD.Shared.hanghoa import HangHoa
from CRUD.Shared.thongke import ThongKe


class NghiepVuAdmin(
    NhanVien,
    TaiKhoan,
    DanhMuc,
    KhoHang,
    HangHoa,
    ThongKe,
):
    """Xu ly nghiep vu cua Admin."""

    def __init__(self, thu_muc_goc=None, tai_khoan_dang_nhap=None):
        self.thu_muc_goc = thu_muc_goc or self.lay_thu_muc_goc()
        self.thu_muc_data = os.path.join(self.thu_muc_goc, "Data")
        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap or {}
        self.ma_tai_khoan = self.tai_khoan_dang_nhap.get("maTaiKhoan", "")

        self.ten_vai_tro = "Admin"
        self.la_quyen_admin = True

    def lay_thu_muc_goc(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def lay_duong_dan_file(self, ten_file):
        return os.path.join(self.thu_muc_data, ten_file)

    def doc_json(self, ten_file, mac_dinh=None):
        if mac_dinh is None:
            mac_dinh = {}

        duong_dan = self.lay_duong_dan_file(ten_file)

        if not os.path.exists(duong_dan):
            return mac_dinh

        try:
            with open(duong_dan, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return mac_dinh

    def ghi_json(self, ten_file, data):
        duong_dan = self.lay_duong_dan_file(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def tim_item(self, danh_sach, truong_ma, ma):
        for item in danh_sach:
            if item.get(truong_ma, "") == ma:
                return item
        return None

    def dem_dong_theo_ma(self, danh_sach, truong_ma, ma):
        dem = 0

        for item in danh_sach:
            if item.get(truong_ma, "") == ma:
                dem += 1

        return dem

    def kiem_tra_trung_gia_tri(self, danh_sach, ten_truong, gia_tri, ten_hien_thi, truong_ma, ma_bo_qua=""):
        gia_tri = str(gia_tri).strip().lower()

        if gia_tri == "":
            return

        for item in danh_sach:
            if item.get(truong_ma, "") == ma_bo_qua:
                continue

            gia_tri_hien_tai = str(item.get(ten_truong, "")).strip().lower()

            if gia_tri_hien_tai == gia_tri:
                raise ValueError(ten_hien_thi + " đã tồn tại.")

    def tao_ma_tu_dong_do_dai(self, danh_sach, truong_ma, tien_to, do_dai_so):
        so_lon_nhat = 0

        for item in danh_sach:
            ma = str(item.get(truong_ma, ""))

            if ma.startswith(tien_to):
                phan_so = ma.replace(tien_to, "")

                if phan_so.isdigit():
                    so_hien_tai = int(phan_so)

                    if so_hien_tai > so_lon_nhat:
                        so_lon_nhat = so_hien_tai

        return tien_to + str(so_lon_nhat + 1).zfill(do_dai_so)

    def tao_ma_tu_dong(self, danh_sach, truong_ma, tien_to):
        return self.tao_ma_tu_dong_do_dai(danh_sach, truong_ma, tien_to, 4)

    def lay_thoi_gian_hien_tai(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def ghi_nhat_ky(self, hanh_dong, doi_tuong, ghi_chu):
        data = self.doc_json("nhat_ky.json", [])
        ma_nhat_ky = self.tao_ma_tu_dong(data, "maNhatKy", "NK")

        data.append({
            "maNhatKy": ma_nhat_ky,
            "maTaiKhoan": self.ma_tai_khoan,
            "hanhDong": hanh_dong,
            "doiTuong": doi_tuong,
            "thoiGian": self.lay_thoi_gian_hien_tai(),
            "trangThai": "Thành công",
            "ghiChu": ghi_chu,
        })

        self.ghi_json("nhat_ky.json", data)

    def lay_ma_tai_khoan_hien_tai(self):
        return self.ma_tai_khoan

    def lay_ma_nhan_vien_hien_tai(self):
        data = self.doc_json("nguoi_dung.json", {})

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") == self.ma_tai_khoan:
                return tai_khoan.get("maNhanVien", "")

        return ""


AdminCRUD = NghiepVuAdmin