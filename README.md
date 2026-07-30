# 📶 WifiRescue - Windows Wi-Fi Backup & Restore Tool

**WifiRescue** là công cụ portable nhỏ gọn giúp sinh viên **FPTU** sao lưu và khôi phục toàn bộ mật khẩu Wi-Fi (bao gồm cả tài khoản Wi-Fi trường **FU-Students** / WPA2 Enterprise) trên Windows chỉ trong 1-click mỗi lần đi thi bị bắt "Forget Wi-Fi".

Tác giả: **QuiNC** · Phiên bản: **v1.2.0**

---

## 🌟 Tính Năng Nổi Bật (v1.2.0)

- **1-Click Backup & Restore:** Sao lưu và khôi phục Wi-Fi trong 1s với phân quyền chuẩn FPTU (`user=all`).
- **Enterprise Auto-Login:** Tự động lưu & nạp lại Username / Password cho mạng trường **FU-Students** (802.1X Enterprise) qua Windows Credential Manager.
- **Impeccable Zinc Dark Theme UI:** Giao diện Modal & Toast Notification thiết kế chuẩn Impeccable Zinc Dark Mode.
- **Password Eye Toggle (👁):** Form nhập tài khoản thông minh cho phép bật/tắt hiển thị mật khẩu để kiểm tra chính xác trước khi lưu.
- **Sequential Modal Windowing:** Tự động gộp các SSID Enterprise trùng lặp và hiển thị từng thông báo tuần tự, không bị đè cửa sổ.
- **100% Single File Executable Portable:** Chạy trực tiếp file `WifiRescue.exe` không cần cài đặt.

---

## 💡 Lưu Ý Về Wi-Fi Trường (FU-Students / WPA2 Enterprise)

- **Vì sao cần nhập tài khoản 1 lần khi Backup?**  
  Khác với Wi-Fi cá nhân (WPA2-Personal) lưu mật khẩu rõ ràng trong file XML, Wi-Fi trường học (**FU-Students**) sử dụng mã hóa doanh nghiệp **802.1X (EAP-PEAP)**. Mật khẩu được Windows mã hóa 1 chiều bảo mật trong hệ thống (LSA Secrets) nên không thể trích xuất trực tiếp dạng văn bản thô.
- **Giải pháp của WifiRescue:**  
  Bạn chỉ cần nhập Username/Password **1 lần duy nhất** khi bấm Backup. Thông tin này sẽ được lưu an toàn trong file `enterprise_credentials.json` đi kèm. Khi sang máy mới hoặc sau khi thi xong, bấm **RESTORE PROFILES** thì tool sẽ tự động đăng nhập vào Windows Credential Manager mà **không bao giờ phải nhập lại nữa!**

---

## 📖 Hướng Dẫn Sử Dụng

1. **Tải về & Giải nén:** Tải `WifiRescue.zip` từ [Releases](https://github.com/quinc-fptu/WifiRescue/releases) và giải nén ra thư mục.
2. **Trước khi thi (Backup):** Mở `WifiRescue.exe` ➔ Bấm **BACKUP PROFILES**. Nhập Username/Password Wi-Fi **FU-Students** 1 lần duy nhất để lưu lại.
3. **Sau khi thi (Restore):** Mở `WifiRescue.exe` ➔ Bấm **RESTORE PROFILES**. Mọi Wi-Fi và tài khoản **FU-Students** sẽ tự động được nạp lại vào Windows mà không cần nhập thủ công!

---

## 🌐 Trang Web Hướng Dẫn
👉 [https://quinc-fptu.github.io/WifiRescue/](https://quinc-fptu.github.io/WifiRescue/)

---

## 🛡️ Bản Quyền
Copyright (c) 2026 QuiNC. All rights reserved.



