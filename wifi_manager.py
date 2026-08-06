import os
import sys
import json
import subprocess
import threading
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

__author__ = "QuiNC"
__version__ = "1.3.1"
GITHUB_REPO = "quinc-fptu/WifiRescue"

# Application directory configuration
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    APP_DIR = Path(__file__).parent
    BUNDLE_DIR = APP_DIR

BACKUP_DIR = APP_DIR / "WiFi_Backup"
CREDENTIALS_FILE = BACKUP_DIR / "enterprise_credentials.json"

# Windows AppUserModelID for taskbar icon binding
try:
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "QuiNC.WifiRescue.App.1.3"
    )
except Exception:
    pass


class ImpeccableDialog(tk.Toplevel):
    """Custom Zinc-themed dialog modal matching the main app aesthetics."""

    def __init__(self, parent, title, app_icon_path=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg="#09090B")
        self.transient(parent)

        if app_icon_path and app_icon_path.exists():
            try:
                self.iconbitmap(str(app_icon_path))
            except Exception:
                pass

        # Color scheme
        self.BG = "#09090B"
        self.SURFACE = "#18181B"
        self.BORDER = "#27272A"
        self.INK = "#FAFAFA"
        self.MUTED = "#A1A1AA"
        self.ACCENT = "#3F3F46"

    def center_modal(self, width=340, height=260):
        """Center modal window over parent window."""
        self.update_idletasks()
        self.master.update_idletasks()

        parent_x = self.master.winfo_rootx()
        parent_y = self.master.winfo_rooty()
        parent_w = self.master.winfo_width()
        parent_h = self.master.winfo_height()

        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")
        self.grab_set()


GITHUB_PAGES_URL = "https://quinc-dev.github.io/WifiRescue/"


class UpdatePromptDialog(ImpeccableDialog):
    """Zinc-styled Remote Update Prompt Modal."""

    def __init__(
        self,
        parent,
        latest_ver,
        download_url=None,
        release_notes="",
        app_icon_path=None,
    ):
        super().__init__(parent, "Cập Nhật Phiên Bản Mới", app_icon_path)
        self.download_url = GITHUB_PAGES_URL

        # Header
        head = tk.Frame(self, bg=self.BG, padx=18, pady=12)
        head.pack(fill="x")

        tk.Label(
            head,
            text=f"🎉 Đã Có Phiên Bản Mới ({latest_ver})",
            font=("Segoe UI", 10, "bold"),
            fg="#10B981",
            bg=self.BG,
        ).pack(anchor="w")
        tk.Label(
            head,
            text=f"Bạn đang dùng v{__version__}. Khuyên dùng bản mới nhất!",
            font=("Segoe UI", 8),
            fg=self.MUTED,
            bg=self.BG,
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(self, bg=self.BORDER, height=1).pack(fill="x", padx=18)

        # Body Message
        body = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        body.pack(fill="both", expand=True)

        msg_text = f"Phiên bản WifiRescue {latest_ver} đã sẵn sàng.\n"
        if release_notes:
            cleaned_notes = (
                release_notes.replace("###", "")
                .replace("**", "")
                .replace("---", "")
                .strip()
            )
            msg_text += f"\nNội dung cập nhật:\n{cleaned_notes[:180]}"

        msg_lbl = tk.Label(
            body,
            text=msg_text,
            font=("Segoe UI", 8),
            fg="#D4D4D8",
            bg=self.BG,
            justify="left",
            wraplength=310,
            anchor="nw",
        )
        msg_lbl.pack(fill="both", expand=True)

        # Bottom Buttons
        btn_box = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        btn_box.pack(fill="x", side="bottom")

        btn_download = tk.Button(
            btn_box,
            text="MỞ TRANG TẢI VỀ",
            font=("Segoe UI", 8, "bold"),
            bg="#10B981",
            fg="#09090B",
            activebackground="#34D399",
            activeforeground="#09090B",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.on_download,
        )
        btn_download.pack(side="right", padx=(6, 0))

        btn_later = tk.Button(
            btn_box,
            text="Để Sau",
            font=("Segoe UI", 8),
            bg=self.SURFACE,
            fg=self.MUTED,
            activebackground=self.BORDER,
            activeforeground=self.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.destroy,
        )
        btn_later.pack(side="right")

        self.center_modal(360, 260)

    def on_download(self):
        webbrowser.open(GITHUB_PAGES_URL)
        self.destroy()


class EnterpriseCredentialDialog(ImpeccableDialog):
    """Custom dialog for entering Enterprise Wi-Fi credentials with Show/Hide password toggle."""

    def __init__(self, parent, ssid_name, app_icon_path=None, default_user=""):
        super().__init__(parent, f"Wi-Fi Credentials - {ssid_name}", app_icon_path)
        self.result = None

        # Header
        head = tk.Frame(self, bg=self.BG, padx=18, pady=12)
        head.pack(fill="x")

        tk.Label(
            head,
            text=f"🔑 Wi-Fi Trường ({ssid_name})",
            font=("Segoe UI", 11, "bold"),
            fg=self.INK,
            bg=self.BG,
        ).pack(anchor="w")
        tk.Label(
            head,
            text="Tùy chọn: Nhập tài khoản để tự động lưu & khôi phục (WIP - Có thể chưa hoạt động tùy bản Windows). Bấm Bỏ Qua nếu chỉ muốn sao lưu Wi-Fi thường.",
            font=("Segoe UI", 9),
            fg=self.MUTED,
            bg=self.BG,
            wraplength=380,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        tk.Frame(self, bg=self.BORDER, height=1).pack(fill="x", padx=18, pady=(8, 0))

        # Body Form
        body = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        body.pack(fill="both", expand=True)

        # Username Field
        tk.Label(
            body,
            text="USERNAME / MSSV",
            font=("Segoe UI", 9, "bold"),
            fg="#71717A",
            bg=self.BG,
        ).pack(anchor="w")

        u_frame = tk.Frame(
            body, bg=self.SURFACE, highlightbackground=self.BORDER, highlightthickness=1
        )
        u_frame.pack(fill="x", pady=(4, 10))

        self.ent_user = tk.Entry(
            u_frame,
            font=("Segoe UI", 10),
            bg=self.SURFACE,
            fg=self.INK,
            insertbackground=self.INK,
            bd=0,
            relief="flat",
        )
        self.ent_user.pack(fill="x", padx=8, pady=6)
        if default_user:
            self.ent_user.insert(0, default_user)
        else:
            self.ent_user.focus_set()

        # Password Field
        tk.Label(
            body,
            text="PASSWORD / MẬT KHẨU",
            font=("Segoe UI", 9, "bold"),
            fg="#71717A",
            bg=self.BG,
        ).pack(anchor="w")

        p_frame = tk.Frame(
            body, bg=self.SURFACE, highlightbackground=self.BORDER, highlightthickness=1
        )
        p_frame.pack(fill="x", pady=(4, 8))

        self.ent_pass = tk.Entry(
            p_frame,
            font=("Segoe UI", 10),
            bg=self.SURFACE,
            fg=self.INK,
            insertbackground=self.INK,
            bd=0,
            relief="flat",
            show="•",
        )
        self.ent_pass.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=6)

        self.show_pwd = False
        self.btn_toggle = tk.Label(
            p_frame,
            text="👁",
            font=("Segoe UI", 10),
            fg="#71717A",
            bg=self.SURFACE,
            cursor="hand2",
        )
        self.btn_toggle.pack(side="right", padx=6)
        self.btn_toggle.bind("<Button-1>", self.toggle_password_visibility)

        # Action Buttons
        btn_box = tk.Frame(self, bg=self.BG, padx=18, pady=12)
        btn_box.pack(fill="x", side="bottom")

        btn_save = tk.Button(
            btn_box,
            text="Lưu Tài Khoản",
            font=("Segoe UI", 9, "bold"),
            bg=self.INK,
            fg=self.BG,
            activebackground="#E4E4E7",
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.on_save,
        )
        btn_save.pack(side="right", padx=(6, 0))

        btn_skip = tk.Button(
            btn_box,
            text="Bỏ Qua",
            font=("Segoe UI", 9),
            bg=self.SURFACE,
            fg=self.MUTED,
            activebackground=self.BORDER,
            activeforeground=self.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.destroy,
        )
        btn_skip.pack(side="right")

        self.center_modal(420, 330)

    def toggle_password_visibility(self, event=None):
        self.show_pwd = not self.show_pwd
        if self.show_pwd:
            self.ent_pass.config(show="")
            self.btn_toggle.config(fg=self.INK)
        else:
            self.ent_pass.config(show="•")
            self.btn_toggle.config(fg="#71717A")

    def on_save(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        if u and p:
            self.result = (u, p)
            self.destroy()


class CustomToast(ImpeccableDialog):
    """Zinc-styled Notification Toast Modal with auto-calculated height & perfect centering."""

    def __init__(self, parent, title, message, is_error=False, app_icon_path=None):
        super().__init__(parent, title, app_icon_path)

        # Header
        head = tk.Frame(self, bg=self.BG, padx=16, pady=10)
        head.pack(fill="x")

        icon_str = "❌ " if is_error else "✓ "
        lbl = tk.Label(
            head,
            text=icon_str + title,
            font=("Segoe UI", 10, "bold"),
            fg="#EF4444" if is_error else "#10B981",
            bg=self.BG,
        )
        lbl.pack(anchor="w")

        tk.Frame(self, bg=self.BORDER, height=1).pack(fill="x", padx=16)

        # Body Message
        body = tk.Frame(self, bg=self.BG, padx=16, pady=10)
        body.pack(fill="both", expand=True)

        msg_lbl = tk.Label(
            body,
            text=message,
            font=("Segoe UI", 8),
            fg="#D4D4D8",
            bg=self.BG,
            justify="left",
            wraplength=280,
            anchor="nw",
        )
        msg_lbl.pack(fill="both", expand=True)

        # Bottom Button
        btn_box = tk.Frame(self, bg=self.BG, padx=16, pady=10)
        btn_box.pack(fill="x", side="bottom")

        btn_close = tk.Button(
            btn_box,
            text="Đã Hiểu",
            font=("Segoe UI", 8, "bold"),
            bg=self.SURFACE,
            fg=self.INK,
            activebackground=self.BORDER,
            activeforeground=self.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=5,
            command=self.destroy,
        )
        btn_close.pack(fill="x")

        self.center_modal(320, 180)


class ChangelogDialog(ImpeccableDialog):
    """Zinc-styled Changelog Modal."""

    def __init__(self, parent, app_icon_path=None):
        super().__init__(parent, "Changelog - WifiRescue", app_icon_path)

        # Header
        head = tk.Frame(self, bg=self.BG, padx=18, pady=12)
        head.pack(fill="x")

        tk.Label(
            head,
            text="🚀 NHẬT KÝ THAY ĐỔI (CHANGELOG)",
            font=("Segoe UI", 10, "bold"),
            fg=self.INK,
            bg=self.BG,
        ).pack(anchor="w")
        tk.Label(
            head,
            text=f"WifiRescue by QuiNC · Hiện tại: v{__version__}",
            font=("Segoe UI", 8),
            fg=self.MUTED,
            bg=self.BG,
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(self, bg=self.BORDER, height=1).pack(fill="x", padx=18)

        # Content
        body = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        body.pack(fill="both", expand=True)

        changelog_text = (
            "🔥 v1.3.0 (Phiên bản mới nhất):\n"
            "• Thêm nút '⚙ Quản Lý / Xóa Wi-Fi Đã Lưu' trên Windows.\n"
            "• Sửa lỗi tự động đăng nhập FU-Students (WPA2 802.1X).\n"
            "• Tự động vá thẻ XML <cacheCredentials>true</cacheCredentials>.\n"
            "• Đa dạng hóa Target Credential & netsh profileparameter.\n\n"
            "✨ v1.2.0:\n"
            "• Giao diện Modal & Toast Impeccable Zinc Dark Mode.\n"
            "• Thêm nút 👁 hiện/ẩn mật khẩu khi nhập tài khoản.\n"
            "• Khử trùng lặp Popup khi có nhiều Wi-Fi Enterprise.\n"
            "• Căn giữa màn hình (Center Modal) & Sửa lỗi Font.\n\n"
            "⚡ v1.1.0:\n"
            "• Hỗ trợ tự động sao lưu & khôi phục tài khoản\n"
            "  Wi-Fi Trường FU-Students (WPA2 802.1X Enterprise).\n"
            "• Tích hợp lệnh cmdkey vào Windows Credential Manager.\n\n"
            "🎉 v1.0.0:\n"
            "• Phát hành chính thức ứng dụng Portable WifiRescue."
        )

        txt = tk.Label(
            body,
            text=changelog_text,
            font=("Segoe UI", 8),
            fg="#D4D4D8",
            bg=self.BG,
            justify="left",
            anchor="nw",
        )
        txt.pack(fill="both", expand=True)

        btn_box = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        btn_box.pack(fill="x", side="bottom")

        btn_close = tk.Button(
            btn_box,
            text="Đóng",
            font=("Segoe UI", 8, "bold"),
            bg=self.SURFACE,
            fg=self.INK,
            activebackground=self.BORDER,
            activeforeground=self.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=5,
            command=self.destroy,
        )
        btn_close.pack(fill="x")

        self.center_modal(360, 360)


class ManageProfilesDialog(ImpeccableDialog):
    """Dialog for listing all saved Windows Wi-Fi profiles and selectively deleting/forgetting them."""

    def __init__(self, parent, app_icon_path=None):
        super().__init__(parent, "Quản Lý Wi-Fi Đã Lưu", app_icon_path)

        # Header
        head = tk.Frame(self, bg=self.BG, padx=18, pady=12)
        head.pack(fill="x")

        tk.Label(
            head,
            text="📶 DANH SÁCH WI-FI ĐÃ LƯU TRÊN MÁY",
            font=("Segoe UI", 10, "bold"),
            fg=self.INK,
            bg=self.BG,
        ).pack(anchor="w")
        tk.Label(
            head,
            text="Chọn mạng Wi-Fi và bấm Xóa để Forget profile khỏi Windows.",
            font=("Segoe UI", 8),
            fg=self.MUTED,
            bg=self.BG,
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(self, bg=self.BORDER, height=1).pack(fill="x", padx=18)

        # Listbox Frame
        body = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        body.pack(fill="both", expand=True)

        list_frame = tk.Frame(
            body, bg=self.SURFACE, highlightbackground=self.BORDER, highlightthickness=1
        )
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg=self.SURFACE,
            fg=self.INK,
            selectbackground="#27272A",
            selectforeground="#10B981",
            bd=0,
            relief="flat",
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)
        scrollbar.config(command=self.listbox.yview)

        # Bottom Buttons
        btn_box = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        btn_box.pack(fill="x", side="bottom")

        btn_delete = tk.Button(
            btn_box,
            text="🗑 Xóa Mạng Đã Chọn",
            font=("Segoe UI", 8, "bold"),
            bg="#EF4444",
            fg="#FFFFFF",
            activebackground="#DC2626",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.delete_selected,
        )
        btn_delete.pack(side="right", padx=(6, 0))

        btn_close = tk.Button(
            btn_box,
            text="Đóng",
            font=("Segoe UI", 8),
            bg=self.SURFACE,
            fg=self.MUTED,
            activebackground=self.BORDER,
            activeforeground=self.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.destroy,
        )
        btn_close.pack(side="right")

        self.load_profiles()
        self.center_modal(380, 340)

    def load_profiles(self):
        self.listbox.delete(0, tk.END)
        try:
            res = subprocess.run(
                "netsh wlan show profiles",
                capture_output=True,
                text=True,
                shell=True,
                encoding="utf-8",
                errors="ignore",
            )
            profiles = []
            for line in res.stdout.splitlines():
                if ":" in line:
                    p_name = line.split(":", 1)[1].strip()
                    if p_name and p_name != "<None>":
                        profiles.append(p_name)
            for p in sorted(profiles):
                self.listbox.insert(tk.END, f"  {p}")
            if not profiles:
                self.listbox.insert(tk.END, " (Không có Wi-Fi nào đã lưu)")
        except Exception as e:
            self.listbox.insert(tk.END, f" Lỗi: {e}")

    def delete_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        item_text = self.listbox.get(sel[0]).strip()
        if item_text.startswith("(") or item_text.startswith("Lỗi"):
            return

        cmd = f'netsh wlan delete profile name="{item_text}"'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if res.returncode == 0:
            # Also clean up WLEA credential if present
            target = f"Microsoft_Wlea_{item_text}"
            subprocess.run(
                f"cmdkey /delete:{target}", capture_output=True, text=True, shell=True
            )
            
            # Synchronize with WiFi_Backup directory: remove corresponding XML backup file(s)
            if BACKUP_DIR.exists():
                for xml_file in BACKUP_DIR.glob("*.xml"):
                    # netsh exports profiles as Wi-Fi-{SSID}.xml or {SSID}.xml
                    stem_name = xml_file.stem
                    if stem_name.startswith("Wi-Fi-"):
                        stem_name = stem_name[6:]
                    if stem_name.strip().lower() == item_text.lower():
                        try:
                            xml_file.unlink()
                        except Exception:
                            pass

                # Remove from enterprise_credentials.json if exists
                if CREDENTIALS_FILE.exists():
                    try:
                        creds = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
                        matching_keys = [k for k in creds if k.lower() == item_text.lower()]
                        if matching_keys:
                            for k in matching_keys:
                                del creds[k]
                            CREDENTIALS_FILE.write_text(
                                json.dumps(creds, indent=2, ensure_ascii=False),
                                encoding="utf-8",
                            )
                    except Exception:
                        pass

            self.load_profiles()
        else:
            messagebox.showerror("Lỗi", f"Không thể xóa profile: {res.stderr}")


class CompactWifiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WifiRescue - by QuiNC")
        self.root.geometry("340x290")
        self.root.resizable(False, False)

        self.icon_path = BUNDLE_DIR / "app_icon_flat.ico"
        if self.icon_path.exists():
            try:
                self.root.iconbitmap(str(self.icon_path))
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

        # Check for remote updates in background thread
        threading.Thread(target=self.check_update_async, daemon=True).start()

    def check_update_async(self):
        """Fetch latest release tag from GitHub API in background."""
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "WifiRescue-App"})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    html_url = data.get(
                        "html_url", f"https://github.com/{GITHUB_REPO}/releases"
                    )
                    notes = data.get("body", "")

                    if latest_tag and self.is_newer_version(latest_tag, __version__):
                        self.root.after(
                            0,
                            lambda: UpdatePromptDialog(
                                self.root,
                                f"v{latest_tag}",
                                html_url,
                                notes,
                                self.icon_path,
                            ),
                        )
        except Exception:
            pass

    @staticmethod
    def is_newer_version(latest, current):
        """Parse version strings like 1.2.0 and compare tuple (1, 2, 0)."""
        try:
            p_latest = tuple(map(int, latest.split(".")))
            p_current = tuple(map(int, current.split(".")))
            return p_latest > p_current
        except Exception:
            return False

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
            anchor="w",
        )
        lbl_title.pack(side="left")

        right_links = tk.Frame(header, bg=self.COLOR_BG)
        right_links.pack(side="right")

        btn_ver = tk.Label(
            right_links,
            text=f"v{__version__}",
            font=self.FONT_SMALL,
            fg="#10B981",
            bg=self.COLOR_BG,
            cursor="hand2",
        )
        btn_ver.pack(side="left", padx=(0, 8))
        btn_ver.bind("<Button-1>", lambda e: self.show_changelog_popup())

        btn_help = tk.Label(
            right_links,
            text="❓ Help",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            cursor="hand2",
        )
        btn_help.pack(side="left", padx=(0, 8))
        btn_help.bind("<Button-1>", lambda e: self.show_help_popup())

        btn_folder = tk.Label(
            right_links,
            text="📁 Folder",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            cursor="hand2",
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
            command=self.backup_wifi,
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
            command=self.restore_wifi,
        )
        self.btn_restore.pack(fill="x", pady=(0, 8))

        self.btn_manage = tk.Button(
            content,
            text="⚙ QUẢN LÝ / XÓA WI-FI ĐÃ LƯU",
            font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_MUTED,
            activebackground=self.COLOR_BORDER,
            activeforeground=self.COLOR_INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=6,
            command=self.show_manage_popup,
        )
        self.btn_manage.pack(fill="x", pady=(0, 8))

        # Checkbox Option to Skip Enterprise Prompt (WIP)
        self.skip_enterprise_var = tk.BooleanVar(value=False)
        self.chk_skip_ent = tk.Checkbutton(
            content,
            text="Bỏ qua Wi-Fi Enterprise (Tạm thời test / WIP)",
            variable=self.skip_enterprise_var,
            font=("Segoe UI", 9),
            fg="#A1A1AA",
            bg=self.COLOR_BG,
            activebackground=self.COLOR_BG,
            activeforeground=self.COLOR_INK,
            selectcolor=self.COLOR_SURFACE,
            bd=0,
            highlightthickness=0,
            anchor="w",
        )
        self.chk_skip_ent.pack(fill="x")

        # Footer Status Bar
        footer = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=8)
        footer.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(
            footer,
            text="STATUS: READY",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG,
            anchor="w",
        )
        self.lbl_status.pack(side="left")

        lbl_sig = tk.Label(
            footer,
            text="by QuiNC",
            font=self.FONT_SIG,
            fg=self.COLOR_WATERMARK,
            bg=self.COLOR_BG,
            anchor="e",
        )
        lbl_sig.pack(side="right")

    def show_changelog_popup(self):
        ChangelogDialog(self.root, self.icon_path)

    def show_manage_popup(self):
        ManageProfilesDialog(self.root, self.icon_path)

    def show_help_popup(self):
        popup = ImpeccableDialog(
            self.root, "Hướng Dẫn Sử Dụng - WifiRescue", self.icon_path
        )

        # Header
        head = tk.Frame(popup, bg=popup.BG, padx=18, pady=12)
        head.pack(fill="x")

        tk.Label(
            head,
            text="📖 HƯỚNG DẪN SỬ DỤNG",
            font=("Segoe UI", 10, "bold"),
            fg=popup.INK,
            bg=popup.BG,
        ).pack(anchor="w")
        tk.Label(
            head,
            text="Tác giả: QuiNC · Phiên bản Portable",
            font=("Segoe UI", 8),
            fg=popup.MUTED,
            bg=popup.BG,
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(popup, bg=popup.BORDER, height=1).pack(fill="x", padx=18)

        body_f = tk.Frame(popup, bg=popup.BG, padx=18, pady=12)
        body_f.pack(fill="both", expand=True)

        steps_text = (
            "1. Trước khi đi thi (Sao lưu):\n"
            "   Mở app ➔ Bấm BACKUP PROFILES để lưu toàn bộ Wi-Fi.\n"
            "   Nếu có Wi-Fi Trường (FU-Students), app sẽ hiển thị\n"
            "   popup nhập Username & Password chung để sao lưu.\n\n"
            "2. Sau khi thi xong (Khôi phục):\n"
            "   Mở app ➔ Bấm RESTORE PROFILES để nạp lại Wi-Fi\n"
            "   và tự động đăng nhập FU-Students không cần gõ lại!\n\n"
            "💡 Lưu ý: Nếu Windows báo màn hình xanh lần đầu,\n"
            "   chọn More info ➔ chọn Run anyway để chạy."
        )

        txt = tk.Label(
            body_f,
            text=steps_text,
            font=("Segoe UI", 8),
            fg="#D4D4D8",
            bg=popup.BG,
            justify="left",
            anchor="nw",
        )
        txt.pack(fill="both", expand=True)

        btn_box = tk.Frame(popup, bg=popup.BG, padx=18, pady=10)
        btn_box.pack(fill="x", side="bottom")

        btn_close = tk.Button(
            btn_box,
            text="Đã Hiểu",
            font=("Segoe UI", 8, "bold"),
            bg=popup.SURFACE,
            fg=popup.INK,
            activebackground=popup.BORDER,
            activeforeground=popup.INK,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=5,
            command=popup.destroy,
        )
        btn_close.pack(fill="x")

        popup.center_modal(360, 310)

    def backup_wifi(self):
        try:
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            cmd = f'netsh wlan export profile key=clear folder="{BACKUP_DIR}"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                count = len(list(BACKUP_DIR.glob("*.xml")))

                # Check for Enterprise SSIDs (like FU-Students, FU-Exams)
                ent_creds = {}
                if CREDENTIALS_FILE.exists():
                    try:
                        ent_creds = json.loads(
                            CREDENTIALS_FILE.read_text(encoding="utf-8")
                        )
                    except Exception:
                        pass

                # Find unique enterprise SSIDs
                ent_ssids = set()
                for xml_file in BACKUP_DIR.glob("*.xml"):
                    try:
                        content = xml_file.read_text(encoding="utf-8", errors="ignore")
                        if "<useOneX>true</useOneX>" in content:
                            name_part = xml_file.stem
                            if name_part.startswith("Wi-Fi-"):
                                name_part = name_part[6:]
                            ent_ssids.add(name_part)
                    except Exception:
                        pass

                # Prompt for each unique enterprise SSID sequentially (unless skipped via checkbox)
                if not self.skip_enterprise_var.get():
                    for ssid in sorted(ent_ssids):
                        def_u = ent_creds.get(ssid, {}).get("user", "")
                        dlg = EnterpriseCredentialDialog(
                            self.root, ssid, self.icon_path, default_user=def_u
                        )
                        self.root.wait_window(dlg)

                        if dlg.result:
                            u, p = dlg.result
                            ent_creds[ssid] = {"user": u, "pass": p}

                    if ent_creds:
                        CREDENTIALS_FILE.write_text(
                            json.dumps(ent_creds, indent=2), encoding="utf-8"
                        )

                self.lbl_status.config(
                    text=f"STATUS: BACKED UP {count} PROFILES", fg=self.COLOR_INK
                )
                toast = CustomToast(
                    self.root,
                    "Sao Lưu Thành Công",
                    f"Đã sao lưu thành công {count} cấu hình Wi-Fi vào thư mục:\n{BACKUP_DIR}",
                    app_icon_path=self.icon_path,
                )
                self.root.wait_window(toast)
            else:
                self.lbl_status.config(text="STATUS: BACKUP FAILED", fg="#EF4444")
                toast = CustomToast(
                    self.root,
                    "Sao Lưu Thất Bại",
                    f"Không thể xuất cấu hình Wi-Fi.\n{result.stderr}",
                    is_error=True,
                    app_icon_path=self.icon_path,
                )
                self.root.wait_window(toast)
        except Exception as e:
            toast = CustomToast(
                self.root,
                "Lỗi Hệ Thống",
                str(e),
                is_error=True,
                app_icon_path=self.icon_path,
            )
            self.root.wait_window(toast)

    def restore_wifi(self):
        if not BACKUP_DIR.exists():
            CustomToast(
                self.root,
                "Cảnh Báo",
                "Không tìm thấy thư mục WiFi_Backup trong ứng dụng.",
                is_error=True,
                app_icon_path=self.icon_path,
            )
            return

        xml_files = list(BACKUP_DIR.glob("*.xml"))
        if not xml_files:
            CustomToast(
                self.root,
                "Cảnh Báo",
                "Không tìm thấy file cấu hình XML nào.",
                is_error=True,
                app_icon_path=self.icon_path,
            )
            return

        existing_profiles = []
        try:
            show_res = subprocess.run(
                "netsh wlan show profiles",
                capture_output=True,
                text=True,
                shell=True,
                encoding="utf-8",
                errors="ignore",
            )
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

        # Load Enterprise credentials if available (and if not skipped via checkbox)
        ent_creds = {}
        skip_ent = self.skip_enterprise_var.get()
        if CREDENTIALS_FILE.exists() and not skip_ent:
            try:
                ent_creds = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass

        for xml_file in xml_files:
            name_part = xml_file.stem
            if name_part.startswith("Wi-Fi-"):
                name_part = name_part[6:]

            # Check if this profile is Enterprise (useOneX)
            is_enterprise = False
            try:
                xml_content = xml_file.read_text(encoding="utf-8", errors="ignore")
                if "<useOneX>true</useOneX>" in xml_content:
                    is_enterprise = True
                    # Patch XML to ensure cacheCredentials is set to true if missing
                    if "<cacheCredentials>false</cacheCredentials>" in xml_content:
                        xml_content = xml_content.replace(
                            "<cacheCredentials>false</cacheCredentials>",
                            "<cacheCredentials>true</cacheCredentials>",
                        )
                        xml_file.write_text(xml_content, encoding="utf-8")
                    elif (
                        "<cacheCredentials>" not in xml_content
                        and "</OneX>" in xml_content
                    ):
                        xml_content = xml_content.replace(
                            "</OneX>",
                            "    <cacheCredentials>true</cacheCredentials>\n    </OneX>",
                        )
                        xml_file.write_text(xml_content, encoding="utf-8")
            except Exception:
                pass

            # Add profile
            if name_part.lower() not in existing_profiles:
                cmd = f'netsh wlan add profile filename="{xml_file}" user=all'
                res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                if res.returncode == 0:
                    new_restored_count += 1
                else:
                    failed_count += 1
            else:
                already_existed_count += 1

            # Inject Enterprise Credentials via both cmdkey AND netsh profileparameter if present (and not skipped)
            if not skip_ent and name_part in ent_creds:
                u = ent_creds[name_part]["user"]
                p = ent_creds[name_part]["pass"]

                # 1. Target Generic for WLEA
                target = f"Microsoft_Wlea_{name_part}"
                cmd_cred = f'cmdkey /generic:{target} /user:"{u}" /pass:"{p}"'
                subprocess.run(cmd_cred, capture_output=True, text=True, shell=True)

                # 2. Also target Domain/Server style targets for 802.1X
                target_domain = f"Microsoft_Wlea_{name_part.lower()}"
                if target_domain != target:
                    cmd_cred_dom = (
                        f'cmdkey /generic:{target_domain} /user:"{u}" /pass:"{p}"'
                    )
                    subprocess.run(
                        cmd_cred_dom, capture_output=True, text=True, shell=True
                    )

                # 3. Force netsh wlan set profileparameter key=userData if applicable
                try:
                    cmd_param = f'netsh wlan set profileparameter name="{name_part}" key=userData'
                    subprocess.run(
                        cmd_param, capture_output=True, text=True, shell=True
                    )
                except Exception:
                    pass

        total = len(xml_files)
        if already_existed_count == total and not ent_creds:
            status_text = "STATUS: ALL PROFILES ALREADY EXIST"
            if skip_ent:
                status_text += " (ENTERPRISE SKIPPED)"
            self.lbl_status.config(text=status_text, fg=self.COLOR_INK)
            msg_exist = f"Toàn bộ {total} cấu hình Wi-Fi đã sẵn có trên máy tính này."
            if skip_ent:
                msg_exist += (
                    "\n(Đã bỏ qua nạp tài khoản Wi-Fi Enterprise theo yêu cầu)."
                )
            CustomToast(
                self.root,
                "Thông Báo",
                msg_exist,
                app_icon_path=self.icon_path,
            )
        elif new_restored_count > 0 or ent_creds or skip_ent:
            msg = f"Đã khôi phục thành công các cấu hình Wi-Fi."
            if new_restored_count > 0:
                msg += f"\n• Nạp thêm: {new_restored_count} Wi-Fi mới."
            if skip_ent:
                msg += "\n• Đã bỏ qua nạp tài khoản Wi-Fi Enterprise (WIP)."
            elif ent_creds:
                msg += f"\n• Tự động đăng nhập tài khoản: {', '.join(ent_creds.keys())}"
            self.lbl_status.config(text=f"STATUS: RESTORED SUCCESS", fg=self.COLOR_INK)
            CustomToast(
                self.root, "Khôi Phục Thành Công", msg, app_icon_path=self.icon_path
            )
        else:
            self.lbl_status.config(text="STATUS: RESTORE FAILED", fg="#EF4444")
            CustomToast(
                self.root,
                "Khôi Phục Thất Bại",
                "Không thể khôi phục các cấu hình Wi-Fi.",
                is_error=True,
                app_icon_path=self.icon_path,
            )

    def open_backup_dir(self):
        if not BACKUP_DIR.exists():
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        os.startfile(BACKUP_DIR)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompactWifiApp(root)
    root.mainloop()
