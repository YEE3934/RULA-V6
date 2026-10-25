# RULA v6：Pose + Hand 實驗版（延續 v5）

## 內含檔案
- `222.py`：可直接作為 Streamlit Cloud Main file 的完整程式。
- `requirements.txt`：沿用 v5 的套件版本，`mediapipe==0.10.21` 同時支援 Hand Tasks API。
- `scripts/download_hand_model.py`：可在本機下載官方 Hand Landmarker 模型。
- `models/README.txt`：模型放置方式與來源。

## 建議使用方式

請**另建一個 GitHub 儲存庫／Streamlit Cloud 實驗網站**，不要覆蓋 v5 正式版。

1. 將壓縮檔內容解壓縮（保留 `models/` 和 `scripts/` 子目錄）。
2. 在電腦可連網的情況下，執行 `python scripts/download_hand_model.py`，會產生 `models/hand_landmarker.task`。
3. 把 `222.py`、`requirements.txt`、`models/hand_landmarker.task` 上傳新 GitHub 儲存庫，主檔設定為 `222.py`。
4. Streamlit Cloud 選擇 Python 3.11，等待部署完成。
5. 上傳正面＋側面影片，選擇 Hand 功能（預設勾選），並保留**安全比較模式**。
6. 分析後在「手腕演算法比較實驗中心」查看影格、角度、圖片與推論耗時。

不想自行下載模型也可以：程式會在**第一次分析**時，嘗試從官方來源下載到 `/tmp/rula_hand_assets/hand_landmarker.task`。唯讀的 `site-packages` **不會**被寫入；如網站無法連線，會警告並退回 Pose 模式。

## 重要設計
- **預設安全模式**：只做 Pose/Hand 角度比較，不改動 v5 RULA 評分。
- **實驗計分模式（須使用者選取）**：匹配目標手腕、Hand/Pose 角度差不超過 35°、腕點距離與前臂長度比不超過 0.32，才會把 Hand 2D 代理角度作為 RULA 手腕屈伸基礎角度，其他情況保留 Pose。
- 同一張圖的 Pose 肘部與 Hand 腕／掌指點做**影像 2D 座標**角度比較。
- Hand World 只輸出手掌**局部**幾何（掌心方向長度、掌指張角）；**沒有**和 Pose World 的 3D 點相減，**沒有**宣稱量得前臂旋前旋後。
- 匯出 ZIP 包含 `Hand_Comparison/Comparison_Data.csv` 以及每張的 `Pose` / `PoseHand` 影像對照。原本 RULA CSV、異常影格審核、逐影格重算、時間軸功能保留。
- 分析畫面可比較 `Pose 側面偵測耗時(ms)` 與 `Hand 偵測耗時(ms)`；兩者的測量範圍不同，不代表完整網站前後總耗時可直接相減。
- **資料仍須研究驗證**：Hand 匹配成功率、模型間一致性並非量測準確率。保持與 v5 輸出對照，不要將模型輸出當作真值。

## 本機安裝

```bash
python -m pip install -r requirements.txt
python scripts/download_hand_model.py
streamlit run 222.py
```

## 依賴與模型
Google 官方文件：https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python
模型檔：https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

## 若 Hand 偵測不到
先確認模型檔、拍攝距離、手是否被物品遮住、畫面解析度及鏡頭是否接近側面。Hand 模型未必能改善第 9 筆等遮擋嚴重的樣本；仍以樣本比較與後續小規模參考測量為準。

## 尚未測試範圍
程式已做語法檢查與模擬單元測試，但環境未提供 Mediapipe、Streamlit 和可下載的 `.task` 二進位模型，因此沒有完成真正 Streamlit Cloud／實際影片端到端驗證。
