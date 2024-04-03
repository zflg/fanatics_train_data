import json


def do_exclude(json_dict: dict):
    for img in json_dict:
        exclude_other_points = []
        points = json_dict[img]
        for point in points:
            # check list
            if point['label'] != 'other':
                exclude_other_points.append(point)
        json_dict[img] = exclude_other_points


def process(input_path: str, output_path: str):
    data = {}
    # load data.
    with open(input_path, 'r') as file:
        for line in file:
            key, json_str = line.strip().split('\t')
            data[key] = json.loads(json_str)
    # de_dup
    do_exclude(data)
    # export
    with open(output_path, 'w') as file:
        for key, value in data.items():
            json_str = json.dumps(value)
            file.write(f"{key}\t{json_str}\n")


if __name__ == '__main__':
    process('train_data/fanatics/train/train.json', 'train_data/fanatics/train/train_exclude_other.json')
    process('train_data/fanatics/val/val.json', 'train_data/fanatics/val/val_exclude_other.json')
