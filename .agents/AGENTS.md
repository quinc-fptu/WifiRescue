# Project Rules - WifiRescue

## Git Commit & Release Documentation Workflow

Mỗi khi nâng cấp phiên bản (Release), sửa đổi tính năng chính hoặc chuẩn bị `git push`, BẮT BUỘC thực hiện đúng và đầy đủ danh sách kiểm tra (Checklist) sau:

1. **Cập nhật Nhật ký Hệ thống & Tài liệu:**
   - `README.md`: Cập nhật mục **Changelog / Nhật ký thay đổi**, hướng dẫn sử dụng và ghi chú kỹ thuật.
   - `index.html` (Landing page / GitHub Pages): Cập nhật thông tin phiên bản mới, link tải đính kèm và mô tả tính năng.
   - `.agents/doc/context-snapshot.md`: Cập nhật trạng thái ngữ cảnh, cấu trúc phiên bản hiện tại.
   - `.agents/doc/implementation_plan.md`: Đánh dấu task hoàn thành và kế hoạch tiếp theo.
   - Trong ứng dụng (GUI): Cập nhật hằng số version (`__version__`), popup Changelog và nhãn hiển thị version trên thanh giao diện (Header).

2. **Rà soát Bảo mật & Dữ liệu Nhạy cảm (Security Audit):**
   - Kiểm tra file `.gitignore`: Đảm bảo các thư mục dữ liệu cá nhân (như `WiFi_Backup/`), file mật khẩu (`enterprise_credentials.json`), API Key, `.env`, hoặc file build tạm đều đã được thêm vào `.gitignore`.
   - Kiểm tra `git status` & `git diff`: Rà soát không có file chứa thông tin thực/mật khẩu cá nhân nào nằm trong danh sách sắp commit.

3. **Build & Đóng gói:**
   - Thực hiện đóng gói build chính thức (`PyInstaller` / `npm build`), kiểm tra cấu trúc zip sản phẩm cuối trước khi tạo GitHub Release.
