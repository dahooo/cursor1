# 私有區塊鏈 (Private Blockchain)

一個用 Python 實作的簡單但功能完整的私有區塊鏈系統。

## 功能特色

- ✅ **區塊結構**: 完整的區塊數據結構，包含索引、交易、時間戳、哈希值等
- ✅ **工作量證明**: 實作 Proof of Work (PoW) 挖礦機制
- ✅ **交易系統**: 支援用戶間的代幣轉帳
- ✅ **餘額管理**: 自動計算和驗證用戶餘額
- ✅ **區塊鏈驗證**: 完整的區塊鏈完整性驗證
- ✅ **REST API**: 提供 HTTP API 介面
- ✅ **資料持久化**: 可將區塊鏈保存到 JSON 文件

## 專案結構

```
├── block.py          # 區塊類別
├── transaction.py    # 交易類別
├── blockchain.py     # 區塊鏈主要邏輯
├── api.py           # Flask REST API
├── demo.py          # 示例程式
├── requirements.txt  # Python 依賴
└── README.md        # 專案說明
```

## 安裝與設定

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 運行示例程式

```bash
python demo.py
```

這會創建一個示例區塊鏈，演示：
- 創建創世區塊
- 用戶間交易
- 挖礦過程
- 餘額計算
- 區塊鏈驗證

### 3. 啟動 API 服務器

```bash
python api.py
```

API 服務器將在 `http://localhost:5000` 啟動。

## API 使用說明

### 基本資訊

- **GET /** - 獲取 API 資訊和端點列表

### 區塊鏈操作

- **GET /blockchain** - 獲取完整區塊鏈
- **GET /blockchain/validate** - 驗證區塊鏈完整性
- **GET /stats** - 獲取區塊鏈統計資訊

### 交易操作

- **POST /transaction** - 創建新交易
  ```json
  {
    "from_address": "Alice_0x1234",
    "to_address": "Bob_0x5678",
    "amount": 100.0
  }
  ```

- **GET /pending** - 獲取待處理交易
- **POST /mine** - 挖掘待處理交易
  ```json
  {
    "mining_reward_address": "Miner_0x9abc"
  }
  ```

### 用戶操作

- **GET /balance/<address>** - 獲取地址餘額
- **GET /transactions/<address>** - 獲取地址交易歷史

### 資料管理

- **POST /save** - 保存區塊鏈到文件
  ```json
  {
    "filename": "my_blockchain.json"
  }
  ```

## API 使用範例

### 1. 創建交易

```bash
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "Alice_0x1234",
    "to_address": "Bob_0x5678",
    "amount": 50.0
  }'
```

### 2. 挖掘區塊

```bash
curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{
    "mining_reward_address": "Miner_0x9abc"
  }'
```

### 3. 查詢餘額

```bash
curl http://localhost:5000/balance/Alice_0x1234
```

### 4. 查看區塊鏈

```bash
curl http://localhost:5000/blockchain
```

## 核心概念

### 區塊結構

每個區塊包含：
- `index`: 區塊索引
- `transactions`: 交易列表
- `timestamp`: 時間戳
- `previous_hash`: 前一個區塊的哈希
- `nonce`: 工作量證明隨機數
- `hash`: 當前區塊哈希

### 工作量證明

使用簡單的 PoW 算法：
- 尋找使區塊哈希以指定數量的零開頭的 nonce 值
- 預設難度為 2（即哈希需要以 "00" 開頭）
- 難度可調整以控制挖礦時間

### 交易驗證

交易驗證包括：
- 金額必須大於 0
- 發送方和接收方地址不能為空
- 發送方不能是接收方
- 發送方必須有足夠餘額（系統交易除外）

## 安全特性

1. **哈希完整性**: 每個區塊都有唯一的哈希值
2. **鏈式連接**: 區塊通過哈希值連接，確保順序不可變
3. **工作量證明**: 防止惡意修改歷史區塊
4. **交易驗證**: 防止無效交易和雙重支付
5. **餘額檢查**: 自動驗證用戶餘額

## 限制與改進建議

### 當前限制

- 簡化的工作量證明算法
- 沒有數位簽名驗證
- 單一節點運行（非分散式）
- 基本的交易結構

### 可能的改進

1. **數位簽名**: 添加公私鑰對和交易簽名
2. **網路協議**: 實作節點間通信協議
3. **共識機制**: 添加更複雜的共識算法
4. **智能合約**: 支援可程式化交易
5. **資料庫**: 使用更高效的資料儲存方案

## 開發與測試

### 運行測試

```bash
python demo.py
```

### 自定義配置

可以調整以下參數：
- 挖礦難度（`difficulty`）
- 挖礦獎勵（`mining_reward`）
- API 端口（`port`）

### 除錯模式

API 服務器預設在除錯模式下運行，會顯示詳細的錯誤訊息。

## 授權

本專案為教育和學習目的而創建，歡迎自由使用和修改。

## 聯絡資訊

如有問題或建議，歡迎提出 Issue 或 Pull Request。

---

**注意**: 這是一個簡化的區塊鏈實作，僅用於學習和演示目的。在生產環境中使用前，需要添加更多的安全特性和優化。
