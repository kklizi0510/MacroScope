"""Presentation translations; original catalog keys remain stable for calculations."""
import streamlit as st

LANGUAGES = {"zh": "中文", "ja": "日本語", "en": "English"}
TEXT = {}


def add(zh, en, ja):
    TEXT[zh] = {"zh": zh, "en": en, "ja": ja}


# Centralized interface and metadata translations.
ROWS = [
    ("首页", "Home", "ホーム"),
    ("美国经济专区", "US Economy", "米国経済"),
    ("中美日宏观经济数据看板", "China, US and Japan · Macroeconomic dashboard", "日米中のマクロ経済ダッシュボード"),
    ("追踪中美日宏观经济指标并比较长期趋势。年度数据通常滞后；数据接入情况见页面底部，美国高频数据请查看美国经济专区。", "Track macroeconomic indicators across China, the US and Japan and compare long-term trends. Annual data usually lag; see coverage below and visit US Economy for higher-frequency US data.", "日米中のマクロ経済指標と長期トレンドを比較します。年次データには公表の遅れがあります。対応状況は下部、米国の高頻度データは米国経済ページをご覧ください。"),
    ("时间范围", "Time range", "表示期間"),
    ("最近5年（截至最新数据）", "Latest five years (through latest data)", "最新データまでの直近5年間"),
    ("自定义日期", "Custom dates", "期間を指定"),
    ("每张图以所选序列的最新有效观测为终点，展示最近5年；年度指标展示最近5个观测年份。", "Each chart ends at the latest valid observation across its selected series and shows the preceding five years. Annual indicators show the latest five observation years.", "各グラフは選択系列の最新の有効観測を終点に直近5年間を表示します。年次指標は直近5つの観測年を表示します。"),
    ("开始日期", "Start date", "開始日"), ("结束日期", "End date", "終了日"),
    ("开始日期不能晚于结束日期。", "Start date must not be after end date.", "開始日は終了日以前に設定してください。"),
    ("国家", "Countries", "国"),
    ("中国", "China", "中国"), ("美国", "United States", "米国"), ("日本", "Japan", "日本"),
    ("指标（不同单位分别绘图）", "Indicators (separate charts for different units)", "指標（単位ごとに別のグラフで表示）"),
    ("年度序列按观测年份筛选，日期统一标为当年 1 月 1 日。跨国使用同一世界银行指标；不把年度数据扩展成月度数据。", "Annual series are filtered by observation year and dated January 1. Countries use the same World Bank indicator; annual data are not expanded into monthly data.", "年次系列は観測年で絞り込み、日付をその年の1月1日とします。各国で同じ世界銀行指標を使用し、年次値を月次値には変換しません。"),
    ("GDP 总量", "GDP level", "GDP総額"), ("GDP 实际增速", "Real GDP growth", "実質GDP成長率"),
    ("CPI 年度通胀", "Annual CPI inflation", "CPI年間インフレ率"),
    ("出口额", "Exports", "輸出額"), ("进口额", "Imports", "輸入額"), ("贸易差额", "Trade balance", "貿易収支"),
    ("非农就业月度变动", "Monthly change in nonfarm payrolls", "非農業部門雇用者数の前月差"),
    ("初请失业金人数", "Initial unemployment claims", "新規失業保険申請件数"),
    ("初请四周均值", "Initial claims: four-week average", "新規失業保険申請件数・4週移動平均"),
    ("CPI 同比", "CPI year-over-year", "CPI前年同月比"), ("CPI 环比", "CPI month-over-month", "CPI前月比"),
    ("联邦基金有效利率", "Effective federal funds rate", "実効フェデラルファンド金利"),
    ("2 年国债收益率", "2-year Treasury yield", "米国債2年利回り"),
    ("10 年国债收益率", "10-year Treasury yield", "米国債10年利回り"),
    ("年度", "Annual", "年次"), ("季度", "Quarterly", "四半期"), ("月度", "Monthly", "月次"), ("周度", "Weekly", "週次"), ("日度", "Daily", "日次"),
    ("美元（现价）", "Current US dollars", "米ドル（名目）"), ("千人", "Thousands of persons", "千人"), ("人", "Persons", "人"),
    ("十亿美元（现价，年率）", "Billions of current USD, annual rate", "10億米ドル（名目・年率）"),
    ("%（环比折年率）", "% (quarter-on-quarter, annualized)", "%（前期比年率）"),
    ("读取{country}数据…", "Loading data for {country}…", "{country}のデータを取得中…"),
    ("所选年份没有可用数据。", "No observations available for the selected years.", "選択した年に利用可能な観測値がありません。"),
    ("来源：", "Source: ", "出所："),
    ("来源：[世界银行 WDI](https://data.worldbank.org/)；贸易差额由出口减进口计算。", "Source: [World Bank WDI](https://data.worldbank.org/). Trade balance is calculated as exports minus imports.", "出所：[世界銀行 WDI](https://data.worldbank.org/)。貿易収支は輸出額から輸入額を差し引いて計算します。"),
    ("MVP 数据接入清单与边界", "MVP data coverage and limitations", "MVPのデータ対応状況と制約"),
    ("清除缓存并重新读取", "Clear cache and reload", "キャッシュを消去して再取得"),
    ("所选区间没有可用观测值。未填充或模拟数据。", "No observations available in this period. No values have been filled or simulated.", "選択期間に利用可能な観測値がありません。補完値や模擬データは使用しません。"),
    ("有 {missing} 条观测缺失；图中保留缺口，未前向填充。", "{missing} observations are missing. Gaps are retained; no forward filling.", "観測値が{missing}件欠損しています。グラフに欠損を残し、前方補完は行いません。"),
    ("有效观测范围：{start} — {end}。观测日期不是发布日期；可能存在发布滞后和修订。", "Available observations: {start} — {end}. Observation dates are not release dates; publication lags and revisions may apply.", "有効な観測期間：{start} — {end}。観測日は公表日ではありません。公表の遅れや改定があります。"),
    ("观测期", "Observation period", "観測期間"), ("序列", "Series", "系列"),
    ("下载当前数据 CSV", "Download current data as CSV", "表示データをCSVでダウンロード"),
    ("是什么", "What it measures", "何を表す指標か"),
    ("如何阅读 · 对投资市场的可能影响", "How to read it · Possible market effects", "読み方・投資市場への影響"),
    ("如何阅读", "How to read it", "読み方"),
    ("可能影响市场的路径（机制解读）", "Possible market transmission channels", "市場に影響する経路（仕組みの解説）"),
    ("容易误解的地方", "Common pitfalls", "誤解しやすい点"),
    ("参考资料：", "References: ", "参考資料："),
    ("月度、周度、季度和日度序列分别展示，保留各自频率与定义。", "Monthly, weekly, quarterly and daily series are shown separately, preserving their frequency and definition.", "月次・週次・四半期・日次の系列を、それぞれの頻度と定義を保って個別に表示します。"),
    ("选择美国指标", "Select US indicators", "米国の指標を選択"),
    ("配置 FRED_API_KEY 后可读取美国专区数据；无密钥时仍可使用首页世界银行数据。", "Configure FRED_API_KEY to load US data. World Bank data on the home page work without a key.", "米国データの取得にはFRED_API_KEYを設定してください。ホームの世界銀行データはキーなしで利用できます。"),
    ("读取官方数据…", "Loading official data…", "公式データを取得中…"),
    ("数据请求失败。请检查网络、服务状态或 FRED 密钥，稍后重试。", "Request failed. Check your connection, service availability or FRED key, then try again.", "取得に失敗しました。ネットワーク、サービスの稼働状況、FREDキーを確認し、後でもう一度お試しください。"),
    ("世界银行返回格式异常。", "Unexpected World Bank response format.", "世界銀行の応答形式が想定と異なります。"),
    ("世界银行数据字段异常。", "Unexpected World Bank data fields.", "世界銀行のデータ項目が想定と異なります。"),
    ("尚未配置 FRED_API_KEY。请按 README 设置自己的密钥。", "FRED_API_KEY is not configured. Follow the README to set your own key.", "FRED_API_KEYが未設定です。READMEに従ってご自身のキーを設定してください。"),
    ("FRED 返回格式异常，无法读取观测值。", "Unexpected FRED response; unable to read observations.", "FREDの応答形式が想定と異なり、観測値を読み込めません。"),
    ("名义 GDP；受汇率影响，不代表实际产出增速。", "Nominal GDP; exchange rates affect it. This is not real output growth.", "名目GDP。為替の影響を受け、実質産出の成長率ではありません。"),
    ("不变价 GDP 年增长率。", "Annual GDP growth at constant prices.", "固定価格GDPの年間成長率。"),
    ("年度 CPI 通胀；不是某个月的同比或环比。", "Annual CPI inflation, not a particular month's year-on-year or month-on-month rate.", "年間CPIインフレ率。特定月の前年同月比や前月比ではありません。"),
    ("货物和服务出口，国民账户口径。", "Exports of goods and services, national accounts basis.", "国民経済計算ベースの財・サービス輸出。"),
    ("货物和服务进口，国民账户口径。", "Imports of goods and services, national accounts basis.", "国民経済計算ベースの財・サービス輸入。"),
    ("同年货物和服务出口减进口；不是海关月度商品贸易帐。", "Same-year goods and services exports minus imports; not monthly customs merchandise trade.", "同年の財・サービス輸出から輸入を控除。税関の月次商品貿易収支とは異なります。"),
    ("BLS，季调非农就业总量的一阶差分；包含历史修订。", "BLS: first difference of seasonally adjusted nonfarm payrolls; includes historical revisions.", "BLSの季節調整済み非農業部門雇用者数の前月差。過去の改定を含みます。"),
    ("美国劳工部，季调；日期为周结束日。", "US Department of Labor, seasonally adjusted; dated at week end.", "米労働省、季節調整済み。日付は週末日です。"),
    ("美国劳工部发布的季调四周移动平均。", "Official seasonally adjusted four-week moving average from the US Department of Labor.", "米労働省公表の季節調整済み4週移動平均。"),
    ("BLS，季调 CPI 指数计算的 12 个月变化；与非季调官方同比可能不同。", "BLS: 12-month change calculated from seasonally adjusted CPI; may differ from the official unadjusted year-on-year rate.", "BLSの季節調整済みCPIから算出した12か月変化率。非季調の公式前年同月比とは異なる場合があります。"),
    ("BLS，季调 CPI 指数计算的 1 个月变化。", "BLS: one-month change calculated from seasonally adjusted CPI.", "BLSの季節調整済みCPIから算出した1か月変化率。"),
    ("BEA，季调年率；不是当季实际金额或世界银行年度值。", "BEA: seasonally adjusted annual rate, not actual quarterly output or the World Bank annual value.", "BEAの季節調整済み年率。当該四半期の実額や世界銀行の年次値とは異なります。"),
    ("BEA，实际 GDP 季调环比折年增长率；不是同比。", "BEA: seasonally adjusted real GDP growth, quarter-on-quarter annualized; not year-on-year.", "BEAの実質GDP、季節調整済み前期比年率。前年同期比ではありません。"),
    ("联邦基金有效利率月均值；不是政策目标区间。", "Monthly average effective federal funds rate; not the policy target range.", "実効FF金利の月平均。政策目標レンジではありません。"),
    ("美国财政部固定期限收益率；节假日无报价。", "US Treasury constant maturity yield; no holiday quotations.", "米財務省の固定満期利回り。祝日は公表値がありません。"),
    ("市场还会比较实际公布值与此前预期，并考虑经济周期、政策信号和历史修订。本应用没有市场预期数据，不能据此判断本次发布是否超预期，也不自动生成买卖信号。", "Markets also compare releases with prior expectations and consider the cycle, policy signals and revisions. This app has no consensus forecasts, cannot identify a release surprise, and generates no trading signals.", "市場は公表値と事前予想を比較し、景気局面、政策シグナル、過去の改定も考慮します。本アプリには市場予想データがないため、予想との差を判定せず、売買シグナルも生成しません。"),
]
for row in ROWS:
    add(*row)

FIELDS = {
    "date": ("观测期", "Observation period", "観測期間"),
    "value": ("数值", "Value", "値"),
    "series": ("序列", "Series", "系列"),
    "unit": ("单位", "Unit", "単位"),
    "frequency": ("频率", "Frequency", "頻度"),
    "indicator": ("指标", "Indicator", "指標"),
    "source": ("来源", "Source", "出所"),
}


def lang():
    return st.session_state.get("language", "zh")


def t(text, **kwargs):
    return TEXT.get(text, {}).get(lang(), text).format(**kwargs)


def column_name(name):
    return FIELDS.get(name, (name, name, name))[("zh", "en", "ja").index(lang())]


def sidebar():
    # Permanent state is separate from widget state, which Streamlit may clear on navigation.
    st.session_state.setdefault("language", "zh")
    def changed():
        st.session_state.language = st.session_state._language_picker
    st.sidebar.selectbox("语言 / Language / 言語", list(LANGUAGES),
                         index=list(LANGUAGES).index(lang()), format_func=LANGUAGES.get,
                         key="_language_picker", on_change=changed)
    st.sidebar.page_link("app.py", label=t("首页"), icon="🌏")
    st.sidebar.page_link("pages/1_US_Economy.py", label=t("美国经济专区"), icon="🇺🇸")
    st.sidebar.page_link("pages/2_Correlation.py", label=t("相关性分析"), icon="📊")


def coverage():
    return {
        "zh": """| 指标 | 中国 / 日本 | 美国 |
|---|---|---|
| GDP、年度 CPI 通胀、年度进出口及差额 | 世界银行，已接入 | 世界银行，已接入 |
| 月度 CPI 同比/环比 | 待接入 | FRED，需密钥 |
| 政策/基准利率 | 待接入（需明确口径） | FRED 有效联邦基金利率，非目标区间 |
| 2 年 / 10 年国债收益率 | 待接入 | FRED，需密钥 |
| 非农、初请及四周均值 | 不适用 | FRED，需密钥 |

各国定义、季调和修订存在差异。未接入项没有模拟值。""",
        "en": """| Indicator | China / Japan | United States |
|---|---|---|
| GDP, annual CPI inflation, annual exports/imports/balance | World Bank, connected | World Bank, connected |
| Monthly CPI YoY / MoM | Not connected | FRED; key required |
| Policy / benchmark rate | Not connected; definitions pending | Effective federal funds rate, not target range |
| 2-year / 10-year Treasury yields | Not connected | FRED; key required |
| Payrolls, initial claims and four-week average | Not applicable | FRED; key required |

Definitions, seasonal adjustment and revisions differ across countries. No simulated values are shown.""",
        "ja": """| 指標 | 中国 / 日本 | 米国 |
|---|---|---|
| GDP、年間CPIインフレ率、年間輸出入・収支 | 世界銀行、接続済み | 世界銀行、接続済み |
| 月次CPI前年同月比 / 前月比 | 未接続 | FRED、キーが必要 |
| 政策・基準金利 | 未接続、定義の確認が必要 | 実効FF金利、目標レンジとは異なる |
| 国債2年 / 10年利回り | 未接続 | FRED、キーが必要 |
| 非農業雇用、新規失業保険申請・4週平均 | 対象外 | FRED、キーが必要 |

定義、季節調整、改定方法は国により異なります。未接続の項目に模擬値は表示しません。""",
    }[lang()]


from macroscope.statistics_translations import ROWS as STATISTICS_ROWS
for row in STATISTICS_ROWS:
    add(*row)
