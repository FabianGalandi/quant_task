import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helper import do_three_years

total = 1000000

'''
### Task Solution
'''

# Add a slider
st.write(f'**Assuming a total portfolio value of {total} EUR**')

st.write(">Set the Relative Decline of the following assets:")

c1, c2, c3, c4 = st.columns(4)

with c1:
  a = st.slider(
      'stocks',
      0.0, 1.0, 0.33
  )

with c2:
  b = st.slider(
      'bonds',
      0.0, 1.0, 0.2
  )

with c3:
  c = st.slider(
      'flat in Berlin',
      0.0, 1.0, 0.1
  )

with c4:
  d = st.slider(
      'flat in Potsdam',
      0.0, 1.0, 0.1
  )

### ---
st.write(">Assets and liabilities values over the course of 3 years:")
fixed_worst_case = [a, b, c, d]
timeseries = do_three_years(total, fixed_worst_case)


# for year, x in enumerate(timeseries):
#     st.write("--------------------")
#     st.write(f"YEAR {year}")
#     st.write(x['liabilities'])
#     st.write(x['assets'])
#     #st.write(x['scenario'])
#     st.write(f"total asset value = {sum(x['assets'].values())} EUR")


# s_params = df.iloc[test_s][0]['scenario']
tmp1 = pd.DataFrame(map(lambda x: x['assets'], timeseries))
tmp2 = pd.DataFrame(map(lambda x: x['liabilities'], timeseries))
df_final_fixed = pd.concat([tmp1, tmp2], axis=1)

st.line_chart(df_final_fixed)

"""
**Daframe** used to generate the chart above (If you see some **red** elements below, you will not be able to service your payments)
"""

st.table(df_final_fixed.style.highlight_between(color="red",left=-9999999, right=0))

"""
A more elaborate solution can be found here:
https://drive.google.com/file/d/1TE54GRqBIC2tQirbr7IJdiBX8Kd8UpsX/view?usp=sharing
"""