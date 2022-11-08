import pandas as pd

#Pricing an IRS maturing in 3 years.
df = pd.read_csv('rates.csv')

notional = input("\n\nEnter the notional: \n")

df['float_leg'] = df['Fwd_rate (quarter)'] * float(notional) * 0.25

df['DiscFactor'] = 1 / (1 + df['Spot_rate (annual)'] / 4) ** (df['Maturity (years)'] * 4)

df['float_legPV'] = df['DiscFactor'] * df['float_leg']

#To drop the first row because of N\A values
df = df.drop(0)

#Fixed leg coupon is equal to the sum of the present values of the float leg cash flows divided by the sum of the discount factors.
fixed_leg = df['float_legPV'].sum() / df['DiscFactor'].sum()
print("\nFixed Leg = " + str(fixed_leg))

FixedRate = float(fixed_leg) / float(notional)
print("\nFixed Rate = " + str(FixedRate) + "\n")

df['fixed_leg'] = (fixed_leg)
df['fixed_legPV'] = df['DiscFactor'] * (fixed_leg)
print(df)

with pd.ExcelWriter('output.xlsx') as writer:
	df.to_excel(writer, sheet_name = 'Sheet_1')
