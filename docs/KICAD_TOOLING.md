# KICAD 9 TOOLING & MCP INTEGRATION SPECIFICATION

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Tài liệu**: Đặc tả Tích hợp Công cụ KiCad & MCP Toolchain cho AI Agent  
> **Phiên bản**: V1.0.0 — Toolchain Verification & Setup Complete  
> **Trạng thái**: `KICAD_TOOLCHAIN_READY`  

---

## 1. Thông Tin Môi Trường KiCad Cục Bộ (Local KiCad Environment)

- **Phiên bản KiCad phát hiện**: `KiCad 9.0.7` (Release build, Jan 2 2026, Visual C++ 1944).
- **Đường dẫn thư mục cài đặt**: `E:\kicad`
- **Đường dẫn kicad-cli**: `E:\kicad\bin\kicad-cli.exe`
- **Output xác thực CLI**:
  ```text
  kicad-cli version: 9.0.7
  ```
- **Kiểm tra lệnh ERC**:
  ```text
  kicad-cli sch erc --help -> Exit code 0 (Hỗ trợ đầy đủ cờ --format, --severity-all, --exit-code-violations)
  ```
- **Kiểm tra thư viện chuẩn (Standard Libraries)**:
  - Symbols: `E:\kicad\share\kicad\symbols\` (Device.kicad_sym, MCU_Espressif.kicad_sym, ...)
  - Footprints: `E:\kicad\share\kicad\footprints\`
- **Môi trường Python liên quan**:
  - Python hệ thống: `Python 3.12.0` (`C:\Users\phamt\AppData\Local\Programs\Python\Python312\python.exe`)
  - Python đi kèm KiCad: `Python 3.11.9` (`E:\kicad\bin\python.exe`, hỗ trợ `pcbnew`)
  - Trình quản lý gói: `uv 0.12.5`

---

## 2. Lựa Chọn & Cấu Hình MCP Server (Selected MCP Server)

### 2.1 Máy chủ MCP được chọn
- **Tên máy chủ**: `mcp-server-kicad`
- **Nguồn Repository**: [ProductOfAmerica/mcp-server-kicad](https://github.com/ProductOfAmerica/mcp-server-kicad)
- **Phiên bản PyPI**: `0.20.1`
- **Commit Git chính xác**: `511a50d6bf6f1a0df1b2c965443efa674d2fe618`
- **Lý do lựa chọn ưu tiên**:
  1. Hỗ trợ chính thức và tương thích trực tiếp với KiCad 9.x và 10.x trên Windows.
  2. Sử dụng kiến trúc Concrete Syntax Tree (CST) để chỉnh sửa file nguyên tử, bảo toàn 100% byte không thay đổi, loại bỏ nguy cơ làm hỏng định dạng S-expression.
  3. Cung cấp 109 công cụ MCP bao phủ toàn bộ vòng đời thiết kế (Project, Schematic, Symbol, Footprint, PCB, ERC, DRC, Export).
  4. **Không phụ thuộc vào GUI KiCad hay IPC API socket**: Có thể chạy headless hoàn toàn qua `kicad-cli`, không đòi hỏi người dùng bật plugin GUI phức tạp.

### 2.2 Vị trí cài đặt & Cấu hình Antigravity
- **Vị trí cài đặt thư viện**: `C:\Users\phamt\AppData\Local\Programs\Python\Python312\Lib\site-packages\mcp_server_kicad`
- **Script điều phối chuyên dụng**: `C:\Users\phamt\.gemini\antigravity\kicad\run_mcp.py`
  - Đảm bảo biến môi trường `KICAD_CLI_PATH = E:\kicad\bin\kicad-cli.exe` và bổ sung thư mục bin KiCad vào `PATH`.
- **Cấu hình Antigravity**: Đã đăng ký `"kicad"` trong cả 2 tệp cấu hình:
  - `C:\Users\phamt\.gemini\antigravity\mcp_config.json`
  - `C:\Users\phamt\.gemini\config\mcp_config.json`
- **Danh mục Tool Schema**: Toàn bộ 109 schema công cụ đã được trích xuất và lưu tại:
  `C:\Users\phamt\.gemini\antigravity\mcp\kicad\*.json`

---

## 3. Dự Án Skill Đã Tích Hợp (Project-Scoped Skill)

- **Tên Skill**: `using-kicad`
- **Vị trí cài đặt**: `e:\documents\dien_tu\embedded_sys\.agents\skills\using-kicad\SKILL.md`
- **Nguồn gốc (Provenance)**:
  - Repo: `https://github.com/ProductOfAmerica/mcp-server-kicad`
  - Commit: `511a50d6bf6f1a0df1b2c965443efa674d2fe618`
- **Vai trò**:
  - Khóa chặt quy tắc cấm sửa trực tiếp text trên file KiCad.
  - Định hướng thứ tự thao tác qua các cổng kiểm tra (BOM -> Schematic Plan -> Schematic Design -> ERC = 0 -> PCB Layout -> DRC = 0).

---

## 4. Các Thao Tác Cốt Lõi Khả Dụng (Core Operations Checklist)

| Thao tác yêu cầu | Tên công cụ MCP tương ứng | Nhóm chức năng | Trạng thái xác thực |
| :--- | :--- | :--- | :---: |
| **create_project** | `create_project` | Project Scaffolding | `VERIFIED (Smoke Test)` |
| **create_schematic** | `create_schematic` | Project Scaffolding | `VERIFIED (Smoke Test)` |
| **create_symbol_library**| `create_symbol_library` | Symbol Library | `VERIFIED` |
| **add_symbol** | `add_symbol` | Symbol Definition | `VERIFIED` |
| **place_component** | `place_component` | Schematic Capture | `VERIFIED (Smoke Test)` |
| **move_component** | `move_component` | Schematic Capture | `VERIFIED` |
| **connect_pins** | `connect_pins` | Schematic Wiring | `VERIFIED (Smoke Test)` |
| **wire_pins_to_net** | `wire_pins_to_net` | Schematic Wiring | `VERIFIED` |
| **add_label** | `add_label` | Net Naming | `VERIFIED` |
| **add_power_symbol** | `add_power_symbol` | Power Rails | `VERIFIED` |
| **get_schematic_summary**| `get_schematic_summary` | Inspection | `VERIFIED (Smoke Test)` |
| **get_symbol_pins** | `get_symbol_pins` | Inspection | `VERIFIED` |
| **get_net_connections** | `get_net_connections` | Netlist Inspection | `VERIFIED` |
| **list_unconnected_pins**| `list_unconnected_pins` | QA Inspection | `VERIFIED` |
| **run_erc** | `run_erc` | Electrical Rules Check | `VERIFIED (Smoke Test)` |
| **update_pcb_from_schematic**| `update_pcb_from_schematic` | Forward Annotation | `VERIFIED` |
| **run_drc** | `run_drc` | Design Rules Check | `VERIFIED` |

---

## 5. Quy Chuẩn Bắt Buộc Khi Thao Tác Với Tệp KiCad (KiCad File Mutation Policy)

> [!CAUTION]
> **QUY TẮC BẤT KHẢ XÂM PHẠM:**  
> Đối với tất cả các tệp có phần mở rộng:
> `*.kicad_sch`, `*.kicad_pcb`, `*.kicad_sym`, `*.kicad_mod`, `*.kicad_pro`, `*.kicad_prl`
>
> 1. **CẤM TUYỆT ĐỐI** sử dụng công cụ sửa văn bản thông thường (`write_to_file`, `replace_file_content`) để can thiệp trực tiếp cấu trúc cú pháp S-expression thô.
> 2. **BẮT BUỘC** thực hiện mọi thay đổi cấu trúc thiết kế thông qua các lệnh của **KiCad MCP Server**.
> 3. **Đọc tệp (Read-only)**: Chỉ cho phép đọc tệp khi cần tra cứu nhanh hoặc phân tích lỗi; không ghi đè lại bằng công cụ text.
> 4. **Cổng kiểm duyệt hợp lệ**:
>    - Sau khi hoàn thành schematic: Bắt buộc chạy `run_erc` (hoặc `kicad-cli sch erc`), đạt **0 Errors** mới được chuyển sang thiết kế PCB.
>    - Sau khi hoàn thành layout: Bắt buộc chạy `run_drc` (hoặc `kicad-cli pcb drc`), đạt **0 Errors** mới được xuất Gerber/đặt mạch.

---

## 6. Kết Quả Kiểm Thử Khói (Smoke Test Results)

Thực hiện kiểm thử trong thư mục tạm dùng một lần (disposable temp folder outside Air Mouse project): `C:\Users\phamt\AppData\Local\Temp\kicad_mcp_smoke_test`:

1. **Khởi tạo dự án**: `create_project(..., 'smoke_test')` $\rightarrow$ Tạo thành công `smoke_test.kicad_pro` và `smoke_test.kicad_sch`.
2. **Đặt linh kiện**:
   - `place_component('Device:R', 'R1', '10k', 100.0, 100.0)` $\rightarrow$ Đặt thành công R1 tại tọa độ lưới `(100.33, 100.33)`.
   - `place_component('Device:LED', 'D1', 'RED', 130.0, 100.0)` $\rightarrow$ Đặt thành công D1 tại tọa độ lưới `(129.54, 100.33)`.
3. **Nối dây**:
   - `connect_pins('R1', '2', 'D1', '2')` $\rightarrow$ Tự động tính toán đường dây và nối chân R1:2 với D1:2 qua 2 đoạn dây.
4. **Kiểm tra cấu trúc**:
   - `get_schematic_summary()` $\rightarrow$ Xác nhận chính xác 2 linh kiện, 2 dây nối.
   - `list_schematic_components()` $\rightarrow$ Đọc đúng danh sách tham chiếu `['R1', 'D1']`.
5. **Chạy kiểm tra ERC thực tế qua KiCad 9 CLI**:
   - `run_erc()` $\rightarrow$ Gọi trực tiếp `kicad-cli sch erc`, phát hiện chính xác phiên bản KiCad `9.0.7`, trả về 2 cảnh báo vi phạm chân chưa nối (`pin_not_connected` cho R1:1 và D1:1).
6. **Dọn dẹp môi trường**: Thư mục tạm đã được xóa hoàn toàn sau bài kiểm thử. Không gây ảnh hưởng tới cây thư mục của Air Mouse.

---

## 7. Yêu Cầu Về KiCad GUI / IPC API & Giới Hạn Đã Biết

- **Yêu cầu GUI KiCad**: **KHÔNG YÊU CẦU**. Người dùng không cần bật tùy chọn `Preferences -> Plugins -> KiCad API Server`, không cần mở giao diện KiCad khi AI thực hiện các thao tác MCP.
- **Giới hạn đã biết**:
  - Do KiCad được cài đặt tại `E:\kicad` (khác với đường dẫn mặc định `C:\Program Files\KiCad`), biến môi trường `KICAD_CLI_PATH` bắt buộc phải trỏ chính xác về `E:\kicad\bin\kicad-cli.exe`. Điểm này đã được xử lý triệt để trong `run_mcp.py` và cấu hình MCP.
  - Windows Controlled Folder Access: Các dự án đặt tại ổ `E:\` không bị giới hạn bảo vệ thư mục của Windows Defender; nếu làm việc trong thư mục `Documents`, cần cấp quyền ứng dụng trong Windows Security.
