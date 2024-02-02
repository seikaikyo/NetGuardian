# NetGuardian 監控系統

NetGuardian 是一款專門為監控網路設備而設計的系統，它能夠實時追蹤設備的狀態並在異常發生時提供通知。

## 功能特點

- **持續監控**：實時追蹤網路中設備的存活狀態，確保系統運行無間斷。
- **郵件通知**：當設備狀態發生變化時，系統會自動發送郵件通知給管理員。
- **多收件人支持**：支持將郵件通知發送給多個收件人，確保關鍵訊息能夠及時傳達。
- **終端機狀態輸出**：在終端機中實時輸出監控狀態，提升監控的透明度和即時性。

## 安裝指南

跟隨以下步驟，您可以輕鬆地在您的系統上安裝並運行 NetGuardian 監控系統。

### 前提條件

在安裝之前，請確保您的系統滿足以下條件：

- Python 3.6 或更高版本。
- SQLite 3.25.0 或更高版本（用於支持窗口函數）。
- 必要的 Python 依賴包：`smtplib`, `email`, `sqlite3`。

### 安裝步驟

1. **克隆存儲庫**：首先，克隆 GitHub 存儲庫到您的本地系統：

    ```bash
    git clone https://github.com/seikaikyo/NetGuardian.git
    cd NetGuardian
    ```

2. **配置系統**：複製 `config.example.json` 為 `config.json` 並填入適當的配置值。

3. **啟動系統**：確保所有配置正確無誤後，運行以下命令以啟動監控系統：

    ```bash
    python scan.py
    ```

歡迎閱讀 [Wiki](https://github.com/seikaikyo/NetGuardian/wiki) 或 [FAQ](https://github.com/seikaikyo/NetGuardian/wiki/FAQ) 以獲得更多詳細資訊和使用指南。

## 貢獻

如果您對改進 NetGuardian 有任何建議或想要貢獻代碼，請隨時通過 Pull Request 或 Issues 與我們聯繫。我們非常歡迎任何形式的貢獻！

## 授權

本項目採用 MIT 授權協議。有關更多授權資訊，請參閱 [LICENSE](LICENSE) 文件。
