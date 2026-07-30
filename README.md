<div align="center">

<img src="favicon.svg" width="64" height="64" alt="WifiRescue Icon" />

# WifiRescue

**Công cụ 1-click sao lưu & khôi phục Wi-Fi cho sinh viên FPTU.**  
Không bao giờ phải cấu hình lại mạng sau mỗi buổi thi PE/FE nữa.

[![Release](https://img.shields.io/github/v/release/quinc-fptu/WifiRescue?style=flat-square&color=18181b&labelColor=09090b&label=Latest)](https://github.com/quinc-fptu/WifiRescue/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/quinc-fptu/WifiRescue/total?style=flat-square&color=18181b&labelColor=09090b)](https://github.com/quinc-fptu/WifiRescue/releases)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&color=18181b&labelColor=09090b)](https://github.com/quinc-fptu/WifiRescue)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square&color=18181b&labelColor=09090b)](https://github.com/quinc-fptu/WifiRescue/blob/main/LICENSE)

[**⬇ Tải ngay**](https://github.com/quinc-fptu/WifiRescue/releases/latest) · [**📄 Trang hướng dẫn**](https://quinc-fptu.github.io/WifiRescue/) · [**🐛 Báo lỗi**](https://github.com/quinc-fptu/WifiRescue/issues)

</div>

---

## Vấn đề

Mỗi lần thi PE/FE tại FPTU, máy tính bị bắt **Forget Wi-Fi** trước khi vào phòng thi. Sau khi thi xong, sinh viên phải kết nối lại thủ công từng mạng — đặc biệt với **FU-Students** (WPA2 Enterprise / 802.1X) đòi hỏi đăng nhập tài khoản và cấu hình lại rất mất thời gian.

**WifiRescue** giải quyết hoàn toàn vấn đề này chỉ với 2 lần bấm nút.

---

## Tính năng

| Tính năng | Mô tả |
|---|---|
| **1-Click Backup** | Sao lưu toàn bộ Wi-Fi Profile với phân quyền FPTU (`user=all`) |
| **1-Click Restore** | Khôi phục tất cả mạng và đăng nhập tự động vào Windows |
| **Enterprise Auto-Login** | Tự lưu & nạp lại tài khoản **FU-Students** (802.1X) qua Credential Manager |
| **Password Eye Toggle** | Xem/ẩn mật khẩu khi nhập để kiểm tra trước khi lưu |
| **Auto Update Check** | Tự động kiểm tra phiên bản mới từ GitHub Releases khi khởi động |
| **Portable .exe** | Chạy thẳng file, không cần cài đặt, không phụ thuộc Python |

---

## Cài đặt & Sử dụng

### Bước 1 — Tải về

Tải file `WifiRescue.zip` từ **[Releases](https://github.com/quinc-fptu/WifiRescue/releases/latest)** và giải nén ra thư mục bất kỳ.

```
WifiRescue/
├── WifiRescue.exe        ← Chạy file này
└── WiFi_Backup/          ← Tự tạo khi Backup lần đầu
    ├── *.xml             (Profile Wi-Fi)
    └── enterprise_credentials.json  (Tài khoản FU-Students — KHÔNG share)
```

### Bước 2 — Trước khi thi (Backup)

1. Mở `WifiRescue.exe`
2. Bấm **BACKUP PROFILES**
3. Nhập Username / Password **FU-Students** khi được hỏi *(chỉ 1 lần duy nhất)*

### Bước 3 — Sau khi thi (Restore)

1. Mở `WifiRescue.exe`
2. Bấm **RESTORE PROFILES**
3. Tất cả Wi-Fi và tài khoản **FU-Students** tự động nạp lại — không cần nhập gì thêm!

---

## Lưu ý về FU-Students (802.1X Enterprise)

Wi-Fi trường sử dụng chuẩn **EAP-PEAP (802.1X)** — mật khẩu được Windows mã hóa 1 chiều trong LSA Secrets, không thể trích xuất dạng văn bản thô như Wi-Fi cá nhân.

> **Giải pháp:** WifiRescue yêu cầu bạn nhập tài khoản **1 lần duy nhất** khi Backup. Thông tin này được lưu cục bộ trong `WiFi_Backup/enterprise_credentials.json`. Mọi lần Restore sau đó, tool tự động đăng nhập vào Windows Credential Manager mà không cần nhập lại.

⚠️ **Không chia sẻ** thư mục `WiFi_Backup/` cho người khác vì chứa mật khẩu cá nhân.

---

## Changelog

### 🚀 v1.2.0 *(Latest)*
- **Impeccable Zinc Dark Theme** — Toàn bộ Dialog & Toast Notification thiết kế lại theo tiêu chuẩn Zinc Dark Mode
- **Password Eye Toggle (👁)** — Bật/tắt hiển thị mật khẩu trong form nhập tài khoản Enterprise
- **Deduplicated Enterprise Prompts** — Khử trùng lặp SSID, hiển thị 1 form nhập đại diện duy nhất
- **Auto-centered Modal & Geometry Fix** — Tự căn giữa cửa sổ, sửa lỗi font float trên Windows/Tkinter
- **Version & Changelog Viewer** — Nút hiển thị version `v1.2.0` trên Header để xem Changelog nhanh

### ⚡ v1.1.0
- **Enterprise Wi-Fi Auto-Login** — Tự động lưu & nạp lại tài khoản FU-Students (802.1X) qua `cmdkey`

### 🎉 v1.0.0
- Phát hành phiên bản Portable đầu tiên, hỗ trợ Backup & Restore 1-click chuẩn FPTU

---

## Bảo mật

- File `enterprise_credentials.json` **không được commit** lên Git (đã thêm vào `.gitignore`)
- Tool **không gửi dữ liệu** ra ngoài — tất cả xử lý cục bộ trên máy
- Kiểm tra phiên bản chỉ gọi GitHub API công khai (`/releases/latest`), không truyền thông tin cá nhân

---

<div align="center">

Made with ❤️ for FPTU students by **[QuiNC](https://github.com/quinc-fptu)**

</div>
