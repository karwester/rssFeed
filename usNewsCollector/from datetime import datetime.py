from datetime import datetime
from dateutil import tz
import pandas as pd
d = 'Wed, 03 May 2023 05:36:31 EDT'
d = d[5:25]
print(d)
entryPublished = pd.to_datetime(d, format="%d %b %Y %H:%M:%S")
print(entryPublished)

#p = pd.to_datetime(d, infer_datetime_format=True)
#print(p)