from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional


class NghiepVuAdmin:

    def __init__(self, thu_muc_goc: Optional[str] = None, tai_khoan_dang_nhap: Optional[Dict[str, Any]] = None):
        self.thu_muc_goc = thu_muc_goc or self.lay_thu_muc_goc()
        self.thu_muc_data = os.path.join(self.thu_muc_goc, "Data")
        self.tai_khoan_dang_nhap = tai_khoan_dang_nhap or {}

    def lay_thu_muc_goc(self):
        thu_muc = os.path.dirname(os.path.abspath(__file__))

        while True:
            if os.path.exists(os.path.join(thu_muc, "Data")):
                return thu_muc

            thu_muc_cha = os.path.dirname(thu_muc)

            if thu_muc_cha == thu_muc:
                return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            thu_muc = thu_muc_cha

    def lay_duong_dan_file(self, ten_file: str):
        return os.path.join(self.thu_muc_data, ten_file)

    def doc_json(self, ten_file: str, mac_dinh: Any = None):
        duong_dan = self.lay_duong_dan_file(ten_file)

        if not os.path.exists(duong_dan):
            return deepcopy(mac_dinh)

        for encoding in ["utf-8-sig", "utf-8", "cp1258"]:
            try:
                with open(duong_dan, "r", encoding=encoding) as file:
                    return json.load(file)
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

        return deepcopy(mac_dinh)

    def ghi_json(self, ten_file: str, data: Any):
        duong_dan = self.lay_duong_dan_file(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def lay_ma_tai_khoan_hien_tai(self):
        return self.tai_khoan_dang_nhap.get("maTaiKhoan", "TK001")

    def lay_ma_nhan_vien_hien_tai(self):
        return self.tai_khoan_dang_nhap.get("maNhanVien", "")

    def lay_ten_admin_hien_tai(self):
        ma_nhan_vien = self.lay_ma_nhan_vien_hien_tai()
        data = self.doc_json("nguoi_dung.json", {})

        for nhan_vien in data.get("nhanVien", []):
            if nhan_vien.get("maNhanVien") == ma_nhan_vien:
                return nhan_vien.get("tenNhanVien", "Admin")

        return self.tai_khoan_dang_nhap.get("tenTaiKhoan", "Admin")

    def lay_vai_tro_tai_khoan(self, ma_tai_khoan: str):
        data = self.doc_json("nguoi_dung.json", {})
        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            vai_tro_map[vai_tro.get("maVaiTro", "")] = vai_tro.get("tenVaiTro", "")

        ket_qua = []
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                ket_qua.append(vai_tro_map.get(phan_quyen.get("maVaiTro", ""), ""))

        return ket_qua

    def la_tai_khoan_admin(self, ma_tai_khoan: str = "", ma_nhan_vien: str = ""):
        data = self.doc_json("nguoi_dung.json", {})

        if ma_tai_khoan == "" and ma_nhan_vien != "":
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien") == ma_nhan_vien:
                    ma_tai_khoan = tai_khoan.get("maTaiKhoan", "")
                    break

        for ten_vai_tro in self.lay_vai_tro_tai_khoan(ma_tai_khoan):
            if str(ten_vai_tro).lower() in ["admin", "quan tri", "quan tri vien"]:
                return True

        return False

    def la_tai_khoan_dang_dung(self, ma_tai_khoan: str = "", ma_nhan_vien: str = ""):
        if ma_tai_khoan != "" and ma_tai_khoan == self.lay_ma_tai_khoan_hien_tai():
            return True

        if ma_nhan_vien != "" and ma_nhan_vien == self.lay_ma_nhan_vien_hien_tai():
            return True

        return False

    def lay_trang_thai_moi(self, trang_thai_hien_tai: Any):
        trang_thai = str(trang_thai_hien_tai).strip().lower()

        if trang_thai in ["true", "1", "hoat dong", "hoạt động", "dang hoat dong", "đang hoạt động", "active", "mo", "mở"]:
            return "Đã khóa"

        return "Hoạt động"

    def doc_nguoi_dung(self):
        return self.doc_json("nguoi_dung.json", {})

    def ghi_nguoi_dung(self, data):
        self.ghi_json("nguoi_dung.json", data)

    def khoa_mo_nhan_vien(self, ma_nhan_vien: str):
        if self.la_tai_khoan_dang_dung(ma_nhan_vien=ma_nhan_vien):
            raise ValueError("Không thể khóa/mở chính nhân viên đang đăng nhập.")

        data = self.doc_nguoi_dung()
        da_tim_thay = False
        trang_thai_moi = ""

        for item in data.get("nhanVien", []):
            if item.get("maNhanVien") == ma_nhan_vien:
                trang_thai_moi = self.lay_trang_thai_moi(item.get("trangThai", ""))
                item["trangThai"] = trang_thai_moi
                da_tim_thay = True
                break

        if not da_tim_thay:
            raise ValueError("Không tìm thấy nhân viên đã chọn.")

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maNhanVien") == ma_nhan_vien:
                tai_khoan["trangThai"] = trang_thai_moi

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Khóa/Mở khóa", "Nhân viên", "Cập nhật trạng thái " + ma_nhan_vien + " thành " + trang_thai_moi)

        return trang_thai_moi

    def khoa_mo_tai_khoan(self, ma_tai_khoan: str):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể khóa/mở chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        da_tim_thay = False
        trang_thai_moi = ""

        for item in data.get("taiKhoan", []):
            if item.get("maTaiKhoan") == ma_tai_khoan:
                trang_thai_moi = self.lay_trang_thai_moi(item.get("trangThai", ""))
                item["trangThai"] = trang_thai_moi
                da_tim_thay = True
                break

        if not da_tim_thay:
            raise ValueError("Không tìm thấy tài khoản đã chọn.")

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Khóa/Mở khóa", "Tài khoản", "Cập nhật trạng thái " + ma_tai_khoan + " thành " + trang_thai_moi)

        return trang_thai_moi

    def reset_mat_khau_tai_khoan(self, ma_tai_khoan: str):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể reset mật khẩu của chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        mat_khau_moi = "123456"
        da_tim_thay = False

        for item in data.get("taiKhoan", []):
            if item.get("maTaiKhoan") == ma_tai_khoan:
                item["matKhau"] = mat_khau_moi
                da_tim_thay = True
                break

        if not da_tim_thay:
            raise ValueError("Không tìm thấy tài khoản đã chọn.")

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Reset mật khẩu", "Tài khoản", "Reset mật khẩu " + ma_tai_khoan)

        return mat_khau_moi

    def tao_ma_tu_dong(self, danh_sach: List[Dict[str, Any]], truong_ma: str, tien_to: str):
        so_lon_nhat = 0

        for item in danh_sach:
            ma = str(item.get(truong_ma, ""))

            if ma.startswith(tien_to):
                phan_so = ma.replace(tien_to, "")

                if phan_so.isdigit():
                    so_lon_nhat = max(so_lon_nhat, int(phan_so))

        return tien_to + str(so_lon_nhat + 1).zfill(4)

    def ghi_nhat_ky(self, hanh_dong: str, doi_tuong: str, ghi_chu: str):
        data = self.doc_json("nhat_ky.json", [])

        if not isinstance(data, list):
            data = []

        data.append({
            "maNhatKy": self.tao_ma_tu_dong(data, "maNhatKy", "NK"),
            "maTaiKhoan": self.lay_ma_tai_khoan_hien_tai(),
            "hanhDong": hanh_dong,
            "doiTuong": doi_tuong,
            "thoiGian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trangThai": "Thành công",
            "ghiChu": ghi_chu,
        })

        self.ghi_json("nhat_ky.json", data)


AdminCRUD = NghiepVuAdmin
