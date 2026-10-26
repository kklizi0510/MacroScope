# 验证记录 / 検証記録 / Validation

2026-10-27（Asia/Tokyo）

## 中文

- 32 项离线测试通过，覆盖数据解析、缺失值、指标计算、最近五年窗口、描述统计、频率对齐、相关系数、三语切换和独立相关性页面。
- 已通过真实请求验证 FRED 美国专区全部 10 个指标（2023—2024 区间）；世界银行已验证中国实际 GDP 增速、日本实际 GDP 增速、年度 CPI 通胀、出口、进口及差额。其他世界银行请求曾遇到连接失败，不能据此宣称全部在线验证完成。
- 本机 Streamlit 服务已启动并通过健康检查；尚未发布公网应用或 GitHub 远程仓库。
- 测试数字仅为离线夹具，不用于页面或失败兜底。密钥仅存于被 Git 忽略的本地配置，分发包不包含密钥。

## 日本語

- データ解析、欠損値、指標計算、直近5年、記述統計、頻度整合、相関係数、3言語切替、独立相関ページを含む32件のオフラインテストが通過しました。
- FRED米国10指標は2023～2024年の実リクエストで検証済みです。世界銀行は中国の実質GDP成長率、日本の実質GDP成長率、年間CPIインフレ率、輸出、輸入、収支を検証しました。他の世界銀行リクエストには接続失敗があり、全系列のオンライン検証完了とはしていません。
- ローカルStreamlitの起動とヘルスチェックは確認済みです。公開アプリやGitHubのリモートリポジトリは未作成です。
- テスト値はオフラインの検証用で、画面や取得失敗時の代替値には使用しません。キーはGit対象外のローカル設定のみで、配布パッケージには含みません。

## English

- All 32 offline tests pass, covering parsing, missing data, indicator calculations, trailing five-year windows, descriptive statistics, frequency alignment, correlations, three-language switching and the independent correlation page.
- All 10 FRED US indicators were verified with real requests for 2023–2024. World Bank verification succeeded for China's real GDP growth and Japan's real GDP growth, annual CPI inflation, exports, imports and balance. Other World Bank requests encountered connection failures; full online verification is not claimed.
- The local Streamlit service and health endpoint were verified. No public deployment or GitHub remote repository has been created.
- Test figures are offline fixtures, never displayed or used as fallbacks. The key exists only in ignored local configuration and is excluded from the distribution package.
