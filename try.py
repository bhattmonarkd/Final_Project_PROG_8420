import pandas as pd


def show_products():
    print("here")
    df = pd.read_csv(r'productprice.csv', sep=',')

    print(df.to_string(index=False))
    print("false")
    print(df)
    return df


x = '1'
y = show_products()
while x == 1:
    c = y
    print(c)
