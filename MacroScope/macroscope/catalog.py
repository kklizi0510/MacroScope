"""Explicit definitions prevent mixing units or silently substituting indicators."""
from dataclasses import dataclass

COUNTRIES = {"中国": "CHN", "美国": "USA", "日本": "JPN"}


@dataclass(frozen=True)
class Indicator:
    code: str
    unit: str
    frequency: str
    note: str


WORLD_BANK = {
    "GDP 总量": Indicator("NY.GDP.MKTP.CD", "美元（现价）", "年度", "名义 GDP；受汇率影响，不代表实际产出增速。"),
    "GDP 实际增速": Indicator("NY.GDP.MKTP.KD.ZG", "%", "年度", "不变价 GDP 年增长率。"),
    "CPI 年度通胀": Indicator("FP.CPI.TOTL.ZG", "%", "年度", "年度 CPI 通胀；不是某个月的同比或环比。"),
    "出口额": Indicator("NE.EXP.GNFS.CD", "美元（现价）", "年度", "货物和服务出口，国民账户口径。"),
    "进口额": Indicator("NE.IMP.GNFS.CD", "美元（现价）", "年度", "货物和服务进口，国民账户口径。"),
    "贸易差额": Indicator("balance", "美元（现价）", "年度", "同年货物和服务出口减进口；不是海关月度商品贸易帐。"),
}

FRED = {
    "非农就业月度变动": Indicator("PAYEMS", "千人", "月度", "BLS，季调非农就业总量的一阶差分；包含历史修订。"),
    "初请失业金人数": Indicator("ICSA", "人", "周度", "美国劳工部，季调；日期为周结束日。"),
    "初请四周均值": Indicator("IC4WSA", "人", "周度", "美国劳工部发布的季调四周移动平均。"),
    "CPI 同比": Indicator("CPIAUCSL", "%", "月度", "BLS，季调 CPI 指数计算的 12 个月变化；与非季调官方同比可能不同。"),
    "CPI 环比": Indicator("CPIAUCSL", "%", "月度", "BLS，季调 CPI 指数计算的 1 个月变化。"),
    "GDP 总量": Indicator("GDP", "十亿美元（现价，年率）", "季度", "BEA，季调年率；不是当季实际金额或世界银行年度值。"),
    "GDP 实际增速": Indicator("A191RL1Q225SBEA", "%（环比折年率）", "季度", "BEA，实际 GDP 季调环比折年增长率；不是同比。"),
    "联邦基金有效利率": Indicator("FEDFUNDS", "%", "月度", "联邦基金有效利率月均值；不是政策目标区间。"),
    "2 年国债收益率": Indicator("DGS2", "%", "日度", "美国财政部固定期限收益率；节假日无报价。"),
    "10 年国债收益率": Indicator("DGS10", "%", "日度", "美国财政部固定期限收益率；节假日无报价。"),
}

