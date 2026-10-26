# MacroScope 🌏

[中文](#中文) · [日本語](#日本語) · [English](#english)

## 中文

MacroScope 是一个中美日宏观经济数据可视化与统计分析应用。项目整合官方公开数据，提供指标趋势、跨国比较、描述统计与双序列相关性分析，支持中文、日文和英文界面。

### 功能

- **首页**：对比中国、美国、日本的年度 GDP 总量、实际 GDP 增速、CPI 年度通胀、货物和服务出口额、进口额与贸易差额。
- **美国经济专区**：查看非农就业月度变动、初请失业金人数及四周均值、CPI 同比/环比、GDP 总量/实际增速、有效联邦基金利率及 2 年/10 年国债收益率。
- **独立相关性分析**：分别选择两组数据的来源、国家与指标，支持跨国家和跨数据源比较，提供 Pearson、Spearman、散点图、共同样本数与配对数据下载。
- **描述统计**：按序列提供有效样本数、源中空值数、均值、中位数、样本标准差、分位数、极值和有效观测起止日期。
- **指标解释**：提供定义、阅读方法、市场影响机制、常见误区与参考资料。
- **时间与导出**：默认截至最新有效观测的最近 5 年；年度图展示最近 5 个观测年份。可自定义日期并下载原始数据、统计结果和相关性配对 CSV。

### 数据来源与覆盖

首页使用免密钥的[世界银行 WDI API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)；美国专区使用 [FRED API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)，需要自己的 `FRED_API_KEY`。

中国、日本月度 CPI、政策/基准利率、2 年与 10 年国债收益率，以及月度海关商品贸易数据尚未接入。未接入或请求失败时明确提示，不展示模拟数据。项目不包含股票指数或行情功能。

### 统计口径与限制

- 图表保留原始单位、频率及来源。年度观测标为当年 1 月 1 日，不是发布日期；美国季度 GDP 年率与世界银行年度 GDP 不可直接视为同口径。
- 描述统计排除空值，标准差采用 `ddof=1`；不足 2 个有效样本时标准差留空。空值不填零，缺失数不包括数据源未返回的日期。
- 相关性默认使用相邻期差值，也支持原始水平值。按较低频率的日历期取有效值算术平均，不插值或前向填充；先差分再保留共同有效观测。
- 期内均值不代表复合通胀率或新的 GDP 增长率，边界时期可能不完整。至少 3 组、双方非恒定才计算系数；少于 12 组提示小样本风险。
- 相关性不代表因果或预测能力；不提供显著性检验或交易信号。历史数据可能修订，不支持历史版本回测。市场机制说明不构成针对当前公布值的事件归因。

### 运行与配置

依赖 Python 3.11 或 3.12，技术栈为 Streamlit、Pandas、NumPy、Plotly、Requests 与 python-dotenv。安装命令见下方[运行命令](#运行命令--実行コマンド--commands)。

本地将 `.env.example` 复制为 `.env` 并填写自己的 FRED 密钥；也支持环境变量和 Streamlit Secrets。没有密钥仍可使用世界银行数据。世界银行缓存 24 小时，FRED 缓存 1 小时；网络失败会显示提示。

仓库部署入口为 `MacroScope/app.py`，依赖文件为 `requirements.txt`。Streamlit Community Cloud 的 Secrets 使用 `FRED_API_KEY = "your-own-key"`；不要提交 `.env` 或 `.streamlit/secrets.toml`。

源代码采用 MIT 许可证。第三方数据遵循各自条款，MIT 不授予第三方数据再分发权。数据页面及参考资料保留原始出处。

## 日本語

MacroScope は、中国・米国・日本のマクロ経済データを可視化し、統計分析するアプリケーションです。公式の公開データを統合し、時系列の推移、国際比較、記述統計、2系列の相関分析を提供します。日本語・中国語・英語の画面に対応しています。

### 機能

- **ホーム**：日米中の年間 GDP 総額、実質 GDP 成長率、年間 CPI インフレ率、財・サービス輸出入額、貿易収支を比較します。
- **米国経済**：非農業部門雇用者数の前月差、新規失業保険申請件数と4週移動平均、CPI 前年同月比・前月比、GDP 総額・実質成長率、実効 FF 金利、米国債2年・10年利回りを表示します。
- **独立した相関分析**：2つのデータ源・国・指標を個別に選択し、国やデータ源をまたいで比較できます。Pearson・Spearman 係数、散布図、共通標本数、配対 CSV を提供します。
- **記述統計**：系列別の有効観測数、データ源の空値数、平均、中央値、標本標準偏差、分位数、極値、有効観測期間を表示します。
- **指標説明**：定義、読み方、市場への影響経路、誤解しやすい点、参考資料を掲載します。
- **期間と出力**：初期表示は最新の有効観測までの直近5年間です。年次指標は直近5つの観測年を表示します。期間指定、元データ・統計結果・配対 CSV のダウンロードに対応します。

### データ源と対応範囲

ホームはキー不要の[世界銀行 WDI API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)、米国経済は独自の `FRED_API_KEY` が必要な [FRED API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)を使用します。

中国・日本の月次 CPI、政策・基準金利、国債2年・10年利回り、税関の月次商品貿易データは未接続です。未接続や取得失敗は明示し、模擬データで代用しません。株価指数や相場取得機能は含みません。

### 統計の定義と制約

- 元の単位・頻度・出所を保持します。年次値の日付は1月1日で、公表日ではありません。米国四半期 GDP の年率値と世界銀行の年次 GDP は同一の定義ではありません。
- 記述統計は空値を除き、標本標準偏差は `ddof=1` とします。有効値が2件未満なら標準偏差は空欄です。欠損をゼロにせず、欠損数に応答にない日付は含めません。
- 相関分析の初期設定は前期差で、水準値も選べます。低い方の頻度の暦期間で有効値の算術平均を取り、補間・前方補完をせず、差分の計算後に共通の有効観測を抽出します。
- 期間内平均は複利のインフレ率や新たな GDP 成長率ではなく、境界期間は不完全な場合があります。3組以上かつ両系列に変動がある場合に係数を計算し、12組未満では注意を表示します。
- 相関は因果関係や予測能力を意味せず、有意性検定や売買シグナルは提供しません。過去の値は改定され得ます。公表時点の履歴によるバックテストには未対応です。市場の仕組みの説明は個別の公表値に関する因果分析ではありません。

### 実行と設定

Python 3.11 または 3.12 を使用します。主な依存関係は Streamlit、Pandas、NumPy、Plotly、Requests、python-dotenv です。実行コマンドは下部に掲載しています。

`.env.example` を `.env` にコピーし、ご自身の FRED キーを設定してください。環境変数と Streamlit Secrets にも対応します。キーなしでも世界銀行データを利用できます。キャッシュは世界銀行24時間、FRED 1時間で、接続失敗時はメッセージを表示します。

デプロイのエントリーポイントは `MacroScope/app.py`、依存関係は `requirements.txt` です。Streamlit Community Cloud の Secrets に `FRED_API_KEY = "your-own-key"` を設定し、`.env` や `.streamlit/secrets.toml` はコミットしないでください。

ソースコードは MIT ライセンスです。第三者データは各提供元の条件に従い、MIT によって再配布権が付与されるものではありません。元の出所をデータ画面と参考資料に記載します。

## English

MacroScope is a macroeconomic visualization and statistical analysis application covering China, the United States and Japan. It combines official public data with time-series charts, cross-country comparisons, descriptive statistics and two-series correlation analysis. The interface supports English, Chinese and Japanese.

### Features

- **Home**: compare annual GDP levels, real GDP growth, CPI inflation, goods and services exports, imports and trade balances across the three countries.
- **US Economy**: explore monthly nonfarm payroll changes, initial unemployment claims and their four-week average, CPI YoY/MoM, GDP levels and real growth, the effective federal funds rate, and 2-year/10-year Treasury yields.
- **Independent correlation analysis**: select two sources, countries and indicators independently, including cross-country and cross-source comparisons. View Pearson and Spearman coefficients, scatterplots, paired sample counts and paired CSV exports.
- **Descriptive statistics**: view valid and source-null counts, mean, median, sample standard deviation, quantiles, extrema and valid observation dates for each series.
- **Indicator descriptions**: definitions, interpretation, possible market transmission channels, common pitfalls and references.
- **Time windows and exports**: default to five years ending at the latest valid observation, or the latest five observation years for annual series. Custom dates and CSV exports of source observations, statistics and pairs are available.

### Data sources and coverage

Home uses the keyless [World Bank WDI API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures). US Economy uses the [FRED API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), which requires your own `FRED_API_KEY`.

Monthly CPI, policy/benchmark rates and 2-year/10-year government yields for China and Japan, and monthly customs merchandise trade data, are not connected. Unavailable data and failed requests are explicitly identified; simulated values are never substituted. Stock indices and market price feeds are not included.

### Statistical definitions and limitations

- Original units, frequencies and sources are retained. Annual observations are dated January 1, not their release date. US quarterly GDP at an annual rate is not the same definition as World Bank annual GDP.
- Descriptive statistics exclude nulls and use sample standard deviation with `ddof=1`, left blank with fewer than two valid observations. Missing values are not zero; dates absent from a source response are not included in the null count.
- Correlation defaults to period-to-period differences; original levels are optional. Series are aligned to the coarser calendar frequency using arithmetic means of valid observations. No interpolation or forward filling is performed; differences are calculated before complete pairs are retained.
- Period means are not compounded inflation or newly calculated GDP growth, and boundary periods may be incomplete. Coefficients require at least three pairs and variation in both series; fewer than 12 pairs trigger a small-sample notice.
- Correlation is not causation or predictive power. No significance tests or trading signals are generated. Historical data may be revised; vintage-based backtesting is not supported. Market transmission descriptions are not event-specific causal attributions.

### Runtime and configuration

Use Python 3.11 or 3.12. The stack includes Streamlit, Pandas, NumPy, Plotly, Requests and python-dotenv. Commands are provided below.

Copy `.env.example` to `.env` and set your own FRED key. Environment variables and Streamlit Secrets are also supported. World Bank data work without a key. Cache lifetimes are 24 hours for World Bank and one hour for FRED; connection failures display a message.

Deploy with `MacroScope/app.py` as the entrypoint and `requirements.txt` as the dependency file. On Streamlit Community Cloud, set `FRED_API_KEY = "your-own-key"` in Secrets. Do not commit `.env` or `.streamlit/secrets.toml`.

Source code is licensed under MIT. Third-party data remain subject to their providers' terms; MIT does not grant redistribution rights to those data. Source attribution is retained in the app and references.

## 运行命令 / 実行コマンド / Commands

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m streamlit run app.py
```

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m streamlit run app.py
```

测试 / テスト / Tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

测试命令需使用虚拟环境中的解释器。 / テストには仮想環境のインタープリターを使用してください。 / Run test commands with the virtual environment's interpreter.

本地地址 / ローカルURL / Local URL: `http://localhost:8501`

## 项目结构 / 構成 / Structure

```text
MacroScope/
├── app.py
├── pages/
│   ├── 1_US_Economy.py
│   └── 2_Correlation.py
├── macroscope/
│   ├── catalog.py
│   ├── data.py
│   ├── ui.py
│   ├── analysis.py
│   ├── analysis_ui.py
│   ├── periods.py
│   ├── explanations.py
│   ├── help_translations.py
│   ├── i18n.py
│   └── statistics_translations.py
├── tests/
├── .github/workflows/tests.yml
├── .streamlit/config.toml
├── .env.example
├── requirements.txt
├── requirements-dev.txt
└── LICENSE
```
