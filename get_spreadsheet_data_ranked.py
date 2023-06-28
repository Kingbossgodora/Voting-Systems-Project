import json
import pandas as pd

sheet_id = '1R8WBauQ3Xb_3csT5fNK-oxsth293oD7urJ2IF7XvVE0'
sheet_name = 'VotingScoring'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(url)

df.reset_index(inplace=True)
df.rename(columns={'index': 'order'}, inplace=True)
df = df.drop('Timestamp', axis=1)

df.iloc[:, 1:33] = df.iloc[:, 1:33].applymap(lambda x: int(x[0]))

column_mapping = {'order': 'order'}
for i in range(1, 33):
    column_mapping[df.columns[i]] = str(i)

df.rename(columns=column_mapping, inplace=True)

objects = []
for i in range(8):
    object_cols = ['order'] + [str(j) for j in range(i * 4 + 1, i * 4 + 5)]
    object_df = df[object_cols].copy()
    objects.append(object_df)

for i, obj in enumerate(objects):
    col_mapping = {'order': 'order', str(i * 4 + 1): '0', str(i * 4 + 2): '1', str(i * 4 + 3): '2', str(i * 4 + 4): '3'}
    obj.rename(columns=col_mapping, inplace=True)
    obj.to_json(f'./json_files_ranked/object_{i}.json', orient='records')

# Iterate over each JSON file
for i in range(8):
    input_file_name = f'./json_files_ranked/object_{i}.json'
    output_file_name = f'./json_files_ranked/object_{i}.json'

    with open(input_file_name, 'r') as input_file:
        data = json.load(input_file)

        reformatted_data = {}

        for obj in data:
            order = int(obj['order'])

            # Convert choice values to integers
            choices = [int(obj[str(j)]) for j in range(4)]

            # Sort choices based on ranking
            sorted_choices = sorted(enumerate(choices), key=lambda x: x[1])

            # Create the reformatted dictionary
            reformatted_data[order] = {
                'coordinates': [],
                'vote': [[choice, 0] for choice, _ in sorted_choices]
            }

        # Save the reformatted data to the output JSON file
        with open(output_file_name, 'w') as output_file:
            json.dump(reformatted_data, output_file)
