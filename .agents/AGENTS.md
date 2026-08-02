# Project Rules - WifiRescue

## Git Commit & Release Documentation Workflow

Mỗi khi nâng cấp phiên bản (Release), sửa đổi tính năng chính hoặc chuẩn bị `git push`, BẮT BUỘC thực hiện đúng và đầy đủ danh sách kiểm tra (Checklist) sau:

1. **Cập nhật Nhật ký Hệ thống & Tài liệu:**
   - `README.md`: Cập nhật mục **Changelog / Nhật ký thay đổi**, hướng dẫn sử dụng và ghi chú kỹ thuật.
   - `index.html` (Landing page / GitHub Pages): Cập nhật thông tin phiên bản mới, mô tả tính năng VÀ rà soát kiểm tra toàn bộ các liên kết nút tải đính kèm (`https://github.com/.../releases/download/vX.X.X/WifiRescue.zip`) đảm bảo đúng tag version mới nhất.
   - `.agents/doc/context-snapshot.md`: Cập nhật trạng thái ngữ cảnh, cấu trúc phiên bản hiện tại.
   - `.agents/doc/implementation_plan.md`: Đánh dấu task hoàn thành và kế hoạch tiếp theo.
   - Trong ứng dụng (GUI): Cập nhật hằng số version (`__version__`), popup Changelog và nhãn hiển thị version trên thanh giao diện (Header).

2. **Lưu ý Cấu hình Wi-Fi Enterprise (802.1X / FU-Students):**
   - Luôn duy trì tính năng vá thẻ XML `<cacheCredentials>true</cacheCredentials>` và tùy chọn Checkbox Bỏ Qua (WIP) ngoài màn hình chính.
   - Luôn đảm bảo cỡ font trong Tkinter là số nguyên (`int`) và các chuỗi Release Notes hiển thị trên Dialog được làm sạch các ký tự Markdown rác.

3. **Rà soát Bảo mật & Dữ liệu Nhạy cảm (Security Audit):**
   - Kiểm tra file `.gitignore`: Đảm bảo các thư mục dữ liệu cá nhân (như `WiFi_Backup/`), file mật khẩu (`enterprise_credentials.json`), API Key, `.env`, hoặc file build tạm đều đã được thêm vào `.gitignore`.
   - Kiểm tra `git status` & `git diff`: Rà soát không có file chứa thông tin thực/mật khẩu cá nhân nào nằm trong danh sách sắp commit.

4. **Quản Lý Phiên Bản & Remote Auto-Update Check:**
   - Khi phát triển tính năng mới hoặc sửa lỗi, luôn ghi nhớ nâng hằng số phiên bản (`__version__`) trong `wifi_manager.py` (ví dụ: `1.2.0` -> `1.3.0`).
   - Đảm bảo cơ chế tự động kiểm tra phiên bản ngầm qua GitHub API (`https://api.github.com/repos/quinc-fptu/WifiRescue/releases/latest`) hoạt động đúng để các máy sinh viên nhận được thông báo cập nhật từ xa khi có Release mới.

5. **Build & Đóng gói:**
   - Thực hiện đóng gói build chính thức (`PyInstaller` / `npm build`), kiểm tra cấu trúc zip sản phẩm cuối trước khi tạo GitHub Release.

