import json
import os
from copy import deepcopy
from datetime import date, datetime

from Class.sanpham import SanPham


class HangHoa:
    # =========================
    # PHÂN QUYỀN
    # =========================
    def la_admin(self):
        return getattr(self, "la_quyen_admin", False)

    def kiem_tra_quyen_admin_hang_hoa(self):
        if not self.la_admin():
            raise ValueError("Nhân viên kho chỉ được xem hàng hóa trong kho được phân công.")

    # =========================
    # HÀM PHỤ
    # =========================
    def chuyen_so_nguyen_an_toan(self, value):
        if hasattr(self, "chuyen_so_nguyen"):
            return self.chuyen_so_nguyen(value)

        try:
            return int(str(value).replace(".", "").replace(",", "").strip())
        except Exception:
            return 0

    def tim_item(self, danh_sach, truong_ma, ma):
        for item in danh_sach:
            if item.get(truong_ma) == ma:
                return item
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

    def dinh_dang_tien_hang_hoa(self, value):
        return "{:,}".format(self.chuyen_so_nguyen_an_toan(value)).replace(",", ".")

    def chuan_hoa_text(self, value):
        return " ".join(str(value).strip().lower().split())

    def kiem_tra_trung_ten_san_pham(self, data, ten_san_pham, ma_bo_qua=""):
        ten_chuan = self.chuan_hoa_text(ten_san_pham)

        for san_pham in data.get("sanPham", []):
            if san_pham.get("maSanPham", "") == ma_bo_qua:
                continue

            if self.chuan_hoa_text(san_pham.get("tenSanPham", "")) == ten_chuan:
                raise ValueError("Tên sản phẩm đã tồn tại.")

    def them_hien_thi_tien_vao_san_pham(self, san_pham):
        dong = dict(san_pham)
        dong["donGiaHienThi"] = self.dinh_dang_tien_hang_hoa(dong.get("donGia", 0))
        dong["mucTonToiThieuHienThi"] = str(self.chuyen_so_nguyen_an_toan(dong.get("mucTonToiThieu", 0)))
        return dong

    def them_thong_tin_san_pham_vao_ton(self, ton, san_pham):
        dong = dict(ton)

        if san_pham is None:
            dong["tenSanPham"] = ""
            dong["maLoaiHang"] = ""
            dong["maDonViTinh"] = ""
            dong["donGia"] = 0
            dong["mucTonToiThieu"] = 0
            dong["trangThai"] = "Không tìm thấy sản phẩm"
            dong["donGiaHienThi"] = "0"
            return dong

        dong["tenSanPham"] = san_pham.get("tenSanPham", "")
        dong["maLoaiHang"] = san_pham.get("maLoaiHang", "")
        dong["maDonViTinh"] = san_pham.get("maDonViTinh", "")
        dong["donGia"] = san_pham.get("donGia", 0)
        dong["mucTonToiThieu"] = san_pham.get("mucTonToiThieu", 0)
        dong["trangThai"] = san_pham.get("trangThai", "Đang kinh doanh")
        dong["donGiaHienThi"] = self.dinh_dang_tien_hang_hoa(san_pham.get("donGia", 0))

        return dong

    # =========================
    # LOAD HÀNG HÓA THEO QUYỀN
    # =========================
    def lay_danh_sach_san_pham(self):
        data = self.doc_json("hang_hoa.json", {})
        danh_sach = []

        for san_pham in data.get("sanPham", []):
            danh_sach.append(self.them_hien_thi_tien_vao_san_pham(san_pham))

        return danh_sach

    def lay_hang_hoa_theo_quyen(self):
        hang_data = self.doc_json("hang_hoa.json", {})
        kho_data = self.doc_json("kho_hang.json", {})

        danh_sach_san_pham = hang_data.get("sanPham", [])
        san_pham_map = {}

        for san_pham in danh_sach_san_pham:
            san_pham_map[san_pham.get("maSanPham", "")] = san_pham

        if self.la_admin():
            ket_qua = []

            for san_pham in danh_sach_san_pham:
                ket_qua.append(self.them_hien_thi_tien_vao_san_pham(san_pham))

            return ket_qua

        if hasattr(self, "loc_theo_kho_duoc_phan_cong"):
            danh_sach_ton = self.loc_theo_kho_duoc_phan_cong(kho_data.get("tonKho", []))
        else:
            danh_sach_ton = kho_data.get("tonKho", [])

        ket_qua = []

        for ton in danh_sach_ton:
            ma_san_pham = ton.get("maSanPham", "")
            san_pham = san_pham_map.get(ma_san_pham)
            ket_qua.append(self.them_thong_tin_san_pham_vao_ton(ton, san_pham))

        return ket_qua

    def lay_ton_hang_hoa_theo_kho_duoc_phan_cong(self):
        return self.lay_hang_hoa_theo_quyen()

    # =========================
    # KIỂM TRA DỮ LIỆU
    # =========================
    def kiem_tra_thong_tin_san_pham(
        self,
        ten_san_pham,
        ma_loai_hang,
        ma_don_vi_tinh,
        don_gia,
        muc_ton_toi_thieu,
    ):
        ten_san_pham = str(ten_san_pham).strip()

        if ten_san_pham == "":
            raise ValueError("Vui lòng nhập tên sản phẩm.")

        if len(ten_san_pham) > 150:
            raise ValueError("Tên sản phẩm không được quá 150 ký tự.")

        if ten_san_pham.isdigit():
            raise ValueError("Tên sản phẩm không hợp lệ.")

        if str(ma_loai_hang).strip() == "":
            raise ValueError("Vui lòng chọn loại hàng.")

        if str(ma_don_vi_tinh).strip() == "":
            raise ValueError("Vui lòng chọn đơn vị tính.")

        if self.chuyen_so_nguyen_an_toan(don_gia) <= 0:
            raise ValueError("Đơn giá phải lớn hơn 0.")

        if self.chuyen_so_nguyen_an_toan(muc_ton_toi_thieu) < 0:
            raise ValueError("Mức tồn tối thiểu không được âm.")

        data = self.doc_json("hang_hoa.json", {})

        if self.tim_item(data.get("loaiHang", []), "maLoaiHang", ma_loai_hang) is None:
            raise ValueError("Loại hàng không tồn tại.")

        if self.tim_item(data.get("donViTinh", []), "maDonViTinh", ma_don_vi_tinh) is None:
            raise ValueError("Đơn vị tính không tồn tại.")

    # =========================
    # ADMIN: THÊM / SỬA / ĐỔI TRẠNG THÁI
    # =========================
    def tao_san_pham(
        self,
        ten_san_pham,
        ma_loai_hang,
        ma_don_vi_tinh,
        don_gia,
        muc_ton_toi_thieu,
    ):
        self.kiem_tra_quyen_admin_hang_hoa()

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

        ma_san_pham = self.tao_ma_tu_dong_do_dai(danh_sach, "maSanPham", "SP", 4)

        san_pham = SanPham(
            ma_san_pham,
            str(ten_san_pham).strip(),
            ma_don_vi_tinh,
            ma_loai_hang,
            self.chuyen_so_nguyen_an_toan(don_gia),
            self.chuyen_so_nguyen_an_toan(muc_ton_toi_thieu),
        ).to_dict()

        if san_pham.get("trangThai", "") == "":
            san_pham["trangThai"] = "Đang kinh doanh"

        danh_sach.append(san_pham)
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Admin thêm sản phẩm", "Hàng hóa", "Tạo sản phẩm " + ma_san_pham)

        return san_pham

    def sua_san_pham(
        self,
        ma_san_pham,
        ten_san_pham,
        ma_loai_hang,
        ma_don_vi_tinh,
        don_gia,
        muc_ton_toi_thieu,
    ):
        self.kiem_tra_quyen_admin_hang_hoa()

        if str(ma_san_pham).strip() == "":
            raise ValueError("Vui lòng chọn sản phẩm cần sửa.")

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
            raise ValueError("Không tìm thấy sản phẩm: " + ma_san_pham)

        self.kiem_tra_trung_ten_san_pham(data, ten_san_pham, ma_san_pham)

        san_pham["maSanPham"] = ma_san_pham
        san_pham["tenSanPham"] = str(ten_san_pham).strip()
        san_pham["maLoaiHang"] = ma_loai_hang
        san_pham["maDonViTinh"] = ma_don_vi_tinh
        san_pham["donGia"] = self.chuyen_so_nguyen_an_toan(don_gia)
        san_pham["mucTonToiThieu"] = self.chuyen_so_nguyen_an_toan(muc_ton_toi_thieu)

        if san_pham.get("trangThai", "") == "":
            san_pham["trangThai"] = "Đang kinh doanh"

        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky("Admin sửa sản phẩm", "Hàng hóa", "Cập nhật sản phẩm " + ma_san_pham)

        return san_pham

    def doi_trang_thai_kinh_doanh_san_pham(self, ma_san_pham):
        self.kiem_tra_quyen_admin_hang_hoa()

        if str(ma_san_pham).strip() == "":
            raise ValueError("Vui lòng chọn sản phẩm.")

        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)

        if san_pham is None:
            raise ValueError("Không tìm thấy sản phẩm: " + ma_san_pham)

        if self.la_san_pham_dang_kinh_doanh(san_pham):
            trang_thai_moi = "Ngừng kinh doanh"
        else:
            trang_thai_moi = "Đang kinh doanh"

        san_pham["trangThai"] = trang_thai_moi
        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky(
            "Admin đổi trạng thái sản phẩm",
            "Hàng hóa",
            "Đổi trạng thái " + ma_san_pham + " thành " + trang_thai_moi,
        )

        return san_pham

    def ngung_kinh_doanh_san_pham(self, ma_san_pham):
        self.kiem_tra_quyen_admin_hang_hoa()

        data = self.doc_json("hang_hoa.json", {})
        san_pham = self.tim_item(data.get("sanPham", []), "maSanPham", ma_san_pham)

        if san_pham is None:
            raise ValueError("Không tìm thấy sản phẩm: " + ma_san_pham)

        san_pham["trangThai"] = "Ngừng kinh doanh"

        self.ghi_json("hang_hoa.json", data)
        self.ghi_nhat_ky(
            "Admin ngừng kinh doanh sản phẩm",
            "Hàng hóa",
            "Chuyển sản phẩm " + ma_san_pham + " sang trạng thái Ngừng kinh doanh",
        )

        return san_pham
