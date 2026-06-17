from __future__ import annotations

import json
import os
import re
from copy import deepcopy
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from Calculator.common import chuyen_so_nguyen
from Calculator.phieu import tinh_tong_tien_chi_tiet
from Class.sanpham import SanPham
from Class.tonkho import TonKho


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

    def chuan_hoa_text_so_sanh(self, value: Any):
        return " ".join(str(value).strip().lower().split())

    def kiem_tra_trung_gia_tri(self, danh_sach: List[Dict[str, Any]], truong: str, value: Any, ten_truong: str, truong_ma: str = "", ma_bo_qua: str = ""):
        value_chuan = self.chuan_hoa_text_so_sanh(value)

        if value_chuan == "":
            return

        for item in danh_sach:
            if truong_ma != "" and item.get(truong_ma, "") == ma_bo_qua:
                continue

            if self.chuan_hoa_text_so_sanh(item.get(truong, "")) == value_chuan:
                raise ValueError(ten_truong + " đã tồn tại.")

    def kiem_tra_so_dien_thoai_vn(self, value: Any, ten_truong: str = "Số điện thoại", bat_buoc: bool = False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + ten_truong.lower() + ".")
            return value

        if not re.fullmatch(r"0\d{9}", value):
            raise ValueError(ten_truong + " phải bắt đầu bằng 0 và đúng 10 số.")

        return value

    def kiem_tra_email_gmail(self, value: Any, ten_truong: str = "Email", bat_buoc: bool = False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + ten_truong.lower() + ".")
            return value

        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@gmail\.com", value):
            raise ValueError(ten_truong + " phải đúng định dạng và có đuôi @gmail.com.")

        return value

    def kiem_tra_ngay_sinh(self, value: Any, bat_buoc: bool = False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập ngày sinh.")
            return value

        try:
            ngay_sinh = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Ngày sinh phải đúng định dạng yyyy-mm-dd và là ngày hợp lệ.")

        hom_nay = date.today()

        if ngay_sinh > hom_nay:
            raise ValueError("Ngày sinh không được lớn hơn ngày hiện tại.")

        tuoi = hom_nay.year - ngay_sinh.year - ((hom_nay.month, hom_nay.day) < (ngay_sinh.month, ngay_sinh.day))

        if tuoi < 18:
            raise ValueError("Nhân viên phải từ 18 tuổi trở lên.")

        if tuoi > 65:
            raise ValueError("Tuổi nhân viên không hợp lý.")

        return value

    def la_san_pham_dang_kinh_doanh(self, san_pham: Dict[str, Any]):
        trang_thai = str(san_pham.get("trangThai", "")).strip().lower()
        return trang_thai not in ["ngừng kinh doanh", "ngung kinh doanh", "đã ngừng", "da ngung", "false", "0", "inactive"]

    def tao_ma_tu_dong_do_dai(self, danh_sach: List[Dict[str, Any]], truong_ma: str, tien_to: str, do_dai_so: int):
        so_lon_nhat = 0

        for item in danh_sach:
            ma_hien_tai = str(item.get(truong_ma, ""))

            if ma_hien_tai.startswith(tien_to):
                phan_so = ma_hien_tai.replace(tien_to, "")

                if phan_so.isdigit():
                    so_lon_nhat = max(so_lon_nhat, int(phan_so))

        return tien_to + str(so_lon_nhat + 1).zfill(do_dai_so)

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

    def la_trang_thai_khoa(self, trang_thai: Any):
        trang_thai_text = str(trang_thai).strip().lower()
        return trang_thai_text in ["false", "0", "đã khóa", "da khoa", "khóa", "khoa", "inactive"]

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

    def xoa_tai_khoan(self, ma_tai_khoan: str):
        if self.la_tai_khoan_dang_dung(ma_tai_khoan=ma_tai_khoan):
            raise ValueError("Không thể xóa chính tài khoản đang đăng nhập.")

        data = self.doc_nguoi_dung()
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần xóa.")
        if not self.la_trang_thai_khoa(tai_khoan.get("trangThai", "")):
            raise ValueError("Chỉ được xóa tài khoản đang ở trạng thái Đã khóa.")

        data["taiKhoan"] = [
            item for item in data.get("taiKhoan", [])
            if item.get("maTaiKhoan", "") != ma_tai_khoan
        ]
        data["phanQuyen"] = [
            item for item in data.get("phanQuyen", [])
            if item.get("maTaiKhoan", "") != ma_tai_khoan
        ]
        data["phanCongKho"] = [
            item for item in data.get("phanCongKho", [])
            if item.get("maTaiKhoan", "") != ma_tai_khoan
        ]

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin xóa Tài khoản", "Tài khoản", "Xóa " + ma_tai_khoan)
        return tai_khoan

    def xoa_nhan_vien(self, ma_nhan_vien: str):
        if self.la_tai_khoan_dang_dung(ma_nhan_vien=ma_nhan_vien):
            raise ValueError("Không thể xóa chính nhân viên đang đăng nhập.")

        data = self.doc_nguoi_dung()
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên cần xóa.")
        if not self.la_trang_thai_khoa(nhan_vien.get("trangThai", "")):
            raise ValueError("Chỉ được xóa nhân viên đang ở trạng thái Đã khóa.")

        tai_khoan_lien_ket = [
            item for item in data.get("taiKhoan", [])
            if item.get("maNhanVien", "") == ma_nhan_vien
        ]

        for tai_khoan in tai_khoan_lien_ket:
            if not self.la_trang_thai_khoa(tai_khoan.get("trangThai", "")):
                raise ValueError("Tài khoản liên kết " + tai_khoan.get("maTaiKhoan", "") + " chưa bị khóa.")

        danh_sach_ma_tai_khoan = [item.get("maTaiKhoan", "") for item in tai_khoan_lien_ket]

        data["nhanVien"] = [
            item for item in data.get("nhanVien", [])
            if item.get("maNhanVien", "") != ma_nhan_vien
        ]
        data["taiKhoan"] = [
            item for item in data.get("taiKhoan", [])
            if item.get("maNhanVien", "") != ma_nhan_vien
        ]
        data["phanQuyen"] = [
            item for item in data.get("phanQuyen", [])
            if item.get("maTaiKhoan", "") not in danh_sach_ma_tai_khoan
        ]
        data["phanCongKho"] = [
            item for item in data.get("phanCongKho", [])
            if item.get("maTaiKhoan", "") not in danh_sach_ma_tai_khoan
        ]

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin xóa Nhân viên", "Nhân viên", "Xóa " + ma_nhan_vien)
        return nhan_vien

    def kiem_tra_thong_tin_nhan_vien(self, data: Dict[str, Any], du_lieu: Dict[str, Any], ma_bo_qua: str = ""):
        self.kiem_tra_ngay_sinh(du_lieu.get("ngaySinh", ""), False)
        self.kiem_tra_so_dien_thoai_vn(du_lieu.get("soDienThoai", ""), "Số điện thoại", False)
        self.kiem_tra_email_gmail(du_lieu.get("email", ""), "Email", False)
        self.kiem_tra_trung_gia_tri(data.get("nhanVien", []), "soDienThoai", du_lieu.get("soDienThoai", ""), "Số điện thoại nhân viên", "maNhanVien", ma_bo_qua)
        self.kiem_tra_trung_gia_tri(data.get("nhanVien", []), "email", du_lieu.get("email", ""), "Email nhân viên", "maNhanVien", ma_bo_qua)

    def tao_nhan_vien(self, du_lieu: Dict[str, Any]):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_nhan_vien(data, du_lieu)
        danh_sach = data.setdefault("nhanVien", [])
        ma_nhan_vien = self.tao_ma_tu_dong_do_dai(danh_sach, "maNhanVien", "NV", 3)
        dong = dict(du_lieu)
        dong["maNhanVien"] = ma_nhan_vien
        danh_sach.append(dong)
        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Nhân viên", "Nhân viên", "Thêm " + ma_nhan_vien)
        return dong

    def kiem_tra_thong_tin_tai_khoan(self, data: Dict[str, Any], du_lieu: Dict[str, Any], ma_bo_qua: str = ""):
        self.kiem_tra_trung_gia_tri(data.get("taiKhoan", []), "tenTaiKhoan", du_lieu.get("tenTaiKhoan", ""), "Tên tài khoản", "maTaiKhoan", ma_bo_qua)

        ma_nhan_vien = du_lieu.get("maNhanVien", "")
        if ma_nhan_vien == "":
            raise ValueError("Vui lòng chọn nhân viên.")

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maTaiKhoan", "") != ma_bo_qua and tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                raise ValueError("Nhân viên này đã có tài khoản.")

    def tao_tai_khoan(self, du_lieu: Dict[str, Any], ma_vai_tro: str):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_tai_khoan(data, du_lieu)
        danh_sach = data.setdefault("taiKhoan", [])
        ma_tai_khoan = self.tao_ma_tu_dong_do_dai(danh_sach, "maTaiKhoan", "TK", 3)
        dong = dict(du_lieu)
        dong["maTaiKhoan"] = ma_tai_khoan
        danh_sach.append(dong)
        data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})
        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Tài khoản", "Tài khoản", "Thêm " + ma_tai_khoan)
        return dong

    def cap_nhat_tai_khoan(self, ma_tai_khoan: str, du_lieu: Dict[str, Any], ma_vai_tro: str):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_tai_khoan(data, du_lieu, ma_tai_khoan)
        tai_khoan = self.tim_item(data.get("taiKhoan", []), "maTaiKhoan", ma_tai_khoan)

        if tai_khoan is None:
            raise ValueError("Không tìm thấy tài khoản cần sửa.")

        tai_khoan.update(du_lieu)
        tai_khoan["maTaiKhoan"] = ma_tai_khoan

        da_cap_nhat = False
        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                phan_quyen["maVaiTro"] = ma_vai_tro
                da_cap_nhat = True
                break

        if not da_cap_nhat:
            data.setdefault("phanQuyen", []).append({"maTaiKhoan": ma_tai_khoan, "maVaiTro": ma_vai_tro})

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin sửa Tài khoản", "Tài khoản", "Sửa " + ma_tai_khoan)
        return tai_khoan

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

    def kiem_tra_thong_tin_san_pham(
        self,
        ten_san_pham: str,
        ma_loai_hang: str,
        ma_don_vi_tinh: str,
        don_gia: int,
        muc_ton_toi_thieu: int,
    ):
        if str(ten_san_pham).strip() == "":
            raise ValueError("Vui lòng nhập tên sản phẩm.")
        if ma_loai_hang == "":
            raise ValueError("Vui lòng chọn loại hàng.")
        if ma_don_vi_tinh == "":
            raise ValueError("Vui lòng chọn đơn vị tính.")
        if chuyen_so_nguyen(don_gia) <= 0:
            raise ValueError("Đơn giá phải lớn hơn 0.")
        if chuyen_so_nguyen(muc_ton_toi_thieu) < 0:
            raise ValueError("Mức tồn tối thiểu không được âm.")

        data = self.doc_json("hang_hoa.json", {})

        if self.tim_item(data.get("loaiHang", []), "maLoaiHang", ma_loai_hang) is None:
            raise ValueError("Loại hàng không tồn tại.")

        if self.tim_item(data.get("donViTinh", []), "maDonViTinh", ma_don_vi_tinh) is None:
            raise ValueError("Đơn vị tính không tồn tại.")

    def kiem_tra_trung_ten_san_pham(self, data: Dict[str, Any], ten_san_pham: str, ma_bo_qua: str = ""):
        self.kiem_tra_trung_gia_tri(data.get("sanPham", []), "tenSanPham", ten_san_pham, "Tên sản phẩm", "maSanPham", ma_bo_qua)

    def tao_san_pham(
        self,
        ten_san_pham: str,
        ma_loai_hang: str,
        ma_don_vi_tinh: str,
        don_gia: int,
        muc_ton_toi_thieu: int,
    ):
        self.kiem_tra_thong_tin_san_pham(
            ten_san_pham,
            ma_loai_hang,
            ma_don_vi_tinh,
            don_gia,
            muc_ton_toi_thieu,
        )

        data = self.doc_json("hang_hoa.json", {})
        danh_sach = data.setdefault("sanPham", [])
        self.kiem_tra_trung_ten_san_pham(data, ten_san_pham)
        ma_san_pham = self.tao_ma_tu_dong(danh_sach, "maSanPham", "SP")

        san_pham = SanPham(
            ma_san_pham,
            ten_san_pham.strip(),
            ma_don_vi_tinh,
            ma_loai_hang,
            chuyen_so_nguyen(don_gia),
            chuyen_so_nguyen(muc_ton_toi_thieu),
        ).to_dict()

        danh_sach.append(san_pham)
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Admin thêm sản phẩm", "Hàng hóa", "Tạo sản phẩm " + ma_san_pham)
        return san_pham

    def sua_san_pham(
        self,
        ma_san_pham: str,
        ten_san_pham: str,
        ma_loai_hang: str,
        ma_don_vi_tinh: str,
        don_gia: int,
        muc_ton_toi_thieu: int,
    ):
        self.kiem_tra_thong_tin_san_pham(
            ten_san_pham,
            ma_loai_hang,
            ma_don_vi_tinh,
            don_gia,
            muc_ton_toi_thieu,
        )

        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)

        if san_pham is None:
            raise ValueError("Không tìm thấy sản phẩm.")

        self.kiem_tra_trung_ten_san_pham(data, ten_san_pham, ma_san_pham)
        san_pham["tenSanPham"] = ten_san_pham.strip()
        san_pham["maLoaiHang"] = ma_loai_hang
        san_pham["maDonViTinh"] = ma_don_vi_tinh
        san_pham["donGia"] = chuyen_so_nguyen(don_gia)
        san_pham["mucTonToiThieu"] = chuyen_so_nguyen(muc_ton_toi_thieu)

        if san_pham.get("trangThai", "") == "":
            san_pham["trangThai"] = "Đang kinh doanh"

        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Admin sửa sản phẩm", "Hàng hóa", "Cập nhật sản phẩm " + ma_san_pham)
        return san_pham

    def ngung_kinh_doanh_san_pham(self, ma_san_pham: str):
        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)

        if san_pham is None:
            raise ValueError("Không tìm thấy sản phẩm.")

        san_pham["trangThai"] = "Ngừng kinh doanh"
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Admin ngừng kinh doanh sản phẩm", "Hàng hóa", "Ngừng kinh doanh " + ma_san_pham)
        return san_pham

    def doi_trang_thai_kinh_doanh_san_pham(self, ma_san_pham: str):
        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)

        if san_pham is None:
            raise ValueError("Không tìm thấy sản phẩm.")

        trang_thai = str(san_pham.get("trangThai", "")).strip().lower()

        if trang_thai in ["ngừng kinh doanh", "ngung kinh doanh", "đã ngừng", "da ngung", "false", "0", "inactive"]:
            trang_thai_moi = "Hoạt động"
        else:
            trang_thai_moi = "Ngừng kinh doanh"

        san_pham["trangThai"] = trang_thai_moi
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky(
            "Admin đổi trạng thái sản phẩm",
            "Hàng hóa",
            "Đổi trạng thái " + ma_san_pham + " thành " + trang_thai_moi,
        )
        return san_pham

    def them_danh_muc_json(
        self,
        ten_file: str,
        danh_muc: str,
        truong_ma: str,
        tien_to: str,
        du_lieu: Dict[str, Any],
        ten_doi_tuong: str,
        do_dai_so: int = 4,
    ):
        data = self.doc_json(ten_file, {})
        danh_sach = data.setdefault(danh_muc, [])
        self.kiem_tra_danh_muc_truoc_luu(data, danh_muc, truong_ma, "", du_lieu)
        ma_moi = self.tao_ma_tu_dong_do_dai(danh_sach, truong_ma, tien_to, do_dai_so)
        dong = dict(du_lieu)
        dong[truong_ma] = ma_moi
        danh_sach.append(dong)
        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin thêm " + ten_doi_tuong, ten_doi_tuong, "Thêm " + ma_moi)
        return dong

    def sua_danh_muc_json(
        self,
        ten_file: str,
        danh_muc: str,
        truong_ma: str,
        ma: str,
        du_lieu: Dict[str, Any],
        ten_doi_tuong: str,
    ):
        data = self.doc_json(ten_file, {})
        item = self.tim_item(data.get(danh_muc, []), truong_ma, ma)

        if item is None:
            raise ValueError("Không tìm thấy dữ liệu cần sửa.")

        self.kiem_tra_danh_muc_truoc_luu(data, danh_muc, truong_ma, ma, du_lieu)
        item.update(du_lieu)
        item[truong_ma] = ma
        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin sửa " + ten_doi_tuong, ten_doi_tuong, "Sửa " + ma)
        return item

    def kiem_tra_danh_muc_truoc_luu(self, data: Dict[str, Any], danh_muc: str, truong_ma: str, ma_bo_qua: str, du_lieu: Dict[str, Any]):
        danh_sach = data.get(danh_muc, [])

        cau_hinh_ten = {
            "kho": ("tenKho", "Tên kho"),
            "loaiHang": ("tenLoaiHang", "Tên loại hàng"),
            "donViTinh": ("tenDonViTinh", "Tên đơn vị tính"),
            "nhaSanXuat": ("tenNhaSanXuat", "Tên nhà sản xuất"),
            "khachHang": ("tenKhachHang", "Tên khách hàng"),
        }

        if danh_muc in cau_hinh_ten:
            truong_ten, ten_truong = cau_hinh_ten[danh_muc]
            self.kiem_tra_trung_gia_tri(danh_sach, truong_ten, du_lieu.get(truong_ten, ""), ten_truong, truong_ma, ma_bo_qua)

        if danh_muc in ["nhaSanXuat", "khachHang"]:
            self.kiem_tra_so_dien_thoai_vn(du_lieu.get("soDienThoai", ""), "Số điện thoại", False)
            self.kiem_tra_email_gmail(du_lieu.get("email", ""), "Email", False)
            self.kiem_tra_trung_gia_tri(danh_sach, "soDienThoai", du_lieu.get("soDienThoai", ""), "Số điện thoại", truong_ma, ma_bo_qua)
            self.kiem_tra_trung_gia_tri(danh_sach, "email", du_lieu.get("email", ""), "Email", truong_ma, ma_bo_qua)

        if danh_muc == "kho":
            self.kiem_tra_so_dien_thoai_vn(du_lieu.get("soDienThoai", ""), "Số điện thoại", False)
            self.kiem_tra_trung_gia_tri(danh_sach, "soDienThoai", du_lieu.get("soDienThoai", ""), "Số điện thoại kho", truong_ma, ma_bo_qua)

    def cap_nhat_nhan_vien(self, ma_nhan_vien: str, du_lieu: Dict[str, Any]):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_nhan_vien(data, du_lieu, ma_nhan_vien)
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên cần sửa.")

        nhan_vien.update(du_lieu)
        nhan_vien["maNhanVien"] = ma_nhan_vien

        if "trangThai" in du_lieu:
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien") == ma_nhan_vien:
                    tai_khoan["trangThai"] = du_lieu.get("trangThai", "")

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin sửa Nhân viên", "Nhân viên", "Sửa " + ma_nhan_vien)
        return nhan_vien

    def xoa_danh_muc_json(
        self,
        ten_file: str,
        danh_muc: str,
        truong_ma: str,
        ma: str,
        ten_doi_tuong: str,
    ):
        self.kiem_tra_truoc_xoa_danh_muc(ten_file, danh_muc, ma, ten_doi_tuong)
        data = self.doc_json(ten_file, {})
        danh_sach = data.get(danh_muc, [])
        con_lai = []
        da_tim_thay = False

        for item in danh_sach:
            if item.get(truong_ma) == ma:
                da_tim_thay = True
            else:
                con_lai.append(item)

        if not da_tim_thay:
            raise ValueError("Không tìm thấy dữ liệu cần xóa.")

        data[danh_muc] = con_lai
        self.ghi_json(ten_file, data)
        self.ghi_nhat_ky("Admin xóa " + ten_doi_tuong, ten_doi_tuong, "Xóa " + ma)
        return True

    def kiem_tra_truoc_xoa_danh_muc(self, ten_file: str, danh_muc: str, ma: str, ten_doi_tuong: str):
        if ten_file == "hang_hoa.json" and danh_muc == "donViTinh":
            hang_data = self.doc_json("hang_hoa.json", {})
            so_san_pham = self.dem_dong_theo_ma(hang_data.get("sanPham", []), "maDonViTinh", ma)

            if so_san_pham > 0:
                raise ValueError(self.tao_thong_bao_dang_duoc_su_dung("đơn vị tính", ma, [str(so_san_pham) + " sản phẩm"]))

        if ten_file == "doi_tac.json" and danh_muc == "khachHang":
            phieu_xuat = self.doc_json("phieu_xuat.json", [])
            so_phieu_xuat = self.dem_dong_theo_ma(phieu_xuat, "maKhachHang", ma)

            if so_phieu_xuat > 0:
                raise ValueError(self.tao_thong_bao_dang_duoc_su_dung("khách hàng", ma, [str(so_phieu_xuat) + " phiếu xuất"]))

    def tao_thong_bao_dang_duoc_su_dung(self, ten_doi_tuong: str, ma: str, danh_sach_lien_quan: List[str]):
        return "Không thể xóa vì ràng buộc dữ liệu."

    def dem_dong_theo_ma(self, danh_sach: List[Dict[str, Any]], truong_ma: str, ma: str):
        so_luong = 0

        for item in danh_sach:
            if item.get(truong_ma, "") == ma:
                so_luong += 1

        return so_luong

    def xoa_kho(self, ma_kho: str):
        kho_data = self.doc_json("kho_hang.json", {})
        nguoi_dung = self.doc_json("nguoi_dung.json", {})
        phieu_nhap = self.doc_json("phieu_nhap.json", [])
        phieu_xuat = self.doc_json("phieu_xuat.json", [])
        kiem_ke = self.doc_json("kiem_ke.json", [])
        lien_quan = []

        so_ton = self.dem_dong_theo_ma(kho_data.get("tonKho", []), "maKho", ma_kho)
        so_vi_tri = self.dem_dong_theo_ma(kho_data.get("viTriKho", []), "maKho", ma_kho)
        so_phan_cong = self.dem_dong_theo_ma(nguoi_dung.get("phanCongKho", []), "maKho", ma_kho)
        so_phieu_nhap = self.dem_dong_theo_ma(phieu_nhap, "maKho", ma_kho)
        so_phieu_xuat = self.dem_dong_theo_ma(phieu_xuat, "maKho", ma_kho)
        so_kiem_ke = self.dem_dong_theo_ma(kiem_ke, "maKho", ma_kho)

        if so_ton > 0:
            lien_quan.append(str(so_ton) + " dòng tồn kho")
        if so_vi_tri > 0:
            lien_quan.append(str(so_vi_tri) + " vị trí kho")
        if so_phan_cong > 0:
            lien_quan.append(str(so_phan_cong) + " phân công kho")
        if so_phieu_nhap > 0:
            lien_quan.append(str(so_phieu_nhap) + " phiếu nhập")
        if so_phieu_xuat > 0:
            lien_quan.append(str(so_phieu_xuat) + " phiếu xuất")
        if so_kiem_ke > 0:
            lien_quan.append(str(so_kiem_ke) + " phiếu kiểm kê")

        if len(lien_quan) > 0:
            raise ValueError(self.tao_thong_bao_dang_duoc_su_dung("kho", ma_kho, lien_quan))

        return self.xoa_danh_muc_json("kho_hang.json", "kho", "maKho", ma_kho, "Kho")

    def xoa_loai_hang(self, ma_loai_hang: str):
        hang_data = self.doc_json("hang_hoa.json", {})
        so_san_pham = self.dem_dong_theo_ma(hang_data.get("sanPham", []), "maLoaiHang", ma_loai_hang)

        if so_san_pham > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    "loại hàng",
                    ma_loai_hang,
                    [str(so_san_pham) + " sản phẩm"],
                )
            )

        return self.xoa_danh_muc_json("hang_hoa.json", "loaiHang", "maLoaiHang", ma_loai_hang, "Loại hàng")

    def xoa_nha_san_xuat(self, ma_nha_san_xuat: str):
        phieu_nhap = self.doc_json("phieu_nhap.json", [])
        so_phieu_nhap = self.dem_dong_theo_ma(phieu_nhap, "maNhaSanXuat", ma_nha_san_xuat)

        if so_phieu_nhap > 0:
            raise ValueError(
                self.tao_thong_bao_dang_duoc_su_dung(
                    "nhà sản xuất",
                    ma_nha_san_xuat,
                    [str(so_phieu_nhap) + " phiếu nhập"],
                )
            )

        return self.xoa_danh_muc_json("doi_tac.json", "nhaSanXuat", "maNhaSanXuat", ma_nha_san_xuat, "Nhà sản xuất")

    def lay_ngay_hien_tai(self):
        return datetime.now().strftime("%Y-%m-%d")

    def la_phieu_luu_tam(self, phieu: Dict[str, Any]):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()
        return trang_thai in ["lưu tạm", "luu tam", "lưu tạm", "chưa xác nhận", "chua xac nhan"]

    def la_phieu_da_huy(self, phieu: Dict[str, Any]):
        trang_thai = str(phieu.get("trangThai", "")).strip().lower()
        return trang_thai in ["đã hủy", "da huy", "hủy", "huy"]

    def tim_item(self, danh_sach: List[Dict[str, Any]], truong_ma: str, ma: str):
        for item in danh_sach:
            if item.get(truong_ma) == ma:
                return item
        return None

    def kiem_tra_kho_ton_tai(self, ma_kho: str):
        data = self.doc_json("kho_hang.json", {})
        if self.tim_item(data.get("kho", []), "maKho", ma_kho) is None:
            raise ValueError("Mã kho không tồn tại: " + ma_kho)

    def kiem_tra_san_pham_ton_tai(self, ma_san_pham: str):
        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)
        if san_pham is None:
            raise ValueError("Mã sản phẩm không tồn tại: " + ma_san_pham)
        return san_pham

    def chuan_hoa_chi_tiet_hang(self, chi_tiet: List[Dict[str, Any]]):
        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết phiếu không được rỗng.")

        ket_qua_map = {}
        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = chuyen_so_nguyen(item.get("soLuong", 0))
            don_gia = chuyen_so_nguyen(item.get("donGia", 0))

            if ma_san_pham == "":
                raise ValueError("Vui lòng chọn sản phẩm.")
            if so_luong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0.")
            if don_gia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0.")

            san_pham = self.kiem_tra_san_pham_ton_tai(ma_san_pham)

            if not self.la_san_pham_dang_kinh_doanh(san_pham):
                raise ValueError("Sản phẩm " + ma_san_pham + " đã ngừng kinh doanh, không thể chọn vào phiếu.")

            if ma_san_pham in ket_qua_map:
                ket_qua_map[ma_san_pham]["soLuong"] += so_luong
                continue

            dong = {
                "maSanPham": ma_san_pham,
                "soLuong": so_luong,
                "donGia": don_gia,
            }

            if item.get("maViTri", "") != "":
                dong["maViTri"] = item.get("maViTri", "")

            ket_qua_map[ma_san_pham] = dong

        return list(ket_qua_map.values())

    def lay_so_luong_ton(self, ma_kho: str, ma_san_pham: str):
        data = self.doc_json("kho_hang.json", {})

        for ton in data.get("tonKho", []):
            if ton.get("maKho") == ma_kho and ton.get("maSanPham") == ma_san_pham:
                return chuyen_so_nguyen(ton.get("soLuongTon", 0))

        return 0

    def cap_nhat_ton_kho(self, ma_kho: str, ma_san_pham: str, so_luong_thay_doi: int, ma_vi_tri: str = ""):
        data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            if ton.get("maKho") == ma_kho and ton.get("maSanPham") == ma_san_pham:
                so_luong_moi = chuyen_so_nguyen(ton.get("soLuongTon", 0)) + chuyen_so_nguyen(so_luong_thay_doi)

                if so_luong_moi < 0:
                    raise ValueError("Số lượng tồn kho không đủ cho sản phẩm " + ma_san_pham)

                ton["soLuongTon"] = so_luong_moi

                if ma_vi_tri != "":
                    ton["maViTri"] = ma_vi_tri

                self.ghi_json("kho_hang.json", data)
                return

        if so_luong_thay_doi < 0:
            raise ValueError("Sản phẩm chưa có tồn kho nên không thể xuất hàng: " + ma_san_pham)

        danh_sach_ton.append(TonKho(ma_kho, ma_san_pham, so_luong_thay_doi, ma_vi_tri).to_dict())
        self.ghi_json("kho_hang.json", data)

    def dat_lai_ton_kho(self, ma_kho: str, ma_san_pham: str, so_luong_moi: int):
        if so_luong_moi < 0:
            raise ValueError("Số lượng tồn mới không hợp lệ.")

        data = self.doc_json("kho_hang.json", {})
        danh_sach_ton = data.setdefault("tonKho", [])

        for ton in danh_sach_ton:
            if ton.get("maKho") == ma_kho and ton.get("maSanPham") == ma_san_pham:
                ton["soLuongTon"] = chuyen_so_nguyen(so_luong_moi)
                self.ghi_json("kho_hang.json", data)
                return

        danh_sach_ton.append(TonKho(ma_kho, ma_san_pham, chuyen_so_nguyen(so_luong_moi)).to_dict())
        self.ghi_json("kho_hang.json", data)

    def chuan_hoa_chi_tiet_kiem_ke(self, ma_kho: str, chi_tiet: List[Dict[str, Any]]):
        if len(chi_tiet) == 0:
            raise ValueError("Chi tiết kiểm kê không được rỗng.")

        ket_qua = []
        san_pham_da_chon = set()

        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong_thuc_te = chuyen_so_nguyen(item.get("soLuongThucTe", 0))

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

    def tao_phieu_kiem_ke(self, ma_kho: str, chi_tiet: List[Dict[str, Any]], ghi_chu: str = ""):
        self.kiem_tra_kho_ton_tai(ma_kho)
        chi_tiet_chuan = self.chuan_hoa_chi_tiet_kiem_ke(ma_kho, chi_tiet)
        data = self.doc_json("kiem_ke.json", [])
        ma_kiem_ke = self.tao_ma_tu_dong(data, "maKiemKe", "KK")

        phieu = {
            "maKiemKe": ma_kiem_ke,
            "maKho": ma_kho,
            "ngayKiemKe": self.lay_ngay_hien_tai(),
            "ghiChu": ghi_chu,
            "trangThai": "Đã kiểm kê",
            "chiTiet": chi_tiet_chuan,
        }

        data.append(phieu)
        self.ghi_json("kiem_ke.json", data)

        for item in chi_tiet_chuan:
            self.dat_lai_ton_kho(
                ma_kho,
                item.get("maSanPham", ""),
                chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
            )

        self.ghi_nhat_ky("Admin tạo kiểm kê", "Kiểm kê", "Tạo phiếu kiểm kê " + ma_kiem_ke)
        return phieu

    def cap_nhat_phieu_kiem_ke(self, ma_kiem_ke: str, ma_kho: str, chi_tiet: List[Dict[str, Any]], ghi_chu: str = ""):
        self.kiem_tra_kho_ton_tai(ma_kho)
        data = self.doc_json("kiem_ke.json", [])
        phieu = self.tim_item(data, "maKiemKe", ma_kiem_ke)

        if phieu is None:
            raise ValueError("Không tìm thấy phiếu kiểm kê.")
        if self.la_phieu_da_huy(phieu):
            raise ValueError("Không thể sửa phiếu kiểm kê đã hủy.")

        phieu_cu = deepcopy(phieu)
        da_hoan_ton_cu = not self.la_phieu_luu_tam(phieu_cu)

        try:
            if da_hoan_ton_cu:
                for item in phieu_cu.get("chiTiet", []):
                    self.dat_lai_ton_kho(
                        phieu_cu.get("maKho", ""),
                        item.get("maSanPham", ""),
                        chuyen_so_nguyen(item.get("soLuongHeThong", 0)),
                    )

            chi_tiet_chuan = self.chuan_hoa_chi_tiet_kiem_ke(ma_kho, chi_tiet)
            phieu["maKho"] = ma_kho
            phieu["ghiChu"] = ghi_chu
            phieu["chiTiet"] = chi_tiet_chuan
            phieu["trangThai"] = "Đã kiểm kê"

            for item in chi_tiet_chuan:
                self.dat_lai_ton_kho(
                    ma_kho,
                    item.get("maSanPham", ""),
                    chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
                )
        except Exception:
            phieu.clear()
            phieu.update(phieu_cu)

            if da_hoan_ton_cu:
                for item in phieu_cu.get("chiTiet", []):
                    self.dat_lai_ton_kho(
                        phieu_cu.get("maKho", ""),
                        item.get("maSanPham", ""),
                        chuyen_so_nguyen(item.get("soLuongThucTe", 0)),
                    )

            raise

        self.ghi_json("kiem_ke.json", data)
        self.ghi_nhat_ky("Admin sửa kiểm kê", "Kiểm kê", "Cập nhật phiếu kiểm kê " + ma_kiem_ke)
        return phieu

    def ap_dung_ton_phieu_nhap(self, phieu: Dict[str, Any], he_so: int):
        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                he_so * chuyen_so_nguyen(item.get("soLuong", 0)),
                item.get("maViTri", ""),
            )

    def ap_dung_ton_phieu_xuat(self, phieu: Dict[str, Any], he_so: int):
        for item in phieu.get("chiTiet", []):
            self.cap_nhat_ton_kho(
                phieu.get("maKho", ""),
                item.get("maSanPham", ""),
                -he_so * chuyen_so_nguyen(item.get("soLuong", 0)),
            )

    def kiem_tra_du_ton_khi_xuat(self, ma_kho: str, chi_tiet: List[Dict[str, Any]]):
        for item in chi_tiet:
            ma_san_pham = item.get("maSanPham", "")
            so_luong = chuyen_so_nguyen(item.get("soLuong", 0))
            if self.lay_so_luong_ton(ma_kho, ma_san_pham) < so_luong:
                raise ValueError("Không đủ tồn kho để xuất sản phẩm " + ma_san_pham)

    def tao_phieu_nhap(self, ma_nha_san_xuat: str, ma_kho: str, chi_tiet: List[Dict[str, Any]], luu_tam: bool = False):
        self.kiem_tra_kho_ton_tai(ma_kho)
        chi_tiet_chuan = self.chuan_hoa_chi_tiet_hang(chi_tiet)
        data = self.doc_json("phieu_nhap.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuNhap", "PN")
        phieu = {
            "maPhieuNhap": ma_phieu,
            "maNhaSanXuat": ma_nha_san_xuat,
            "maKho": ma_kho,
            "maTaiKhoan": self.lay_ma_tai_khoan_hien_tai(),
            "ngayNhap": self.lay_ngay_hien_tai(),
            "tongTien": tinh_tong_tien_chi_tiet(chi_tiet_chuan),
            "trangThai": "Lưu tạm" if luu_tam else "Đã nhập",
            "chiTiet": chi_tiet_chuan,
        }
        data.append(phieu)
        self.ghi_json("phieu_nhap.json", data)

        if not luu_tam:
            self.ap_dung_ton_phieu_nhap(phieu, 1)

        self.ghi_nhat_ky("Admin tạo phiếu nhập", "Phiếu nhập", "Tạo phiếu nhập " + ma_phieu)
        return phieu

    def cap_nhat_phieu_nhap(self, ma_phieu_nhap: str, ma_nha_san_xuat: str, ma_kho: str, chi_tiet: List[Dict[str, Any]], luu_tam: bool = False):
        self.kiem_tra_kho_ton_tai(ma_kho)
        chi_tiet_chuan = self.chuan_hoa_chi_tiet_hang(chi_tiet)
        data = self.doc_json("phieu_nhap.json", [])
        phieu = self.tim_item(data, "maPhieuNhap", ma_phieu_nhap)

        if phieu is None:
            raise ValueError("Không tìm thấy phiếu nhập.")
        if self.la_phieu_da_huy(phieu):
            raise ValueError("Không thể sửa phiếu nhập đã hủy.")

        phieu_cu = deepcopy(phieu)
        da_hoan_ton_cu = False

        try:
            if not self.la_phieu_luu_tam(phieu_cu):
                self.ap_dung_ton_phieu_nhap(phieu_cu, -1)
                da_hoan_ton_cu = True

            phieu["maNhaSanXuat"] = ma_nha_san_xuat
            phieu["maKho"] = ma_kho
            phieu["tongTien"] = tinh_tong_tien_chi_tiet(chi_tiet_chuan)
            phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã nhập"
            phieu["chiTiet"] = chi_tiet_chuan

            if not luu_tam:
                self.ap_dung_ton_phieu_nhap(phieu, 1)
        except Exception:
            phieu.clear()
            phieu.update(phieu_cu)

            if da_hoan_ton_cu:
                self.ap_dung_ton_phieu_nhap(phieu_cu, 1)

            raise

        self.ghi_json("phieu_nhap.json", data)
        self.ghi_nhat_ky("Admin sửa phiếu nhập", "Phiếu nhập", "Cập nhật phiếu nhập " + ma_phieu_nhap)
        return phieu

    def huy_phieu_nhap(self, ma_phieu_nhap: str):
        data = self.doc_json("phieu_nhap.json", [])
        phieu = self.tim_item(data, "maPhieuNhap", ma_phieu_nhap)

        if phieu is None:
            raise ValueError("Không tìm thấy phiếu nhập.")
        if self.la_phieu_da_huy(phieu):
            raise ValueError("Phiếu nhập đã hủy trước đó.")

        if not self.la_phieu_luu_tam(phieu):
            self.ap_dung_ton_phieu_nhap(phieu, -1)

        phieu["trangThai"] = "Đã hủy"
        self.ghi_json("phieu_nhap.json", data)
        self.ghi_nhat_ky("Admin hủy phiếu nhập", "Phiếu nhập", "Hủy phiếu nhập " + ma_phieu_nhap)
        return phieu

    def tao_phieu_xuat(self, ma_khach_hang: str, ma_kho: str, chi_tiet: List[Dict[str, Any]], luu_tam: bool = False):
        self.kiem_tra_kho_ton_tai(ma_kho)
        chi_tiet_chuan = self.chuan_hoa_chi_tiet_hang(chi_tiet)

        if not luu_tam:
            self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

        data = self.doc_json("phieu_xuat.json", [])
        ma_phieu = self.tao_ma_tu_dong(data, "maPhieuXuat", "PX")
        phieu = {
            "maPhieuXuat": ma_phieu,
            "maKho": ma_kho,
            "maKhachHang": ma_khach_hang,
            "maTaiKhoan": self.lay_ma_tai_khoan_hien_tai(),
            "ngayXuat": self.lay_ngay_hien_tai(),
            "tongTien": tinh_tong_tien_chi_tiet(chi_tiet_chuan),
            "trangThai": "Lưu tạm" if luu_tam else "Đã xuất",
            "chiTiet": chi_tiet_chuan,
        }
        data.append(phieu)
        self.ghi_json("phieu_xuat.json", data)

        if not luu_tam:
            self.ap_dung_ton_phieu_xuat(phieu, 1)

        self.ghi_nhat_ky("Admin tạo phiếu xuất", "Phiếu xuất", "Tạo phiếu xuất " + ma_phieu)
        return phieu

    def cap_nhat_phieu_xuat(self, ma_phieu_xuat: str, ma_khach_hang: str, ma_kho: str, chi_tiet: List[Dict[str, Any]], luu_tam: bool = False):
        self.kiem_tra_kho_ton_tai(ma_kho)
        chi_tiet_chuan = self.chuan_hoa_chi_tiet_hang(chi_tiet)
        data = self.doc_json("phieu_xuat.json", [])
        phieu = self.tim_item(data, "maPhieuXuat", ma_phieu_xuat)

        if phieu is None:
            raise ValueError("Không tìm thấy phiếu xuất.")
        if self.la_phieu_da_huy(phieu):
            raise ValueError("Không thể sửa phiếu xuất đã hủy.")

        phieu_cu = deepcopy(phieu)
        da_hoan_ton_cu = False

        try:
            if not self.la_phieu_luu_tam(phieu_cu):
                self.ap_dung_ton_phieu_xuat(phieu_cu, -1)
                da_hoan_ton_cu = True

            if not luu_tam:
                self.kiem_tra_du_ton_khi_xuat(ma_kho, chi_tiet_chuan)

            phieu["maKhachHang"] = ma_khach_hang
            phieu["maKho"] = ma_kho
            phieu["tongTien"] = tinh_tong_tien_chi_tiet(chi_tiet_chuan)
            phieu["trangThai"] = "Lưu tạm" if luu_tam else "Đã xuất"
            phieu["chiTiet"] = chi_tiet_chuan

            if not luu_tam:
                self.ap_dung_ton_phieu_xuat(phieu, 1)
        except Exception:
            phieu.clear()
            phieu.update(phieu_cu)

            if da_hoan_ton_cu:
                self.ap_dung_ton_phieu_xuat(phieu_cu, 1)

            raise

        self.ghi_json("phieu_xuat.json", data)
        self.ghi_nhat_ky("Admin sửa phiếu xuất", "Phiếu xuất", "Cập nhật phiếu xuất " + ma_phieu_xuat)
        return phieu

    def huy_phieu_xuat(self, ma_phieu_xuat: str):
        data = self.doc_json("phieu_xuat.json", [])
        phieu = self.tim_item(data, "maPhieuXuat", ma_phieu_xuat)

        if phieu is None:
            raise ValueError("Không tìm thấy phiếu xuất.")
        if self.la_phieu_da_huy(phieu):
            raise ValueError("Phiếu xuất đã hủy trước đó.")

        if not self.la_phieu_luu_tam(phieu):
            self.ap_dung_ton_phieu_xuat(phieu, -1)

        phieu["trangThai"] = "Đã hủy"
        self.ghi_json("phieu_xuat.json", data)
        self.ghi_nhat_ky("Admin hủy phiếu xuất", "Phiếu xuất", "Hủy phiếu xuất " + ma_phieu_xuat)
        return phieu


AdminCRUD = NghiepVuAdmin
