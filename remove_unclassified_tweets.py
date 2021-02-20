import helpers
import dataset as ds

df = helpers.load_dataset(ds.output_data + 'sentiwordnet_labelled.csv')

df2 = df[(df.sentiment_class == "Positive") | (df.sentiment_class == "Negative") | (df.sentiment_class == "Neutral")]
df3 = df[(df.sentiment_class != "Positive") & (df.sentiment_class != "Negative") & (df.sentiment_class != "Neutral")]
print(df3)
helpers.dataframe_to_csv(df2, ds.output_data + "sentiwordnet_labelled_unclassified_removed.csv")
helpers.dataframe_to_csv(df3, ds.output_data + "unclassified.csv")
