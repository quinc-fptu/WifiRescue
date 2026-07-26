import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

__author__ = "QuiNC"
__version__ = "1.0.0"

# Application directory configuration
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).parent
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    APP_DIR = Path(__file__).parent
    BUNDLE_DIR = APP_DIR

BACKUP_DIR = APP_DIR / "WiFi_Backup"

# Windows AppUserModelID for taskbar icon binding
try:
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("QuiNC.WifiRescue.App.1.0")
except Exception:
    pass

class CompactWifiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WifiRescue - by QuiNC")
        self.root.geometry("340x260")
        self.root.resizable(False, False)

        icon_path = BUNDLE_DIR / "app_icon_flat.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except Exception:
                pass

        # Dark Zinc Theme Palette
        self.COLOR_BG = "#09090B"
        self.COLOR_SURFACE = "#18181B"
        self.COLOR_BORDER = "#27272A"
        self.COLOR_INK = "#FAFAFA"
        self.COLOR_MUTED = "#71717A"
        self.COLOR_WATERMARK = "#52525B"

        self.root.configure(bg=self.COLOR_BG)

        # Typography
        self.FONT_TITLE = ("Segoe UI", 11, "bold")
        self.FONT_BTN = ("Segoe UI", 9, "bold")
        self.FONT_SMALL = ("Segoe UI", 8)
        self.FONT_SIG = ("Segoe UI", 7, "italic")

        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=14)
        header.pack(fill="x")

        lbl_title = tk.Label(
            header,
            text="WIFI RESCUE",
            font=self.FONT_TITLE,
            fg=self.COLOR_INK,
            bg=self.COLOR_BG,
            anchor="w"
        )
        lbl_title.pack(side="left")

        right_links = tk.Frame(header, bg=self.COLOR_BG)
        right_links.pack(side="right")

        btn_help = tk.Label(
            right_links,
            text="❓ Help",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            cursor="hand2"
        )
        btn_help.pack(side="left", padx=(0, 10))
        btn_help.bind("<Button-1>", lambda e: self.show_help_popup())

        btn_folder = tk.Label(
            right_links,
            text="📁 Folder",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            cursor="hand2"
        )
        btn_folder.pack(side="left")
        btn_folder.bind("<Button-1>", lambda e: self.open_backup_dir())

        tk.Frame(self.root, bg=self.COLOR_BORDER, height=1).pack(fill="x", padx=16)

        # Main Action Buttons
        content = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=16)
        content.pack(fill="both", expand=True)

        self.btn_backup = tk.Button(
            content,
            text="BACKUP PROFILES",
            font=self.FONT_BTN,
            bg=self.COLOR_INK,
            fg=self.COLOR_BG,
            activebackground="#E4E4E7",
            activeforeground=self.COLOR_BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.backup_wifi
        )
        self.btn_backup.pack(fill="x", pady=(0, 8))

        self.btn_restore = tk.Button(
            content,
            text="RESTORE PROFILES",
            font=self.FONT_BTN,
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_INK,
            activebackground=self.COLOR_BORDER,
            activeforeground=self.COLOR_INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.restore_wifi
        )
        self.btn_restore.pack(fill="x")

        # Footer Status Bar
        footer = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=8)
        footer.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(
            footer,
            text="STATUS: READY",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            anchor="w"
        )
        self.lbl_status.pack(side="left")

        lbl_sig = tk.Label(
            footer,
            text="by QuiNC",
            font=self.FONT_SIG,
            fg=self.COLOR_WATERMARK,
            bg=self.COLOR_BG,
            anchor="e"
        )
        lbl_sig.pack(side="right")

    def show_help_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Hướng Dẫn Sử Dụng - WifiRescue")
        popup.geometry("380x320")
        popup.resizable(False, False)
        popup.configure(bg=self.COLOR_BG)

        icon_path = BUNDLE_DIR / "app_icon_flat.ico"
        if icon_path.exists():
            try:
                popup.iconbitmap(str(icon_path))
            except Exception:
                pass

        popup.transient(self.root)
        popup.grab_set()

        head_f = tk.Frame(popup, bg=self.COLOR_BG, padx=20, pady=16)
        head_f.pack(fill="x")

        tk.Label(
            head_f,
            text="📖 HƯỚNG DẪN SỬ DỤNG",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLOR_INK,
            bg=self.COLOR_BG
        ).pack(anchor="w")

        tk.Label(
            head_f,
            text="Tác giả: QuiNC · Phiên bản Portable",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(popup, bg=self.COLOR_BORDER, height=1).pack(fill="x", padx=20)

        body_f = tk.Frame(popup, bg=self.COLOR_BG, padx=20, pady=14)
        body_f.pack(fill="both", expand=True)

        steps_text = (
            "1. Trước khi đi thi (Sao lưu):\n"
            "   Mở app ➔ Bấm BACKUP PROFILES để lưu toàn bộ Wi-Fi\n"
            "   vào thư mục WiFi_Backup (nằm cùng cấp với app).\n\n"
            "2. Sau khi thi xong (Khôi phục):\n"
            "   Mở app ➔ Bấm RESTORE PROFILES để nạp lại tất cả\n"
            "   mật khẩu Wi-Fi chỉ trong 1 giây.\n\n"
            "💡 Lưu ý: Nếu Windows báo màn hình xanh lần đầu,\n"
            "   chọn More info ➔ chọn Run anyway để chạy."
        )

        txt = tk.Label(
            body_f,
            text=steps_text,
            font=("Segoe UI", 8),
            fg="#D4D4D8",
            bg=self.COLOR_BG,
            justify="left",
            anchor="nw"
        )
        txt.pack(fill="both", expand=True)

        btn_close = tk.Button(
            popup,
            text="Đã Hiểu",
            font=self.FONT_BTN,
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_INK,
            activebackground=self.COLOR_BORDER,
            activeforeground=self.COLOR_INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=6,
            command=popup.destroy
        )
        btn_close.pack(fill="x", padx=20, pady=(0, 16))

    def backup_wifi(self):
        try:
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            cmd = f'netsh wlan export profile key=clear folder="{BACKUP_DIR}"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                count = len(list(BACKUP_DIR.glob("*.xml")))
                self.lbl_status.config(text=f"STATUS: BACKED UP {count} PROFILES", fg=self.COLOR_INK)
                messagebox.showinfo("WifiRescue by QuiNC", f"Successfully backed up {count} profiles to:\n{BACKUP_DIR}")
            else:
                self.lbl_status.config(text="STATUS: BACKUP FAILED", fg="#EF4444")
                messagebox.showerror("WifiRescue by QuiNC", f"Failed to export profiles.\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def restore_wifi(self):
        if not BACKUP_DIR.exists():
            messagebox.showwarning("WifiRescue by QuiNC", "No backup directory found in current app folder.")
            return

        xml_files = list(BACKUP_DIR.glob("*.xml"))
        if not xml_files:
            messagebox.showwarning("WifiRescue by QuiNC", "No saved profile XML files found.")
            return

        existing_profiles = []
        try:
            show_res = subprocess.run('netsh wlan show profiles', capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')
            for line in show_res.stdout.splitlines():
                if ":" in line:
                    profile_name = line.split(":", 1)[1].strip()
                    if profile_name and profile_name != "<None>":
                        existing_profiles.append(profile_name.lower())
        except Exception:
            pass

        new_restored_count = 0
        already_existed_count = 0
        failed_count = 0

        for xml_file in xml_files:
            name_part = xml_file.stem
            if name_part.startswith("Wi-Fi-"):
                name_part = name_part[6:]

            if name_part.lower() in existing_profiles:
                already_existed_count += 1
                continue

            cmd = f'netsh wlan add profile filename="{xml_file}" user=all'
            res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if res.returncode == 0:
                new_restored_count += 1
            else:
                failed_count += 1

        total = len(xml_files)
        if already_existed_count == total:
            self.lbl_status.config(text=f"STATUS: ALL {total} PROFILES ALREADY EXIST", fg=self.COLOR_INK)
            messagebox.showinfo("WifiRescue by QuiNC", f"All {total} Wi-Fi profiles are already saved on this system.")
        elif new_restored_count > 0:
            msg = f"Successfully restored {new_restored_count} new Wi-Fi profile(s)."
            if already_existed_count > 0:
                msg += f"\n({already_existed_count} profile(s) already existed)."
            self.lbl_status.config(text=f"STATUS: RESTORED {new_restored_count} NEW PROFILE(S)", fg=self.COLOR_INK)
            messagebox.showinfo("WifiRescue by QuiNC", msg)
        else:
            self.lbl_status.config(text="STATUS: RESTORE FAILED", fg="#EF4444")
            messagebox.showerror("WifiRescue by QuiNC", "Failed to restore Wi-Fi profiles.")

    def open_backup_dir(self):
        if not BACKUP_DIR.exists():
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        os.startfile(BACKUP_DIR)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompactWifiApp(root)
    root.mainloop()
