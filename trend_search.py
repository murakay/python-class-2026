from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 日本語フォント設定
plt.rcParams['font.family'] = 'Meiryo'  # または 'MS Gothic'

# 取得キーワード
#keyword = "選挙"
#keyword = "高市"
#keyword = "保全"
keyword = "Claude"

# pytrends でデータ取得
pytrends = TrendReq(hl='ja-JP', tz=540)
pytrends.build_payload(kw_list=[keyword])
data = pytrends.interest_over_time()

# 月単位に集計（平均値）※ "M" → "ME" に変更
monthly = data.resample("ME").mean()

# グラフ描画
monthly.plot(y=keyword, figsize=(12,4))
plt.title(f"Googleトレンド: {keyword}（月別）")
plt.xlabel("年月")
plt.ylabel("人気度")
plt.show()
