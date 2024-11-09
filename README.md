# tobii-gaze-2-vid

視線追跡データの録画から動画作成までを自動化する統合パイプライン
Integrated pipeline for Tobii eye-tracking: Automates gaze data recording, processing, and visualization from capture to final video creation.

## ファイル構成

```
tobii-gaze-2-vid/
├── gaze_recorder.py
├── gaze_interpolation.py
├── video_integration.py
├── main.py
├── utils.py
└── README.md
```

## ファイルの説明

- `gaze_recorder.py`: Tobiiデバイスを使用して視線データを記録
- `gaze_interpolation.py`: 記録された視線データの補完処理
- `video_integration.py`: 視線データと動画の統合
- `main.py`: プログラムのエントリーポイント。全体の処理を制御
- `utils.py`: 共通のユーティリティ関数
- `README.md`: プロジェクトの説明と使用方法

## 使用方法

```bash
python main.py [オプション]
```

詳細なオプションと使用例は後日追加予定