import calendar
import json
import os
import re
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk, messagebox

from Calculator.common import (
    chuyen_so,
    chuyen_so_nguyen,
    dinh_dang_so,
    dinh_dang_so_ngan,
    dinh_dang_tien,
)


class GiaoDienCoSo:
    def __init__(self):
        self.khoi_tao_mau_sac()

    # =========================
    # MÀU SẮC DÙNG CHUNG
    # =========================



    def khoi_tao_mau_sac(self):
        # Theme xanh cobalt dùng chung cho toàn bộ hệ thống
        self.mau_nen = "#F3F8FF"

        self.mau_sidebar = "#123F78"
        self.mau_sidebar_dam = "#0B2D5C"
        self.mau_sidebar_nhat = "#DCEBFF"

        self.mau_menu = "#1D5FAF"
        self.mau_menu_hover = "#2A74D4"
        self.mau_menu_con = "#BFD9FF"
        self.mau_menu_chon = "#0F4C93"

        self.mau_card = "#FFFFFF"
        self.mau_card_nhe = "#F6FAFF"
        self.mau_vien = "#C7DAF5"

        self.mau_chu_dam = "#17324D"
        self.mau_chu_phu = "#5C7188"

        self.mau_them = "#10B981"
        self.mau_sua = "#2F80ED"
        self.mau_xoa = "#EF4444"
        self.mau_thoat = "#49657F"
        self.mau_tim_kiem = "#2F80ED"

        self.mau_canh_bao = "#F59E0B"
        self.mau_thanh_cong = "#10B981"
        self.mau_nguy_hiem = "#EF4444"

        self.mau_blue_nhe = self.mau_sidebar_nhat
        self.mau_blue_vien = self.mau_vien
        self.mau_blue_sang = "#91BDF2"

        self.mau_teal_nhe = self.mau_sidebar_nhat
        self.mau_teal_vien = self.mau_vien
        self.mau_teal_sang = "#91BDF2"

        self.mau_xanh_nhe = self.mau_sidebar_nhat
        self.mau_xanh_vien = self.mau_vien

        self.mau_nhan = self.mau_menu_chon
        self.mau_nhan_nhe = self.mau_sidebar_nhat

    def lay_thu_muc_goc(self):
        thu_muc = os.path.dirname(os.path.abspath(__file__))

        while True:
            duong_dan_data = os.path.join(thu_muc, "Data")

            if os.path.exists(duong_dan_data):
                return thu_muc

            thu_muc_cha = os.path.dirname(thu_muc)

            if thu_muc_cha == thu_muc:
                return os.path.dirname(os.path.abspath(__file__))

            thu_muc = thu_muc_cha

    def lay_duong_dan_data(self, ten_file):
        return os.path.join(self.lay_thu_muc_goc(), "Data", ten_file)

    def doc_json(self, ten_file, mac_dinh=None):
        duong_dan = self.lay_duong_dan_data(ten_file)

        if not os.path.exists(duong_dan):
            return mac_dinh

        danh_sach_encoding = ["utf-8-sig", "utf-8", "cp1258"]

        for encoding in danh_sach_encoding:
            try:
                with open(duong_dan, "r", encoding=encoding) as file:
                    return json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

        return mac_dinh

    def ghi_json(self, ten_file, data):
        duong_dan = self.lay_duong_dan_data(ten_file)

        with open(duong_dan, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # =========================
    # STYLE
    # =========================
    def cau_hinh_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.cau_hinh_style_bang(style)
        self.cau_hinh_style_tab(style)




    def cau_hinh_style_bang(self, style):
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=40,
            background="white",
            fieldbackground="white",
            foreground=self.mau_chu_dam,
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.mau_sidebar_nhat,
            foreground=self.mau_chu_dam,
            padding=9,
            relief="flat",
        )

        style.map(
            "Treeview",
            background=[("selected", self.mau_menu_con)],
            foreground=[("selected", self.mau_chu_dam)],
        )

        style.configure(
            "Vertical.TScrollbar",
            background=self.mau_blue_sang,
            troughcolor=self.mau_nen,
            bordercolor=self.mau_nen,
            arrowcolor=self.mau_chu_dam,
        )

        style.configure(
            "Horizontal.TScrollbar",
            background=self.mau_blue_sang,
            troughcolor=self.mau_nen,
            bordercolor=self.mau_nen,
            arrowcolor=self.mau_chu_dam,
        )

    def cau_hinh_style_tab(self, style):
        style.configure(
            "TNotebook",
            background=self.mau_nen,
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            background=self.mau_card_nhe,
            foreground=self.mau_chu_dam,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", self.mau_menu_chon)],
            foreground=[("selected", "white")],
        )

    def xoa_noi_dung(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def tao_font(self, size, bold=False):
        if bold:
            return ("Segoe UI", size, "bold")

        return ("Segoe UI", size)

    def tao_label(self, parent, text, size=11, color=None, bold=False, bg=None):
        if color is None:
            color = self.mau_chu_dam

        if bg is None:
            bg = self.mau_card

        label = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=color,
            font=self.tao_font(size, bold),
            anchor="w",
            justify="left",
        )

        return label

    def tao_card(self, parent, bg=None):
        if bg is None:
            bg = self.mau_card

        card = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )

        return card


    def tao_nut(self, parent, text, command, bg=None):
        if bg is None:
            bg = self.mau_menu

        button = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg="white",
            activebackground=self.lay_mau_hover_nut(bg),
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=command,
        )

        return button




    def lay_mau_hover_nut(self, bg):
        if bg == self.mau_them:
            return "#059669"

        if bg == self.mau_sua:
            return "#164D9A"

        if bg == self.mau_xoa:
            return "#DC2626"

        if bg == self.mau_thoat:
            return "#344E68"

        if bg == self.mau_tim_kiem:
            return "#164D9A"

        if bg == self.mau_menu:
            return "#2A74D4"

        if bg == self.mau_menu_chon:
            return "#0B2D5C"

        if bg == self.mau_sidebar_dam:
            return "#123F78"

        return bg

    def tao_tieu_de_trang(self, parent, title, subtitle=""):
        self.xoa_noi_dung(parent)

        header = tk.Frame(parent, bg=self.mau_nen)
        header.pack(fill="x", padx=26, pady=(22, 10))

        self.tao_label(
            header,
            title,
            size=28,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_nen,
        ).pack(anchor="w")

        if subtitle != "":
            self.tao_label(
                header,
                subtitle,
                size=11,
                color=self.mau_chu_phu,
                bg=self.mau_nen,
            ).pack(anchor="w", pady=(4, 0))


    def tao_khung_noi_dung(self, parent):
        khung = self.tao_card(parent)
        khung.pack(fill="both", expand=True, padx=26, pady=(0, 22))

        ben_trong = tk.Frame(khung, bg=self.mau_card)
        ben_trong.pack(fill="both", expand=True, padx=18, pady=18)

        return ben_trong

    def tao_khung_cuon_doc(self, parent, bg=None):
        if bg is None:
            bg = self.mau_card

        wrapper = tk.Frame(parent, bg=bg)
        wrapper.pack(fill="both", expand=True, padx=0, pady=0)

        canvas = tk.Canvas(
            wrapper,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            wrapper,
            orient="vertical",
            command=canvas.yview,
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def cap_nhat_vung_cuon(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfigure(window_id, width=canvas.winfo_width())

        def cuon_chuot(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        content.bind("<Configure>", cap_nhat_vung_cuon)
        canvas.bind("<Configure>", cap_nhat_vung_cuon)
        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", cuon_chuot))
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

        return content

    # =========================
    # THANH CÔNG CỤ
    # =========================
    def tao_thanh_cong_cu(
        self,
        parent,
        placeholder,
        tim_kiem,
        them=None,
        sua=None,
        xoa=None,
        buttons=None,
    ):
        toolbar = tk.Frame(parent, bg=self.mau_card)
        toolbar.pack(fill="x", pady=(0, 18))

        button_frame = tk.Frame(toolbar, bg=self.mau_card)
        button_frame.pack(side="left")

        search_frame = tk.Frame(toolbar, bg=self.mau_card)
        search_frame.pack(side="right")

        if buttons is None:
            buttons = self.tao_danh_sach_nut_crud(them, sua, xoa)

        self.tao_cac_nut_toolbar(button_frame, buttons)

        entry = self.tao_o_tim_kiem_toolbar(
            search_frame,
            placeholder,
            tim_kiem,
        )

        return entry

    def tao_danh_sach_nut_crud(self, them=None, sua=None, xoa=None):
        buttons = []

        if them is not None:
            buttons.append({
                "text": "Thêm",
                "command": them,
                "color": self.mau_them,
            })

        if sua is not None:
            buttons.append({
                "text": "Sửa",
                "command": sua,
                "color": self.mau_sua,
            })

        if xoa is not None:
            buttons.append({
                "text": "Xóa",
                "command": xoa,
                "color": self.mau_xoa,
            })

        return buttons

    def tao_cac_nut_toolbar(self, parent, buttons):
        for button in buttons:
            text = button.get("text", "")
            command = button.get("command")
            color = button.get("color", self.mau_menu)

            if text == "" or command is None:
                continue

            self.tao_nut(
                parent,
                text,
                command,
                color,
            ).pack(side="left", padx=(0, 8))


    def tao_o_tim_kiem_toolbar(self, parent, placeholder, tim_kiem):
        search_box = tk.Frame(
            parent,
            bg=self.mau_card_nhe,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        search_box.pack(side="left", padx=(0, 10))

        entry = tk.Entry(
            search_box,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_phu,
            bd=0,
            width=38,
        )
        entry.pack(padx=14, ipady=10)
        entry.insert(0, placeholder)

        def xu_ly_tim(event=None):
            tu_khoa = self.lay_noi_dung_tim_kiem(entry, placeholder)
            tim_kiem(tu_khoa)

        def focus_in(event=None):
            self.xoa_placeholder(entry, placeholder)

        def focus_out(event=None):
            self.khoi_phuc_placeholder(entry, placeholder)

        self.tao_nut(
            parent,
            "Tìm kiếm",
            xu_ly_tim,
            self.mau_tim_kiem,
        ).pack(side="right")

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)
        entry.bind("<Return>", xu_ly_tim)

        return entry

    def lay_noi_dung_tim_kiem(self, entry, placeholder):
        tu_khoa = entry.get().strip()

        if tu_khoa == placeholder:
            return ""

        return tu_khoa

    def xoa_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.mau_chu_dam)

    def khoi_phuc_placeholder(self, entry, placeholder):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg=self.mau_chu_phu)

    # =========================
    # LỊCH CHỌN NGÀY
    # =========================
    def mo_lich_chon_ngay(self, entry):
        hom_nay = date.today()

        popup = self.tao_popup_lich()

        header = tk.Frame(popup, bg=self.mau_card)
        header.pack(fill="x", padx=12, pady=(12, 8))

        thang_var = tk.IntVar(value=hom_nay.month)
        nam_var = tk.IntVar(value=hom_nay.year)

        title = tk.Label(
            header,
            text="",
            bg=self.mau_card,
            fg=self.mau_chu_dam,
            font=("Segoe UI", 11, "bold"),
        )

        grid = tk.Frame(popup, bg=self.mau_card)

        def ve_lich():
            self.ve_noi_dung_lich(
                grid,
                title,
                thang_var,
                nam_var,
                entry,
                popup,
            )

        def lui_thang():
            self.doi_thang_lich(thang_var, nam_var, -1)
            ve_lich()

        def toi_thang():
            self.doi_thang_lich(thang_var, nam_var, 1)
            ve_lich()

        self.tao_nut_doi_thang(header, "<", lui_thang).pack(side="left")
        title.pack(side="left", fill="x", expand=True)
        self.tao_nut_doi_thang(header, ">", toi_thang).pack(side="right")

        grid.pack(padx=12, pady=(0, 12))

        ve_lich()

    def tao_popup_lich(self):
        popup = tk.Toplevel(self.root)
        popup.title("Chọn ngày")
        popup.geometry("310x280")
        popup.configure(bg=self.mau_card)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        return popup


    def tao_nut_doi_thang(self, parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.mau_sua,
            fg="white",
            activebackground=self.mau_menu_hover,
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            width=4,
            cursor="hand2",
        )

        return button

    def doi_thang_lich(self, thang_var, nam_var, huong):
        thang = thang_var.get()
        nam = nam_var.get()

        if huong == -1:
            if thang == 1:
                thang_var.set(12)
                nam_var.set(nam - 1)
            else:
                thang_var.set(thang - 1)

        if huong == 1:
            if thang == 12:
                thang_var.set(1)
                nam_var.set(nam + 1)
            else:
                thang_var.set(thang + 1)

    def ve_noi_dung_lich(self, grid, title, thang_var, nam_var, entry, popup):
        for widget in grid.winfo_children():
            widget.destroy()

        thang = thang_var.get()
        nam = nam_var.get()

        title.config(text=str(thang).zfill(2) + "/" + str(nam))

        self.ve_header_lich(grid)
        self.ve_cac_ngay_trong_thang(grid, thang, nam, entry, popup)

    def ve_header_lich(self, grid):
        danh_sach_thu = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

        for col, text in enumerate(danh_sach_thu):
            tk.Label(
                grid,
                text=text,
                bg=self.mau_card,
                fg=self.mau_chu_phu,
                font=("Segoe UI", 9, "bold"),
                width=4,
            ).grid(row=0, column=col, pady=(0, 4))

    def ve_cac_ngay_trong_thang(self, grid, thang, nam, entry, popup):
        lich_thang = calendar.monthcalendar(nam, thang)

        for row_index, tuan in enumerate(lich_thang, start=1):
            for col_index, ngay in enumerate(tuan):
                if ngay == 0:
                    self.tao_o_ngay_rong(grid, row_index, col_index)
                else:
                    self.tao_nut_ngay(
                        grid,
                        ngay,
                        row_index,
                        col_index,
                        thang,
                        nam,
                        entry,
                        popup,
                    )

    def tao_o_ngay_rong(self, grid, row_index, col_index):
        tk.Label(
            grid,
            text="",
            bg=self.mau_card,
            width=4,
        ).grid(row=row_index, column=col_index)

    def tao_nut_ngay(self, grid, ngay, row_index, col_index, thang, nam, entry, popup):
        def chon_ngay():
            entry.delete(0, tk.END)
            entry.insert(0, f"{nam}-{thang:02d}-{ngay:02d}")
            popup.destroy()

        tk.Button(
            grid,
            text=str(ngay),
            command=chon_ngay,
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            activebackground=self.mau_menu_con,
            activeforeground=self.mau_chu_dam,
            font=("Segoe UI", 9),
            bd=0,
            width=4,
            pady=4,
            cursor="hand2",
        ).grid(row=row_index, column=col_index, padx=2, pady=2)

    # =========================
    # BẢNG
    # =========================
    def tao_bang(self, parent, columns, headings, widths, stretch=True):
        table_frame = tk.Frame(parent, bg=self.mau_card)
        table_frame.pack(fill="both", expand=True)

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview,
        )

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=table.xview,
        )

        table.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.cau_hinh_cot_bang(table, columns, headings, widths, stretch)

        return table

    def cau_hinh_cot_bang(self, table, columns, headings, widths, stretch):
        for index in range(len(columns)):
            table.heading(columns[index], text=headings[index])
            table.column(
                columns[index],
                width=widths[index],
                minwidth=60,
                anchor="w",
                stretch=stretch,
            )

    def do_du_lieu_vao_bang(self, table, danh_sach, cac_cot):
        self.xoa_du_lieu_bang(table)

        for item in danh_sach:
            gia_tri = []

            for cot in cac_cot:
                gia_tri.append(self.lay_gia_tri_cot(item, cot))

            table.insert("", "end", values=gia_tri)

    def xoa_du_lieu_bang(self, table):
        for row in table.get_children():
            table.delete(row)

    def lay_gia_tri_cot(self, item, cot):
        if isinstance(item, dict):
            return item.get(cot, "")

        return getattr(item, cot, "")

    def lay_ma_dong_dang_chon(self, bang):
        selected = bang.selection()

        if len(selected) == 0:
            return ""

        values = bang.item(selected[0], "values")

        if len(values) == 0:
            return ""

        return values[0]

    def gan_su_kien_click(self, widget, command):
        widget.config(cursor="hand2")
        widget.bind("<Button-1>", lambda event: command())

        for child in widget.winfo_children():
            child.config(cursor="hand2")
            child.bind("<Button-1>", lambda event: command())

    # =========================
    # ĐỊNH DẠNG / CHUYỂN ĐỔI SỐ
    # =========================
    def chuyen_so(self, value):
        return chuyen_so(value)

    def chuyen_so_nguyen(self, value):
        return chuyen_so_nguyen(value)

    def dinh_dang_so(self, value):
        return dinh_dang_so(value)

    def dinh_dang_so_ngan(self, value):
        return dinh_dang_so_ngan(value)

    def dinh_dang_tien(self, value):
        return dinh_dang_tien(value)

    # =========================
    # RÀNG BUỘC DỮ LIỆU DÙNG CHUNG
    # =========================
    def bat_buoc_nhap(self, value, label):
        value = str(value).strip()

        if value == "":
            raise ValueError("Vui lòng nhập " + str(label).lower() + ".")

        return value

    def kiem_tra_chi_chu(self, value, label, bat_buoc=True):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + str(label).lower() + ".")
            return value

        for ky_tu in value:
            if not (ky_tu.isalpha() or ky_tu.isspace()):
                raise ValueError(str(label) + " chỉ được nhập chữ.")

        return value

    def kiem_tra_chi_so(self, value, label, bat_buoc=True, gia_tri_nho_nhat=None):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + str(label).lower() + ".")
            return 0

        if not value.isdigit():
            raise ValueError(str(label) + " chỉ được nhập số.")

        so = int(value)

        if gia_tri_nho_nhat is not None and so < gia_tri_nho_nhat:
            raise ValueError(str(label) + " phải lớn hơn hoặc bằng " + str(gia_tri_nho_nhat) + ".")

        return so

    def kiem_tra_so_dien_thoai(self, value, label="Số điện thoại", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + str(label).lower() + ".")
            return value

        if not re.fullmatch(r"0\d{9}", value):
            raise ValueError(str(label) + " phải bắt đầu bằng 0 và đúng 10 số.")

        return value

    def kiem_tra_email_gmail(self, value, label="Email", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + str(label).lower() + ".")
            return value

        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@gmail\.com", value):
            raise ValueError(str(label) + " phải đúng định dạng và có đuôi @gmail.com.")

        return value

    def kiem_tra_ngay(self, value, label="Ngày", bat_buoc=False):
        value = str(value).strip()

        if value == "":
            if bat_buoc:
                raise ValueError("Vui lòng nhập " + str(label).lower() + ".")
            return value

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError(str(label) + " phải đúng định dạng yyyy-mm-dd.")

        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(str(label) + " không hợp lệ.")

        return value

    def gan_rang_buoc_chi_nhap_so(self, entry, label):
        def kiem_tra(event=None):
            value = entry.get()

            if value == "":
                return

            if value.isdigit():
                return

            value_moi = "".join(ky_tu for ky_tu in value if ky_tu.isdigit())
            entry.delete(0, tk.END)
            entry.insert(0, value_moi)
            messagebox.showwarning("Dữ liệu không hợp lệ", str(label) + " chỉ được nhập số.")

        entry.bind("<KeyRelease>", kiem_tra)
        entry.bind("<FocusOut>", kiem_tra)
        return entry

    def gan_rang_buoc_ngay(self, entry, label, placeholder=""):
        def kiem_tra(event=None):
            value = entry.get().strip()

            if value == "" or value == placeholder:
                return

            try:
                self.kiem_tra_ngay(value, label, False)
            except ValueError as loi:
                messagebox.showwarning("Dữ liệu không hợp lệ", str(loi))

        entry.bind("<FocusOut>", kiem_tra, add="+")
        return entry

    # =========================
    # TÍNH TOÁN DÙNG CHUNG
    # =========================
    def tinh_tong_hang_hoa_hien_co(self, danh_sach_ton=None):
        if danh_sach_ton is None:
            kho_data = self.doc_json("kho_hang.json", {})
            danh_sach_ton = kho_data.get("tonKho", [])

        tong = 0

        for ton in danh_sach_ton:
            tong += self.chuyen_so_nguyen(ton.get("soLuongTon", 0))

        return int(tong)

    # =========================
    # FORM DÙNG CHUNG
    # =========================
    def tao_cua_so_form(self, title, width, height, parent=None):
        parent_window = parent or getattr(self, "root", None)

        if parent_window is None:
            form = tk.Toplevel()
        else:
            form = tk.Toplevel(parent_window)
            form.transient(parent_window)

        form.title(title)
        form.geometry(str(width) + "x" + str(height))
        form.minsize(width, min(height, 420))
        form.configure(bg=self.mau_card)
        form.grab_set()

        self.tao_label(
            form,
            title,
            size=17,
            color=self.mau_chu_dam,
            bold=True,
            bg=self.mau_card,
        ).pack(anchor="w", padx=22, pady=(16, 8))

        body = tk.Frame(form, bg=self.mau_card)
        body.pack(fill="both", expand=True, padx=22, pady=(0, 8))

        bottom = tk.Frame(form, bg=self.mau_card)
        bottom.pack(side="bottom", fill="x", padx=22, pady=(4, 16))

        return {
            "window": form,
            "body": body,
            "bottom": bottom,
        }

    def tao_combobox_form(self, parent, label_text, values):
        self.tao_label(
            parent,
            label_text,
            size=10,
            color=self.mau_chu_phu,
            bold=True,
        ).pack(anchor="w", pady=(5, 2))

        combo = ttk.Combobox(
            parent,
            values=values,
            state="readonly",
            font=("Segoe UI", 10),
        )
        combo.pack(fill="x", ipady=3)

        if len(values) > 0:
            combo.current(0)

        return combo

    def tao_entry_form(self, parent, label_text):
        self.tao_label(
            parent,
            label_text,
            size=10,
            color=self.mau_chu_phu,
            bold=True,
        ).pack(anchor="w", pady=(5, 2))

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg=self.mau_card_nhe,
            fg=self.mau_chu_dam,
            bd=0,
            highlightbackground=self.mau_vien,
            highlightthickness=1,
        )
        entry.pack(fill="x", ipady=6)

        return entry

    def tao_nut_luu_huy(self, parent, luu, huy, text_luu="Lưu", text_huy="Hủy"):
        self.tao_nut(
            parent,
            text_luu,
            luu,
            self.mau_them,
        ).pack(side="right", padx=(8, 0))

        self.tao_nut(
            parent,
            text_huy,
            huy,
            self.mau_thoat,
        ).pack(side="right")

    def tao_dong_thong_tin(self, parent, label_text, value_text):
        row = tk.Frame(parent, bg=self.mau_card)
        row.pack(side="left", fill="x", expand=True, pady=3)

        self.tao_label(row, label_text + ":", 10, self.mau_chu_phu, True).pack(side="left")
        self.tao_label(row, str(value_text), 10, self.mau_chu_dam).pack(side="left", padx=(8, 0))

    def mo_chi_tiet_phieu(self, phieu, loai):
        if loai == "nhap":
            title = "Chi tiết phiếu nhập " + phieu.get("maPhieuNhap", "")
            ma_phieu = phieu.get("maPhieuNhap", "")
            ngay = phieu.get("ngayNhap", "")
            doi_tac_label = "Nhà sản xuất"
            doi_tac_value = phieu.get("maNhaSanXuat", "")
        elif loai == "xuat":
            title = "Chi tiết phiếu xuất " + phieu.get("maPhieuXuat", "")
            ma_phieu = phieu.get("maPhieuXuat", "")
            ngay = phieu.get("ngayXuat", "")
            doi_tac_label = "Khách hàng"
            doi_tac_value = phieu.get("maKhachHang", "")
        else:
            title = "Chi tiết phiếu kiểm kho " + phieu.get("maKiemKe", "")
            ma_phieu = phieu.get("maKiemKe", "")
            ngay = phieu.get("ngayKiemKe", "")
            doi_tac_label = "Ghi chú"
            doi_tac_value = phieu.get("ghiChu", "")

        form = self.tao_cua_so_form(title, 880, 620)
        khung = form["body"]

        thong_tin = self.tao_card(khung)
        thong_tin.pack(fill="x", pady=(0, 12))

        dong_1 = tk.Frame(thong_tin, bg=self.mau_card)
        dong_1.pack(fill="x", padx=14, pady=(12, 4))
        self.tao_dong_thong_tin(dong_1, "Mã phiếu", ma_phieu)
        self.tao_dong_thong_tin(dong_1, "Kho", phieu.get("maKho", ""))

        dong_2 = tk.Frame(thong_tin, bg=self.mau_card)
        dong_2.pack(fill="x", padx=14, pady=(0, 4))
        self.tao_dong_thong_tin(dong_2, "Ngày", ngay)
        self.tao_dong_thong_tin(dong_2, "Trạng thái", phieu.get("trangThai", ""))

        dong_3 = tk.Frame(thong_tin, bg=self.mau_card)
        dong_3.pack(fill="x", padx=14, pady=(0, 12))
        self.tao_dong_thong_tin(dong_3, doi_tac_label, doi_tac_value)
        if loai in ["nhap", "xuat"]:
            self.tao_dong_thong_tin(dong_3, "Tổng tiền", self.dinh_dang_tien(phieu.get("tongTien", 0)))

        chi_tiet = self.chuan_bi_chi_tiet_phieu(phieu, loai)

        if loai == "kiem":
            cot = ("maSanPham", "tenSanPham", "soLuongHeThong", "soLuongThucTe", "chenhLech")
            tieu_de = ("Mã SP", "Tên sản phẩm", "SL hệ thống", "SL thực tế", "Chênh lệch")
            do_rong = (120, 360, 130, 130, 130)
        else:
            cot = ("maSanPham", "tenSanPham", "soLuong", "donGia", "thanhTien", "maViTri")
            tieu_de = ("Mã SP", "Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền", "Vị trí")
            do_rong = (120, 330, 110, 140, 150, 120)

        bang = self.tao_bang(khung, cot, tieu_de, do_rong)
        self.do_du_lieu_vao_bang(bang, chi_tiet, cot)

        self.tao_nut(form["bottom"], "Đóng", form["window"].destroy, self.mau_thoat).pack(side="right")

    def chuan_bi_chi_tiet_phieu(self, phieu, loai):
        ket_qua = []

        for item in phieu.get("chiTiet", []):
            ma_san_pham = item.get("maSanPham", "")
            san_pham = self.tim_san_pham_theo_ma_chung(ma_san_pham)
            ten_san_pham = ""

            if san_pham is not None:
                ten_san_pham = san_pham.get("tenSanPham", "")

            dong = dict(item)
            dong["tenSanPham"] = ten_san_pham

            if loai == "kiem":
                he_thong = self.chuyen_so(item.get("soLuongHeThong", 0))
                thuc_te = self.chuyen_so(item.get("soLuongThucTe", 0))
                dong["chenhLech"] = int(thuc_te - he_thong)
            else:
                so_luong = self.chuyen_so(item.get("soLuong", 0))
                don_gia = self.chuyen_so(item.get("donGia", 0))
                dong["thanhTien"] = self.dinh_dang_tien(so_luong * don_gia)

            ket_qua.append(dong)

        return ket_qua

    def tim_san_pham_theo_ma_chung(self, ma_san_pham):
        data = self.doc_json("hang_hoa.json", {})

        for san_pham in data.get("sanPham", []):
            if san_pham.get("maSanPham", "") == ma_san_pham:
                return san_pham

        return None

    def tao_danh_sach_chon(self, danh_sach, ma_key, ten_key):
        ket_qua = []

        for item in danh_sach:
            ma = str(self.lay_gia_tri_cot(item, ma_key))
            ten = str(self.lay_gia_tri_cot(item, ten_key))

            ket_qua.append(ma + " - " + ten)

        return ket_qua

    def lay_ma_tu_combobox(self, value):
        if value is None:
            return ""

        value = str(value).strip()

        if value == "":
            return ""

        return value.split(" - ", 1)[0].strip()

    def chon_combobox_theo_ma(self, combo, ma):
        values = list(combo.cget("values"))

        for index, value in enumerate(values):
            dung_ma_day_du = str(value).startswith(str(ma) + " -")
            dung_ma_truc_tiep = str(value) == str(ma)

            if dung_ma_day_du or dung_ma_truc_tiep:
                combo.current(index)
                return

    # =========================
    # NÚT THOÁT / THÔNG BÁO
    # =========================
    def tao_nut_thoat_duoi(self, parent, command):
        bottom = tk.Frame(parent, bg=self.mau_card)
        bottom.pack(fill="x", pady=(16, 0))

        self.tao_nut(
            bottom,
            "Thoát",
            command,
            self.mau_thoat,
        ).pack(side="right")
