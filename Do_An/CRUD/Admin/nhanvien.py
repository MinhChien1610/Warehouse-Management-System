from datetime import date, datetime


class NhanVien:
    def doc_nguoi_dung(self):
        return self.doc_json("nguoi_dung.json", {})

    def ghi_nguoi_dung(self, data):
        self.ghi_json("nguoi_dung.json", data)

    def la_hoat_dong(self, trang_thai):
        trang_thai = str(trang_thai).strip().lower()
        return trang_thai in [
            "true", "1",
            "hoạt động", "hoat dong",
            "đang hoạt động", "dang hoat dong",
            "active", "mở", "mo"
        ]

    def la_khong_hoat_dong(self, trang_thai):
        trang_thai = str(trang_thai).strip().lower()
        return trang_thai in ["không hoạt động", "khong hoat dong"]

    def la_trang_thai_khoa(self, trang_thai):
        trang_thai = str(trang_thai).strip().lower()
        return trang_thai in [
            "false", "0",
            "đã khóa", "da khoa",
            "khóa", "khoa",
            "inactive"
        ]

    def lay_trang_thai_moi(self, trang_thai_hien_tai):
        if self.la_khong_hoat_dong(trang_thai_hien_tai):
            raise ValueError("Dữ liệu đang không hoạt động, vui lòng dùng chức năng sửa để kích hoạt lại.")

        if self.la_hoat_dong(trang_thai_hien_tai):
            return "Đã khóa"

        return "Hoạt động"

    def kiem_tra_sdt(self, value, label="Số điện thoại", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + label.lower() + ".")
            return ""

        if not value.isdigit():
            raise ValueError(label + " chỉ được nhập số.")

        if len(value) != 10:
            raise ValueError(label + " phải gồm đúng 10 số.")

        if not value.startswith("0"):
            raise ValueError(label + " phải bắt đầu bằng số 0.")

        return value

    def kiem_tra_email(self, value, label="Email", bat_buoc=False):
        value = str(value).strip().lower()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + label.lower() + ".")
            return ""

        if " " in value:
            raise ValueError(label + " không được chứa khoảng trắng.")

        if not value.endswith("@gmail.com"):
            raise ValueError(label + " phải có dạng example@gmail.com.")

        ten_email = value.replace("@gmail.com", "")

        if ten_email == "":
            raise ValueError(label + " không hợp lệ.")

        return value

    def chuan_hoa_ngay_sinh(self, value):
        value = str(value).strip()

        if value == "":
            raise ValueError("Vui lòng nhập ngày sinh.")

        if "/" in value:
            phan = value.split("/")

            if len(phan) != 3:
                raise ValueError("Ngày sinh phải có dạng DD/MM/YYYY hoặc YYYY-MM-DD.")

            ngay, thang, nam = phan

            if len(ngay) != 2 or len(thang) != 2 or len(nam) != 4:
                raise ValueError("Ngày sinh phải có dạng DD/MM/YYYY hoặc YYYY-MM-DD.")

            if not ngay.isdigit() or not thang.isdigit() or not nam.isdigit():
                raise ValueError("Ngày sinh chỉ được nhập số và dấu / hoặc dấu -.")

            ngay = int(ngay)
            thang = int(thang)
            nam = int(nam)

            if ngay <= 0:
                raise ValueError("Ngày sinh phải lớn hơn 0.")

            if thang <= 0:
                raise ValueError("Tháng sinh phải lớn hơn 0.")

            if thang > 12:
                raise ValueError("Tháng sinh phải nằm trong khoảng từ 1 đến 12.")

            try:
                return date(nam, thang, ngay)
            except ValueError:
                raise ValueError("Ngày sinh không tồn tại.")

        if "-" in value:
            phan = value.split("-")

            if len(phan) != 3:
                raise ValueError("Ngày sinh phải có dạng DD/MM/YYYY hoặc YYYY-MM-DD.")

            nam, thang, ngay = phan

            if len(nam) != 4 or len(thang) != 2 or len(ngay) != 2:
                raise ValueError("Ngày sinh phải có dạng DD/MM/YYYY hoặc YYYY-MM-DD.")

            if not ngay.isdigit() or not thang.isdigit() or not nam.isdigit():
                raise ValueError("Ngày sinh chỉ được nhập số và dấu / hoặc dấu -.")

            ngay = int(ngay)
            thang = int(thang)
            nam = int(nam)

            if ngay <= 0:
                raise ValueError("Ngày sinh phải lớn hơn 0.")

            if thang <= 0:
                raise ValueError("Tháng sinh phải lớn hơn 0.")

            if thang > 12:
                raise ValueError("Tháng sinh phải nằm trong khoảng từ 1 đến 12.")

            try:
                return date(nam, thang, ngay)
            except ValueError:
                raise ValueError("Ngày sinh không tồn tại.")

        raise ValueError("Ngày sinh phải có dạng DD/MM/YYYY hoặc YYYY-MM-DD.")


    def kiem_tra_ngay_sinh(self, value, bat_buoc=True):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập ngày sinh.")
            return ""

        ngay_sinh = self.chuan_hoa_ngay_sinh(value)
        hom_nay = date.today()

        if ngay_sinh > hom_nay:
            raise ValueError("Ngày sinh không được lớn hơn ngày hiện tại.")

        tuoi = hom_nay.year - ngay_sinh.year

        if (hom_nay.month, hom_nay.day) < (ngay_sinh.month, ngay_sinh.day):
            tuoi -= 1

        if tuoi < 18:
            raise ValueError("Nhân viên phải từ 18 tuổi trở lên.")

        if tuoi > 65:
            raise ValueError("Tuổi nhân viên không hợp lý.")

        return ngay_sinh.strftime("%Y-%m-%d")

    def kiem_tra_thong_tin_nhan_vien(self, data, du_lieu, ma_bo_qua=""):
        ten = str(du_lieu.get("tenNhanVien", "")).strip()

        if ten == "":
            raise ValueError("Vui lòng nhập tên nhân viên.")

        if len(ten) < 2:
            raise ValueError("Tên nhân viên phải có ít nhất 2 ký tự.")

        if len(ten) > 100:
            raise ValueError("Tên nhân viên không được quá 100 ký tự.")

        for ky_tu in ten:
            if ky_tu.isdigit():
                raise ValueError("Tên nhân viên không được chứa số.")

        du_lieu["tenNhanVien"] = ten
        du_lieu["ngaySinh"] = self.kiem_tra_ngay_sinh(du_lieu.get("ngaySinh", ""), True)
        du_lieu["soDienThoai"] = self.kiem_tra_sdt(du_lieu.get("soDienThoai", ""), "Số điện thoại", False)
        du_lieu["email"] = self.kiem_tra_email(du_lieu.get("email", ""), "Email", False)

        if du_lieu.get("soDienThoai", "") != "":
            self.kiem_tra_trung_gia_tri(
                data.get("nhanVien", []),
                "soDienThoai",
                du_lieu.get("soDienThoai", ""),
                "Số điện thoại nhân viên",
                "maNhanVien",
                ma_bo_qua,
            )

        if du_lieu.get("email", "") != "":
            self.kiem_tra_trung_gia_tri(
                data.get("nhanVien", []),
                "email",
                du_lieu.get("email", ""),
                "Email nhân viên",
                "maNhanVien",
                ma_bo_qua,
            )

    def tao_nhan_vien(self, du_lieu):
        data = self.doc_nguoi_dung()
        self.kiem_tra_thong_tin_nhan_vien(data, du_lieu)

        danh_sach = data.setdefault("nhanVien", [])
        ma_nhan_vien = self.tao_ma_tu_dong_do_dai(danh_sach, "maNhanVien", "NV", 3)

        dong = dict(du_lieu)
        dong["maNhanVien"] = ma_nhan_vien

        if str(dong.get("trangThai", "")).strip() == "":
            dong["trangThai"] = "Hoạt động"

        danh_sach.append(dong)

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky("Admin thêm Nhân viên", "Nhân viên", "Thêm " + ma_nhan_vien)

        return dong

    def cap_nhat_nhan_vien(self, ma_nhan_vien, du_lieu):
        data = self.doc_nguoi_dung()
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên cần sửa.")

        self.kiem_tra_thong_tin_nhan_vien(data, du_lieu, ma_nhan_vien)

        trang_thai_cu = str(nhan_vien.get("trangThai", "")).strip()
        trang_thai_moi = str(du_lieu.get("trangThai", trang_thai_cu)).strip()

        nhan_vien.update(du_lieu)
        nhan_vien["maNhanVien"] = ma_nhan_vien

        if trang_thai_moi in ["Đã khóa", "Không hoạt động"]:
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                    tai_khoan["trangThai"] = trang_thai_moi

        self.ghi_nguoi_dung(data)

        if self.la_khong_hoat_dong(trang_thai_cu) and self.la_hoat_dong(trang_thai_moi):
            self.ghi_nhat_ky("Admin khôi phục Nhân viên", "Nhân viên", "Khôi phục " + ma_nhan_vien)
        else:
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

        if trang_thai_moi == "Đã khóa":
            for tai_khoan in data.get("taiKhoan", []):
                if tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                    tai_khoan["trangThai"] = "Đã khóa"

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky(
            "Khóa/Mở khóa",
            "Nhân viên",
            "Cập nhật trạng thái " + ma_nhan_vien + " thành " + trang_thai_moi,
        )

        return trang_thai_moi

    def xoa_nhan_vien(self, ma_nhan_vien):
        if self.la_tai_khoan_dang_dung(ma_nhan_vien=ma_nhan_vien):
            raise ValueError("Không thể xóa chính nhân viên đang đăng nhập.")

        data = self.doc_nguoi_dung()
        nhan_vien = self.tim_item(data.get("nhanVien", []), "maNhanVien", ma_nhan_vien)

        if nhan_vien is None:
            raise ValueError("Không tìm thấy nhân viên cần xóa.")

        if self.la_khong_hoat_dong(nhan_vien.get("trangThai", "")):
            raise ValueError("Nhân viên này đã không hoạt động.")

        nhan_vien["trangThai"] = "Không hoạt động"

        for tai_khoan in data.get("taiKhoan", []):
            if tai_khoan.get("maNhanVien", "") == ma_nhan_vien:
                tai_khoan["trangThai"] = "Không hoạt động"

        self.ghi_nguoi_dung(data)
        self.ghi_nhat_ky(
            "Admin xóa mềm Nhân viên",
            "Nhân viên",
            "Chuyển " + ma_nhan_vien + " sang Không hoạt động",
        )

        return nhan_vien