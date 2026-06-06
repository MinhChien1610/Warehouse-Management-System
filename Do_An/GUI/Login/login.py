import ctypes
import tkinter as tk
from tkinter import messagebox

from GUI.Common.base import GiaoDienCoSo


class GiaoDienLogin(GiaoDienCoSo):
    def __init__(self):
        super().__init__()

        self.root = tk.Tk()
        self.root.title("Đăng nhập Hệ thống")
        self.root.geometry("1100x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8F5F3")

        self.entry_username = None
        self.entry_password = None

        self.tao_giao_dien()

    def tao_giao_dien(self):
        self.canvas = tk.Canvas(self.root, bg="#F8F5F3", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.ve_nen()
        self.tao_khung_trai()
        self.tao_khung_phai()

    def ve_nen(self):
        self.canvas.create_rectangle(
            35, 35, 1065, 645,
            fill="white",
            outline="#E8D8D0",
            width=1,
        )

        self.canvas.create_polygon(
            35, 35,
            565, 35,
            515, 645,
            35, 645,
            fill="#B98E7C",
            outline="",
        )

        self.canvas.create_arc(
            -80, 520, 560, 800,
            start=0,
            extent=180,
            fill="#F8EDEA",
            outline="",
        )

        self.canvas.create_line(
            565, 35, 515, 645,
            fill="#F8F5F3",
            width=3,
        )

    def tao_khung_trai(self):
        self.canvas.create_text(
            285, 135,
            text="📦",
            fill="#FFF4EF",
            font=("Segoe UI", 66),
        )

        self.canvas.create_text(
            285, 285,
            text="QUẢN LÝ KHO HÀNG",
            fill="white",
            font=("Segoe UI", 26, "bold"),
        )

        self.canvas.create_text(
            285, 325,
            text="Warehouse Management System",
            fill="#FFF4EF",
            font=("Segoe UI", 13, "bold"),
        )

        self.canvas.create_line(
            250, 360, 320, 360,
            fill="white",
            width=3,
        )

        self.tao_the_gioi_thieu(95, 400, "▣", "Nhập - Xuất - Tồn kho")
        self.tao_the_gioi_thieu(95, 455, "▥", "Thống kê nhanh")
        self.tao_the_gioi_thieu(95, 510, "🔒", "Phân quyền rõ ràng")

        self.canvas.create_text(
            280, 595,
            text="Đơn giản  •  Hiệu quả  •  An toàn",
            fill="#A97C69",
            font=("Segoe UI", 12, "bold"),
        )

    def tao_the_gioi_thieu(self, x, y, icon, text):
        self.canvas.create_rectangle(
            x, y, x + 360, y + 42,
            fill="#C69B8A",
            outline="",
        )

        self.canvas.create_text(
            x + 32, y + 21,
            text=icon,
            fill="white",
            font=("Segoe UI", 16, "bold"),
        )

        self.canvas.create_text(
            x + 190, y + 21,
            text=text,
            fill="white",
            font=("Segoe UI", 12, "bold"),
        )

    def tao_khung_phai(self):
        form = tk.Frame(self.root, bg="white")
        form.place(x=665, y=95, width=360, height=500)

        avatar = tk.Frame(
            form,
            bg="#FBF7F5",
            highlightbackground="#E8D8D0",
            highlightthickness=1,
            width=100,
            height=100,
        )
        avatar.pack(anchor="center", pady=(0, 24))
        avatar.pack_propagate(False)

        tk.Label(
            avatar,
            text="👤",
            bg="#FBF7F5",
            fg="#AD806D",
            font=("Segoe UI", 42),
        ).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            form,
            text="Đăng nhập",
            bg="white",
            fg="#3F241B",
            font=("Segoe UI", 30, "bold"),
        ).pack(anchor="center")

        tk.Frame(form, bg="#AD806D", width=50, height=4).pack(pady=(10, 26))

        self.entry_username = self.tao_o_nhap(
            form,
            "Tên đăng nhập",
            "Nhập tên đăng nhập",
        )

        self.entry_password = self.tao_o_nhap(
            form,
            "Mật khẩu",
            "Nhập mật khẩu",
            True,
        )

        self.tao_nut_dang_nhap(form)

        tk.Label(
            form,
            text="Tài khoản và mật khẩu được quản trị viên cấp",
            bg="white",
            fg="#A0908A",
            font=("Segoe UI", 9),
        ).pack(pady=(18, 0))

    def tao_o_nhap(self, parent, label_text, placeholder, la_mat_khau=False):
        tk.Label(
            parent,
            text=label_text,
            bg="white",
            fg="#3F241B",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        khung = tk.Frame(
            parent,
            bg="#FBF7F5",
            highlightbackground="#E8D8D0",
            highlightthickness=1,
        )
        khung.pack(fill="x", pady=(0, 18))

        icon_text = "🔒" if la_mat_khau else "👤"

        tk.Label(
            khung,
            text=icon_text,
            bg="#FBF7F5",
            fg="#8D6F63",
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(12, 4))

        entry = tk.Entry(
            khung,
            bg="#FBF7F5",
            fg="#8D6F63",
            font=("Segoe UI", 11),
            bd=0,
            show="",
        )
        entry.pack(side="left", fill="x", expand=True, ipady=10)
        entry.insert(0, placeholder)

        if la_mat_khau:
            self.tao_nut_hien_mat_khau(khung, entry, placeholder)

        entry.bind(
            "<FocusIn>",
            lambda event: self.xoa_placeholder(entry, placeholder, la_mat_khau),
        )

        entry.bind(
            "<FocusOut>",
            lambda event: self.khoi_phuc_placeholder(entry, placeholder, la_mat_khau),
        )

        return entry

    def tao_nut_hien_mat_khau(self, parent, entry, placeholder):
        trang_thai = {"hien": False}

        def doi_hien_mat_khau():
            if entry.get() == placeholder:
                return

            if trang_thai["hien"]:
                entry.config(show="*")
                button.config(text="👁")
                trang_thai["hien"] = False
            else:
                entry.config(show="")
                button.config(text="🙈")
                trang_thai["hien"] = True

        button = tk.Button(
            parent,
            text="👁",
            command=doi_hien_mat_khau,
            bg="#FBF7F5",
            fg="#8D6F63",
            activebackground="#FBF7F5",
            activeforeground="#3F241B",
            bd=0,
            width=4,
            cursor="hand2",
        )
        button.pack(side="right", padx=(0, 8))

    def xoa_placeholder(self, entry, placeholder, la_mat_khau=False):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#3F241B")

            if la_mat_khau:
                entry.config(show="*")

    def khoi_phuc_placeholder(self, entry, placeholder, la_mat_khau=False):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#8D6F63")

            if la_mat_khau:
                entry.config(show="")

    def tao_nut_dang_nhap(self, parent):
        button = tk.Button(
            parent,
            text="ĐĂNG NHẬP",
            bg="#AD806D",
            fg="white",
            activebackground="#9F725F",
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            cursor="hand2",
            command=self.xu_ly_dang_nhap,
        )
        button.pack(fill="x", ipady=12, pady=(8, 0))

        self.root.bind("<Return>", lambda event: self.xu_ly_dang_nhap())

    def lay_noi_dung_entry(self, entry, placeholder):
        noi_dung = entry.get().strip()

        if noi_dung == placeholder:
            return ""

        return noi_dung

    def xu_ly_dang_nhap(self):
        username = self.lay_noi_dung_entry(
            self.entry_username,
            "Nhập tên đăng nhập",
        )

        password = self.lay_noi_dung_entry(
            self.entry_password,
            "Nhập mật khẩu",
        )

        if username == "" or password == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        data = self.doc_json("nguoi_dung.json", {})

        for tai_khoan in data.get("taiKhoan", []):
            dung_ten = tai_khoan.get("tenTaiKhoan", "") == username
            dung_mat_khau = tai_khoan.get("matKhau", "") == password

            if dung_ten and dung_mat_khau:
                self.kiem_tra_va_mo_giao_dien(data, tai_khoan)
                return

        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def kiem_tra_va_mo_giao_dien(self, data, tai_khoan):
        if not self.tai_khoan_dang_hoat_dong(tai_khoan):
            messagebox.showwarning("Thông báo", "Tài khoản đã bị khóa.")
            return

        vai_tro = self.lay_vai_tro_tai_khoan(
            data,
            tai_khoan.get("maTaiKhoan", ""),
        )

        if len(vai_tro) == 0:
            messagebox.showerror("Lỗi", "Tài khoản chưa được phân quyền.")
            return

        self.dang_nhap_vao_giao_dien(tai_khoan, vai_tro[0])

    def tai_khoan_dang_hoat_dong(self, tai_khoan):
        trang_thai = str(tai_khoan.get("trangThai", "")).strip().lower()

        return trang_thai in ["true", "1", "hoạt động", "active"]

    def lay_vai_tro_tai_khoan(self, data, ma_tai_khoan):
        vai_tro_map = {}

        for vai_tro in data.get("vaiTro", []):
            ma_vai_tro = vai_tro.get("maVaiTro", "")
            ten_vai_tro = vai_tro.get("tenVaiTro", "")
            vai_tro_map[ma_vai_tro] = ten_vai_tro

        ket_qua = []

        for phan_quyen in data.get("phanQuyen", []):
            if phan_quyen.get("maTaiKhoan") == ma_tai_khoan:
                ma_vai_tro = phan_quyen.get("maVaiTro", "")
                ket_qua.append(vai_tro_map.get(ma_vai_tro, ""))

        return ket_qua

    def dang_nhap_vao_giao_dien(self, tai_khoan, vai_tro):
        self.root.destroy()

        ten_vai_tro = str(vai_tro).strip().lower()

        if ten_vai_tro == "admin":
            from GUI.Admin.admin import hien_thi_admin
            hien_thi_admin(tai_khoan)
            return

        if ten_vai_tro in ["nhanvienkho", "nhân viên kho"]:
            from GUI.NhanVienKho.nhanvienkho import hien_thi_nhan_vien_kho
            hien_thi_nhan_vien_kho(tai_khoan)
            return

        if ten_vai_tro in ["ketoan", "kế toán"]:
            from GUI.KeToan.ketoan import hien_thi_ke_toan
            hien_thi_ke_toan(tai_khoan)
            return

        messagebox.showerror("Lỗi", "Tài khoản chưa được phân quyền giao diện.")

    def chay(self):
        self.root.mainloop()


def hien_thi_login():
    app = GiaoDienLogin()
    app.chay()


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    hien_thi_login()