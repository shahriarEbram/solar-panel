import pandas as pd
import jalali


def convert_gregorian_to_jalali(df):
    df["date"] = df["date"].str.replace("/", "-")
    #df['date'] = pd.to_datetime(df['date'])
    df['jdate'] = df['date'].apply(lambda date: jalali.Gregorian(date).persian_string())
    return df

#df2 = df[df['jdate'].apply(lambda x: x.split("-")[1] == '8')]