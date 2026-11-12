# GitHub公開チェックリスト

## 公開前

- [ ] 社名・著作者表記を必要に応じて追加
- [ ] APIキー、パスワード、秘密鍵が含まれていない
- [ ] 社内URL、顧客情報、個人情報が含まれていない
- [ ] HEF / PT / ONNX をコミットしていない
- [ ] `venv_hailo_apps` をコミットしていない
- [ ] Hailo Apps本体をコピーしていない
- [ ] 撮影画像・動画をコミットしていない
- [ ] 学習データの権利を確認
- [ ] 使用モデルのライセンスを確認
- [ ] READMEの動作環境を実機で確認

## Git確認

```bash
git status
git ls-files
```

大容量ファイル確認:

```bash
find . -type f -size +10M -print
```

秘密情報の簡易確認:

```bash
grep -RniE 'password|secret|token|api[_-]?key' . \
  --exclude-dir=.git
```

## 公開後

- [ ] GitHub上でLICENSEがAGPL-3.0として認識されることを確認
- [ ] README表示を確認
- [ ] 新規cloneから手順を再現できることを確認
- [ ] Releaseに第三者モデルやバイナリを添付していないことを確認
