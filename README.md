# starsector-mod-JapaneseTranslation

これは [Starsector] で日本語を表示するための、翻訳テキスト Mod です。  
現在は、ごく僅かな文章のみ翻訳されています。

## 注意

- 訳文だけなので、別途日本語フォントが必要になります。
  - [starsector-mod-JapaneseFonts]

## ビルド

1. `Starsector` 本体にリンクをはります。
   - `make check` でチェック可能
2. `make setup`
   - POTファイルの生成
   - 旧版のPOファイルのマージ
3. 生成されたPOファイルを翻訳します。
   - *.edit.po が翻訳作業用ファイル
   - *.po はバージョン管理用ファイル
   - [Poedit] がおすすめ
4. `make build`
   - moファイルの生成
   - 訳文の反映
   - modの生成
5. `JapaneseTranslation-x.y.z.zip` が完成品です。

## ライセンス

[MIT License] としています。

---

[starsector]: https://fractalsoftworks.com/
[starsector-mod-JapaneseFonts]: https://github.com/hirmiura/starsector-mod-JapaneseFonts
[poedit]: https://poedit.net/
[MIT License]: https://opensource.org/license/mit/
