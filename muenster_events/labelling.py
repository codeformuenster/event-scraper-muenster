"""Terminal interface to manually create labels."""

import model

df = model.read_events_df()

# create column 'label_family', if not exist
if 'label_family' not in df:
    df['label_family'] = None

# WHILE any entry not labelled, yet:
while df['label_family'].isnull().values.any():
    # label next event without label
    row = df.loc[df['label_family'].isnull()].head(1)
    print("Text of event " + str(row.id.values[0]) + ":")
    text = row['title'] + " - " + row['subtitle'] + " - " + row['details']
    print(text.values[0])
    while True:
        user_label = input("Relevant for families? Enter 1 or 0: ")
        if (user_label == '1') | (user_label == '0'):
            break
    df.loc[df['id'] == int(row['id']), 'label_family'] = int(user_label)
    # exit loop or add next label?
    user_input = input("Stop labelling? (y/N): ")
    if user_input is 'y':
        break

# count events with and without label
print('Label counts:')
print(df['label_family'].value_counts(dropna=False))

# write updated values to database
model.write_events_df(df)
