from datetime import date, datetime


class NhanVien:
    def kiem_tra_ngay_sinh(self, value, bat_buoc=False):
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

    def lay_trang_thai_moi(self, trang_thai_hien_tai):
        trang_thai = str(trang_thai_hien_tai).strip().lower()

        if trang_thai in ["true", "1", "hoat dong", "hoạt động", "dang hoat dong", "đang hoạt động", "active", "mo", "mở"]:
            return "Đã khóa"

        return "Hoạt động"

    def la_trang_thai_khoa(self, trang_thai):
        trang_thai = str(trang_thai).strip().lower()
        return trang_thai in ["false", "0", "đã khóa", "da khoa", "khóa", "khoa", "inactive"]

    def kiem_tra_thong_tin_nhan_vien(self, data, du_lieu, ma_bo_qua=""):
        ten = str(du_lieu.get("tenNhanVien", "")).strip()

        if ten == "":
            raise ValueError("Vui lòng nhập tên nhân viên.")

        self.kiem_tra_ngay_sinh(du_lieu.get("ngaySinh", ""), False)
        self.kiem_tra_so_dien_thoai_vn(du_lieu.get("soDienThoai", ""), "Số điện thoại", False)
        self.kiem_tra_email_gmail(du_lieu.get("email", ""), "Email", False)
        self.kiem_tra_trung_gia_tri(data.get("nhanVien", []), "soDienThoai", du_lieu.get("soDienThoai", ""), "Số điện thoại nhân viên", "maNhanVien", ma_bo_qua)
        self.kiem_tra_trung_gia_tri(data.get("nhanVien", []), "email", du_lieu.get("email", ""), "Email nhân viên", "maNhanVien", ma_bo_qua)

    def tao_nhan_vien(self, du_lieu):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_nhan_vien(data, du_lieu)

        danh_sach = data.setdefault("nhanVien", [])
        ma_nhan_vien = self.tao_ma_tu_dong_do_dai(danh_sach, "maNhanVien", "NV", 3)

        dong = dict(du_lieu)
        dong["maNhanVien"] = ma_nhan_vien

        if dong.get("trangThai", "") == "":
            dong["trangThai"] = "Hoạt động"

        danh_sach.append(dong)
        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Nhân viên", "Nhân viên", "Thêm " + ma_nhan_vien)
        return dong

    def cap_nhat_nhan_vien(self, ma_nhan_vien, du_lieu):
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

    def khoa_mo_nhan_vien(self, ma_nhan_vien):
        if self.la_tai_khoan_dang_dung(ma_nhan_vien=ma_nhan_vien):
            raise ValueError("Không thể khóa/mở chính nhân viên đang đăng nhập.")

        data = self.doc_nguoi_dung()
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên đã chọn.")

        trang_thai_moi = self.lay_trang_thai_moi(nhan_vien.get("trangThai", ""))
        nhan_vien["trangThai"] = trang_thai_moi

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maNhanVien") == ma_nhan_vien:
                tai_khoan["trangThai"] = trang_thai_moi

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Khóa/Mở khóa", "Nhân viên", "Cập nhật trạng thái " + ma_nhan_vien + " thành " + trang_thai_moi)
        return trang_thai_moi

    def xoa_nhan_vien(self, ma_nhan_vien):
        if self.la_tai_khoan_dang_dung(ma_nhan_vien=ma_nhan_vien):
            raise ValueError("Không thể xóa chính nhân viên đang đăng nhập.")

        data = self.doc_nguoi_dung()
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên cần xóa.")

        if not self.la_trang_thai_khoa(nhan_vien.get("trangThai", "")):
            raise ValueError("Chỉ được xóa nhân viên đang ở trạng thái Đã khóa.")

        tai_khoan_lien_ket = []
        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                tai_khoan_lien_ket.append(tai_khoan)

        for tai_khoan in tai_khoan_lien_ket:
            if not self.la_trang_thai_khoa(tai_khoan.get("trangThai", "")):
                raise ValueError("Tài khoản liên kết " + tai_khoan.get("maTaiKhoan", "") + " chưa bị khóa.")

        danh_sach_ma_tai_khoan = []
        for tai_khoan in tai_khoan_lien_ket:
            danh_sach_ma_tai_khoan.append(tai_khoan.get("maTaiKhoan", ""))

        data["nhanVien"] = [item for item in data.get("nhanVien", []) if item.get("maNhanVien", "") != ma_nhan_vien]
        data["taiKhoan"] = [item for item in data.get("taiKhoan", []) if item.get("maNhanVien", "") != ma_nhan_vien]
        data["phanQuyen"] = [item for item in data.get("phanQuyen", []) if item.get("maTaiKhoan", "") not in danh_sach_ma_tai_khoan]
        data["phanCongKho"] = [item for item in data.get("phanCongKho", []) if item.get("maTaiKhoan", "") not in danh_sach_ma_tai_khoan]

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin xóa Nhân viên", "Nhân viên", "Xóa " + ma_nhan_vien)
        return nhan_vien
