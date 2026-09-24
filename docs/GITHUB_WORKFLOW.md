# Quy Trình Git & GitHub Chuẩn Doanh Nghiệp — FoodSafe-DX-OS

> **Tài liệu quy chuẩn quản lý mã nguồn và vòng đời phát triển tính năng (SDLC)**  
> **Người ban hành:** Tech Lead  
> **Phạm vi áp dụng:** Toàn bộ thành viên tham gia phát triển dự án FoodSafe-DX-OS

---

## 1. Nguyên Tắc Cốt Lõi (Core Principles)

1. **Tuyệt đối không commit/code trực tiếp trên nhánh `main`**. Nhánh `main` là nhánh production-ready, chỉ nhận code thông qua Pull Request đã qua Review và CI/CD.
2. **Mỗi task tương ứng một branch độc lập**. Không gộp nhiều đầu việc khác nhau vào cùng một nhánh.
3. **Phân loại nhánh chuẩn xác theo domain công việc**.
4. **Commit atomic, rõ ràng và tuân thủ Conventional Commits**.
5. **Không merge khi chưa qua kiểm thử (Test / CI) và chưa được Review phê duyệt**.
6. **Không tự ý sửa code ngoài phạm vi task**. Nếu phát hiện lỗi khác ngoài task, tạo ticket/issue mới.
7. **Task lớn phải được phân rã thành các task/branch nhỏ hơn** (Incremental Development).
8. **Trước khi tạo branch mới, bắt buộc phải cập nhật mã nguồn mới nhất từ `main`**.

---

## 2. Quy Chuẩn Đặt Tên Branch (Branch Naming Convention)

Mọi nhánh công việc phải tuân theo cấu trúc tiền tố xác định tính chất công việc:

| Loại công việc | Cấu trúc nhánh | Ví dụ |
|---|---|---|
| **UI / Giao diện** | `ui/ten-task` | `ui/design-tokens-base-setup`, `ui/stepper-inspection-flow` |
| **Feature mới** | `feat/ten-task` | `feat/poka-yoke-core-temp`, `feat/export-pdf-audit-report` |
| **Bug fix** | `fix/ten-task` | `fix/locker-countdown-timezone`, `fix/bfs-cycle-detection` |
| **Refactor** | `refactor/ten-task` | `refactor/normalize-inspection-dto`, `refactor/cleanup-css` |
| **Database** | `db/ten-task` | `db/add-facility-indexes`, `db/migration-sample-retention` |
| **API / Backend** | `backend/ten-task` | `backend/audit-log-endpoints`, `backend/healthcheck-probe` |
| **AI / Agent** | `ai/ten-task` | `ai/offline-rag-vector-store`, `ai/agentic-trace-tool` |
| **Documentation** | `docs/ten-task` | `docs/github-workflow-standard`, `docs/api-specification` |
| **Hotfix production** | `hotfix/ten-task` | `hotfix/cors-preflight-cache`, `hotfix/db-pool-exhaustion` |
| **Test** | `test/ten-task` | `test/graph-tracer-edge-cases`, `test/poka-yoke-integration` |

### Quy tắc định dạng tên:
- Viết bằng chữ thường (kebab-case), phân cách các từ bằng dấu gạch ngang `-`.
- Không sử dụng ký tự đặc biệt, dấu cách, hoặc tiếng Việt có dấu trong tên nhánh.
- Tên ngắn gọn, súc tích, phản ánh chính xác mục tiêu của task.

---

## 3. Quy Chuẩn Commit Message (Conventional Commits)

Format chuẩn:
```text
<type>(<scope>): <mô tả ngắn gọn về thay đổi>

[Tùy chọn: Mô tả chi tiết lý do và ngữ cảnh thay đổi]
[Tùy chọn: Refs / Closes #IssueID]
```

### Các types hợp lệ:
- `ui`: Thay đổi giao diện, CSS, HTML, tokens, tương tác người dùng.
- `feat`: Tính năng mới cho người dùng hoặc hệ thống.
- `fix`: Sửa lỗi phát sinh.
- `refactor`: Tái cấu trúc mã nguồn không làm thay đổi hành vi nghiệp vụ.
- `perf`: Cải thiện hiệu năng.
- `test`: Bổ sung hoặc chỉnh sửa test suite.
- `docs`: Cập nhật tài liệu, README, hướng dẫn kỹ thuật.
- `chore`: Tác vụ bảo trì, cấu hình build, dependency.
- `ci`: Thay đổi cấu hình CI/CD pipeline, GitHub Actions.

*Ví dụ commit hợp lệ:*
- `ui(theme): configure design tokens, typography font stack and base styles`
- `feat(poka-yoke): enforce minimum 70C core temperature for cooked poultry`
- `fix(locker): prevent unlock attempt before 24-hour expiration window`
- `docs(workflow): establish standard enterprise github branching and pr process`

---

## 4. Vòng Đời Task Chuẩn (Task Lifecycle Step-by-Step)

```text
[Issue / Task Được Giao]
         │
         ▼
[1. Đồng bộ `main` mới nhất]  ──► git checkout main && git pull origin main
         │
         ▼
[2. Tạo branch theo chuẩn]     ──► git checkout -b <type>/<ten-task>
         │
         ▼
[3. Thực hiện code trong phạm vi]
         │
         ▼
[4. Kiểm thử cục bộ (Test/Lint)] ──► Chạy pytest, kiểm tra docker service, build frontend
         │
         ▼
[5. Commit chuẩn convention]   ──► git commit -m "<type>(<scope>): <message>"
         │
         ▼
[6. Push nhánh lên origin]     ──► git push -u origin <type>/<ten-task>
         │
         ▼
[7. Tạo Pull Request (PR)]     ──► Điền đầy đủ PR template (Context, Changes, Checklist)
         │
         ▼
[8. Review & QA Testing]       ──► Đồng nghiệp / Tech Lead duyệt diff & checklist
         │
         ▼
[9. Approve & Merge vào `main`] ──► Merge commit sạch sẽ (no-ff / squash)
         │
         ▼
[10. Xóa branch sau khi merge] ──► git branch -d <branch> && git push origin --delete <branch>
```

---

## 5. Tiêu Chuẩn Nghiệm Thu PR (Definition of Done - DoD)

Một Pull Request chỉ được chấp thuận (Approved & Merged) khi thỏa mãn:
1. **Scope Integrity**: Chỉ chứa các commit phục vụ đúng mục tiêu của task; không phát sinh thay đổi lạc đề.
2. **Automated Verification**: Toàn bộ unit test và integration test (`docker compose exec backend pytest`) chạy thành công 100%.
3. **No Regressions**: Các API hiện có và giao diện hiện hành không bị vỡ hoặc mất kết nối.
4. **Code Quality**: Code rõ ràng, đặt tên biến có nghĩa, không để lại console debug thừa hay comment rác.
5. **Documentation**: Nếu thay đổi API hoặc luồng dữ liệu, tài liệu tương ứng phải được cập nhật.

---
*FoodSafe-DX-OS Engineering Team — Zero Cloud, 100% Deterministic & Enterprise Standard.*
