"""English/Japanese translations of indicator descriptions."""
from dataclasses import replace
from macroscope.explanations import WORLD_BANK_HELP, FRED_HELP

GROWTH = (
    "Stronger growth may support sales and profits, but inflation and tighter policy expectations may raise financing costs and weigh on valuations. Strong growth does not guarantee rising stocks.",
    "成長の改善は売上や利益を支える可能性がありますが、インフレや金融引き締め観測は資金調達コストを高め、評価額を圧迫することもあります。高成長が株価上昇を保証するわけではありません。",
)
INFLATION = (
    "Higher inflation may raise expected interest rates and affect costs, stock valuations and bonds. Falling inflation may ease rate pressure, but weaker demand can also hurt profits. The economic context matters.",
    "高インフレは金利見通しを押し上げ、企業コスト、株式評価、債券価格に影響する可能性があります。インフレ低下は金利圧力を和らげ得ますが、需要減速を伴えば利益も圧迫されます。景気局面も重要です。",
)
LABOR = (
    "Stronger employment may support consumption and earnings while reducing expectations for rate cuts. Weakness can bring both earnings concerns and easing expectations; a single release cannot determine stock or bond direction.",
    "雇用改善は消費や企業利益を支える一方、利下げ期待を弱める可能性があります。悪化は利益への懸念と緩和期待の両方を生むため、単独の公表値から株式や債券の方向は判断できません。",
)

# Each language tuple: definition, reading, possible market mechanism, pitfalls.
WB = {
    "GDP 总量": (
        ("The annual value of final goods and services produced in an economy, measured in current US dollars.", "Use it to compare economic size. Changes may reflect output, prices or exchange rates.", GROWTH[0], "A larger economy does not imply faster growth, greater household wealth or better stock returns. Annual data are not an immediate trading signal."),
        ("一国で1年間に生産された最終財・サービスの価値です。当年の価格と為替で米ドル換算します。", "経済規模の比較に使います。変化には生産量、物価、為替が影響します。", GROWTH[1], "経済規模の大きさは、高成長、家計の豊かさ、株式リターンの高さを意味しません。年次値は即時の売買判断には使えません。")),
    "GDP 实际增速": (
        ("The annual growth rate of output after removing price changes.", "Positive growth means output exceeds the previous year. Slower positive growth is not the same as falling output.", GROWTH[0], "Annual growth is not comparable with the US page's annualized quarter-on-quarter rate. Historical data can be revised."),
        ("物価変動を除いた実際の生産量が、前年よりどれだけ増減したかを表します。", "プラスなら前年より産出が増加しています。プラスの成長率が低下しても、産出自体の減少とは限りません。", GROWTH[1], "米国ページの前期比年率とは直接比較できません。過去の値が改定される場合があります。")),
    "CPI 年度通胀": (
        ("An annual measure of the change in prices of a representative consumer basket.", "A fall from 3% to 2% means prices are rising more slowly, not that the price level has fallen.", INFLATION[0], "This World Bank annual series is not a specific month's YoY or MoM rate. Consumer baskets and methods vary by country."),
        ("消費者が購入する代表的な財・サービスの価格変化を年次で測る指標です。", "3%から2%への低下は値上がりの減速を意味し、物価水準の下落ではありません。", INFLATION[1], "世界銀行の年次系列で、特定月の前年同月比や前月比ではありません。消費品目や統計手法は国ごとに異なります。")),
    "出口额": (
        ("The annual value of goods and services supplied to buyers abroad.", "Increases may reflect foreign demand, prices, exchange rates or the product mix; value growth need not mean greater volume.", "Stronger export demand may support related firms' revenue, but costs, exchange rates and overseas operations also affect profits. Total exports do not determine stock or currency direction.", "Includes goods and services, unlike monthly customs merchandise exports. Read alongside imports and the trade balance."),
        ("海外に販売した財・サービスの年間総額です。", "増加には海外需要、価格、為替、品目構成が影響します。金額の増加は数量の増加とは限りません。", "輸出需要の改善は関連企業の売上を支え得ますが、利益にはコスト、為替、海外事業も影響します。輸出総額だけで株価や通貨の方向は決まりません。", "財とサービスを含み、税関の月次商品輸出とは異なります。輸入と貿易収支も併せて確認します。")),
    "进口额": (
        ("The annual value of goods and services purchased from abroad.", "Growth may reflect consumption, equipment investment or production inputs, or simply higher import prices. Falling imports may signal weaker demand.", "Equipment and input imports may accompany investment expansion, while higher energy costs may squeeze profits. More imports are not automatically bad for markets.", "Separate price, volume and composition effects. A change in net exports alone does not establish the direction of domestic demand or total GDP."),
        ("海外から購入した財・サービスの年間総額です。", "増加は消費、設備投資、生産投入の拡大や輸入価格の上昇を反映します。減少が需要減速を示すこともあります。", "設備や原材料の輸入は投資拡大を伴う場合がありますが、エネルギー価格上昇は利益を圧迫し得ます。輸入増は一律に悪材料ではありません。", "価格、数量、品目構成を区別します。純輸出の変化だけで内需やGDP全体の方向は判断できません。")),
    "贸易差额": (
        ("Annual exports of goods and services minus imports. Positive means a surplus; negative means a deficit.", "Ask whether the change comes from exports or imports. A larger surplus can reflect stronger exports or falling imports, with different meanings.", "Trade can affect industry earnings and cross-border currency demand, but exchange rates also depend on interest differentials, capital flows and risk appetite. A larger surplus does not guarantee currency appreciation.", "Calculated from two annual national accounts series; not the full balance of payments or monthly customs trade balance."),
        ("年間の財・サービス輸出から輸入を差し引いた値です。プラスは黒字、マイナスは赤字です。", "輸出と輸入のどちらが変化したかを確認します。黒字拡大は輸出増でも輸入減でも起こり、経済的な意味が異なります。", "貿易は業種別利益や通貨需要に影響し得ますが、為替には金利差、資本移動、リスク選好も関係します。黒字拡大が通貨高を保証するわけではありません。", "2つの年次国民経済計算系列から算出します。国際収支全体や税関の月次貿易収支ではありません。")),
}

US = {
    "非农就业月度变动": (
        ("The net monthly change in paid nonfarm jobs in the US, indicating changes in employers' staffing.", "Calculated as the difference in seasonally adjusted PAYEMS. Units are thousands: 100 means about 100,000 additional jobs, not total employment or an unemployment rate.", LABOR[0], "Jobs are not unique people; one person may hold several jobs. Wages, unemployment and revisions also matter; those additional indicators are not connected here."),
        ("米国の非農業部門の給与雇用数が前月から純増・純減した数で、企業の雇用動向を示します。", "季節調整済みPAYEMSの差分です。単位は千人で、100なら約10万の雇用増です。雇用総数や失業率ではありません。", LABOR[1], "雇用数は人数と一致せず、1人が複数の仕事を持つ場合があります。賃金、失業率、過去の改定も重要ですが、補助指標は未接続です。")),
    "初请失业金人数": (
        ("Weekly first-time claims for US unemployment insurance, a frequent indicator of labor market conditions.", "Persistent increases may indicate weakening, but holidays, weather, strikes and seasonal adjustment can affect a single week.", LABOR[0], "Not the total unemployed and not all unemployed people are covered. One week's change cannot establish a recession."),
        ("米国で1週間に初めて失業保険を申請した件数で、労働市場を高頻度で観察できます。", "増加が続く場合は労働市場の弱まりを示し得ますが、単週値には祝日、天候、ストライキ、季節調整も影響します。", LABOR[1], "失業者総数ではなく、すべての失業者を対象とするものでもありません。1週の変化で景気後退は判断できません。")),
    "初请四周均值": (
        ("The average of initial unemployment claims over the latest four weeks, smoothing weekly fluctuations.", "A persistent trend is easier to interpret than one week's spike, but smoothing can delay recognition of turning points. The app uses the official series.", LABOR[0], "Still initial claims, not continuing claims or the unemployment rate. Averaging does not remove all temporary influences."),
        ("直近4週間の新規失業保険申請件数の平均で、単週の変動を和らげます。", "一時的な急増より継続的な傾向を読みやすくしますが、転換点への反応は遅れ得ます。公式の平均系列を使用します。", LABOR[1], "継続受給件数や失業率ではなく、新規申請の指標です。平均でも一時的要因はすべて除けません。")),
    "CPI 同比": (
        ("The percentage change in US consumer prices from 12 months earlier.", "Calculated from seasonally adjusted CPI. A lower rate may reflect slower recent price increases or a higher comparison base; also check month-on-month changes.", INFLATION[0], "A declining positive rate is not falling prices. This is neither official unadjusted YoY inflation, core CPI nor the Fed's PCE inflation measure."),
        ("米国の消費者物価指数が12か月前から何%変化したかを表します。", "季節調整済みCPIから算出します。低下は最近の値上がり減速や前年の高い基準値を反映し得るため、前月比も確認します。", INFLATION[1], "プラスの率が低下しても物価下落ではありません。非季調の公式前年同月比、コアCPI、FRBのPCE指標とは異なります。")),
    "CPI 环比": (
        ("The percentage change in US consumer prices from the previous month, emphasizing recent developments.", "Calculated from seasonally adjusted CPI. A 0.2% reading is a one-month change, not annual inflation; check several months before inferring a trend.", INFLATION[0], "Short-term price shocks can move monthly rates. Seasonal adjustment does not remove all noise. Components and core CPI are not shown here."),
        ("米国の消費者物価指数が前月から何%変化したかを示し、直近の変化を捉えます。", "季節調整済みCPIを使います。0.2%は1か月の変化で、年間率ではありません。傾向は複数月で確認します。", INFLATION[1], "短期の価格変動に左右されます。季節調整でもすべての雑音は除けず、内訳やコアCPIはここでは表示しません。")),
    "GDP 总量": (
        ("US quarterly final output at current prices, seasonally adjusted and expressed at an annual rate.", "Units are billions of dollars. The annual rate scales the quarter's production pace to a year; it is not the amount actually produced that quarter.", GROWTH[0], "Nominal output includes price changes and cannot replace real growth. It is not the same frequency or measure as the World Bank annual GDP series."),
        ("米国の四半期の最終産出を当年価格で測り、季節調整後に年率換算した総額です。", "単位は10億ドルです。その四半期の生産ペースを1年分に換算した値で、当該四半期の実額ではありません。", GROWTH[1], "名目値には物価変動が含まれ、実質成長率の代用にはなりません。世界銀行の年次GDPとは頻度も指標も異なります。")),
    "GDP 实际增速": (
        ("The change in US inflation-adjusted output from the previous quarter, expressed at an annualized rate.", "An annualized 4% does not mean output actually rose 4% that quarter or 4% year-on-year. Slower positive growth is not falling output.", GROWTH[0], "Quarterly estimates are revised; composition matters. Do not directly compare this annualized quarterly rate with annual growth on the home page."),
        ("米国の物価調整後の産出が前四半期からどれだけ変化したかを年率換算した値です。", "年率4%は、実際の前期比4%や前年同期比4%という意味ではありません。プラスの成長率の低下は産出減少とは限りません。", GROWTH[1], "四半期値は改定され、成長の内訳も重要です。ホームの年間成長率とは直接比較しないでください。")),
    "联邦基金有效利率": (
        ("A measure of the actual overnight rate on federal funds transactions between US depository institutions, shown as a monthly average.", "Indicates short-term funding costs and monetary transmission. A monthly average smooths within-month changes and is not an individual policy decision.", "Higher rates can raise funding costs and the discount rate applied to future earnings, affecting stocks, bonds and currencies. Cuts may ease costs but can coincide with worsening growth and weaker stocks.", "The effective rate is not the Fed target range. Markets may reprice before policy actually changes."),
        ("米国の預金取扱機関の間で取引される翌日物FF金利の実効値を、月平均で表示します。", "短期資金コストと政策の波及を観察します。月平均は月内変化を平滑化しており、個別の政策決定そのものではありません。", "金利上昇は資金コストや将来利益の割引率を高め、株式、債券、為替に影響し得ます。利下げは負担を和らげ得ますが、景気悪化を伴えば株価も弱まる場合があります。", "FRBの目標レンジではなく実効金利です。市場は実際の政策変更より前に価格を調整する場合があります。")),
    "2 年国债收益率": (
        ("A US Treasury constant maturity yield at the two-year point of the yield curve.", "Often used to observe pricing of the next few years' short-term rate path, but risk premia also matter. It is not a guaranteed investment return.", "Higher yields generally mean lower prices for comparable fixed-rate bonds, and vice versa. Shorter-maturity yields can also change other assets' relative appeal.", "A yield change is not a bond's total return. Holding period, coupon and purchase price also matter."),
        ("米財務省が公表するイールドカーブの2年固定満期利回りです。", "数年間の短期金利見通しの織り込みに注目する際に使いますが、リスクプレミアムも影響します。確約された投資収益率ではありません。", "利回り上昇は通常、比較可能な固定利付債券の価格下落に対応し、逆も同様です。短期側の利回りは他資産の相対的魅力にも影響し得ます。", "利回りの変化は債券の総収益ではありません。保有期間、利払い、購入価格も関係します。")),
    "10 年国债收益率": (
        ("A US Treasury constant maturity yield at ten years, commonly used to observe longer-term financing conditions.", "Reflects expected future short-term rates and term premia, not just inflation expectations. Compare with the two-year yield to study the term structure.", "Higher long yields can raise long-term financing costs and affect valuation discounting; comparable fixed-rate bond prices generally fall. Longer bonds are often more rate-sensitive, other things equal.", "Falling yields may reflect easing inflation, growth concerns or safe-haven demand; they do not guarantee rising stocks."),
        ("米財務省が公表する10年固定満期利回りで、長期の資金調達環境の観察に使います。", "将来の短期金利予想と期間プレミアムなどを反映し、インフレ予想だけでは説明できません。2年利回りと比べると期間構造を観察できます。", "長期利回り上昇は長期調達費や評価の割引率に影響し、比較可能な固定利付債券の価格は通常下がります。他条件が同じなら長期債ほど金利変動に敏感な傾向があります。", "利回り低下はインフレ緩和、成長懸念、逃避需要のいずれも反映し得るため、株価上昇を保証しません。")),
}


def localized_help(label, group, language):
    original = (FRED_HELP if group == "US" else WORLD_BANK_HELP)[label]
    if language == "zh":
        return original
    values = (US if group == "US" else WB)[label][0 if language == "en" else 1]
    return replace(original, meaning=values[0], reading=values[1], market=values[2], caution=values[3])
