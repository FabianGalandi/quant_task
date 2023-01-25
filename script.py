import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helper import do_three_years

plt.rcParams["font.family"] = "serif"

st.write(f'#### Task Solution')

total = st.number_input('total asset value in EUR', min_value=0, value=1000000 , step=100000)

"""
```python
Set the relative decline of the following assets:
```
"""

# Add a sliders
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

##########################################################
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

with plt.style.context('tableau-colorblind10'):
  fig, ax = plt.subplots()
  ax.set_title('Assets and Liabilities over the course of 3 years')
  ax.set_xlabel('year')
  ax.set_ylabel('amount in EUR')
  ax.set_axisbelow(True) #to make gridlines behind bars
  

  df_final_fixed.plot.bar(ax = ax, grid=True)
  fig.dpi = 150

st.pyplot(fig)

"""
The follwing **Daframe** was used to generate the barchart above (If you see some :red[**red**] entries below, you will not be able to service your payments and commitments)
"""

st.table(df_final_fixed.style.highlight_between(color="red",left=-9999999, right=0))


"""
---
# Multiple Worst Case Scenarios
"""

n_samples = st.number_input('Number of Scenarios', min_value=1 , value=1000, step=1000)

"""
```python
Generating random scenarios based on a multivariate normal distribution:
```
"""



# parameters: prior distribution of value deline
mean = [0.5, 0.3, 0.1, 0.1]
cov = np.array(
       [[0.7,  1,   0,   0],
       [  1, 0.3,   0,   0],
       [  0,   0, 0.1, 0.2],
       [  0,   0, 0.2, 0.1]])
cov *= 0.01 # scaling of cov-matrix

c5, c6 = st.columns(2)
with c5:
  # st.write("**Mean** (change sliders below)")
  mean_stocks = st.slider('mean_stocks_decline',0.0, 1.0, 0.5)
  mean_bonds = st.slider('mean_bonds_decline',0.0, 1.0, 0.3)
  mean_flat1 = st.slider('mean_flat_potsdam_decline',0.0, 1.0, 0.1)
  mean_flat2 = st.slider('mean_flat_berlin_decline',0.0, 1.0, 0.1)
  mean = [mean_stocks, mean_bonds, mean_flat1, mean_flat2]
  st.write("**Variance Matrix** (cannot be changed here):")
  st.table(cov)
# with c6:


worst_case_scenarios =  np.random.multivariate_normal(mean, cov, n_samples).clip(0,1)

fig2, ax2 = plt.subplots(figsize=(8,15))

wcs_T = list(np.transpose(worst_case_scenarios))
ax2.violinplot(wcs_T, showmeans=True)
ax2.set_title('Violin plot showing the value decline distribution per asset')
ax2.set_xticks([y + 1 for y in range(len(wcs_T))], labels= ["stocks","bonds", "flat_berlin", "flat_potsdam"])
ax2.yaxis.grid(color='gray', linestyle='dashed')
fig2.dpi = 150

with c6:
  st.pyplot(fig2)

# pc_df = pd.DataFrame(wcs_T).T
# pc_df['wc_idx'] = pc_df.index

# fig3, ax3 = plt.subplots()
# color = ['#1155bb'] * n_samples
# pd.plotting.parallel_coordinates(pc_df, 'wc_idx', color=color, ax=ax3, alpha=0.05)
# ax3.get_legend().remove()

# st.pyplot(fig3)


# calculate three years for every worst case scenario
results = []
for worst_case_scenario in worst_case_scenarios:
    results.append(do_three_years(1000000, worst_case_scenario))

# columns ^= afer i years, 
# rows ^= scenarios
# element at i,j is dict with portfolio values
df = pd.DataFrame(results)

def map_func(x):
    # aggregate stock & bonds and flats
    decline_stock_bonds = np.mean([x["scenario"][0], x["scenario"][1]])
    decline_flats = np.mean([x["scenario"][2], x["scenario"][3]])

    # check if payments are too much to service
    is_positive = all(value >= 0 for value in x['assets'].values())

    return {"is_positive": is_positive,"mean_decline_stock_bonds": decline_stock_bonds, "mean_decline_flats": decline_flats}


after_three_years = df.applymap(map_func)[3] # after 3 years

final_df = pd.DataFrame(after_three_years.to_list())
cmap = ['#377eb8', '#ff7f00']
final_df['color'] = final_df.apply(lambda x: cmap[0] if x['is_positive'] else cmap[1], axis=1) # add color column for visualization

count = final_df['is_positive'].sum()/n_samples * 100
count = np.around(count, 2)
st.write("---")
st.write("## In", count, "% of cases you will be able service your payments and commitments.")
st.write("---")



fig4, ax4 = plt.subplots()
final_df.plot.scatter(x = 'mean_decline_stock_bonds', y = 'mean_decline_flats', c='color',figsize=[5,5], ax=ax4, grid=True)
ax4.set_axisbelow(True) #to make gridlines behind plot
ax4.set_title('Will you be able to service your payments and commitments? \nEach dot represents one scenario (Blue=Yes, Orange=No)')
st.pyplot(fig4)






"""
---
A Jupyter Notebook of this solution can be found here:
https://drive.google.com/file/d/1TE54GRqBIC2tQirbr7IJdiBX8Kd8UpsX/view?usp=sharing
"""


"""
#### TASK DETAILS:

You have multiple investments: some stocks, some bonds, a flat in Berlin and a flat in Potsdam. Each investment’s
net asset value makes up 25 % or your portfolio. You purchased both flats in January, but 30 % of the purchase
prices have been financed with a bank loan that needs to be repaid in three equal instalments. The bank demands
the yearly repayments of 10 % of the initial value on the flats in December, but they charge you no interest.

Instead of reinvesting the returns of your investment portfolio, you donate them to a friend who runs a kindergarten. Your friend wants to know how much to expect in donations each year’s December, but it is difficult for 
you to make predictions. You guarantee your friend half of last year’s donation (since this is your first year, you
assume that you would have made, in total, a donation amounting to 5 % of your portfolio value). In addition,
you commit to donating 2,5 % of your beginning-of-year portfolio value each year.

You are not sure whether the payments and donation commitments are too much to service. Therefore, you
come up with the worst case you can think of: you just purchased your flats in January, but then your stocks
lose a third of their value, your bonds lose a fifth of their value, and your flats each lose one tenth of their value.
For three years, your stocks, bonds and flats neither appreciate nor depreciate from market movements, you
receive no rental income from your flats, but you’re free to sell any amount of your stocks and/or bonds as you
see fit.

* **Question 1** Will you be able to service your payments and commitments during these three years?
* **Question 2** If we provide you with a list of thousands of our worst-case scenarios, in how many of them would you be able to service your payments and donations?
"""