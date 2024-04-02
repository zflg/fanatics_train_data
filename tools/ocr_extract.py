import json


def do_exclude(json_dict: dict):
    for img in json_dict:
        new_points = []
        points = json_dict[img]
        for point in points:
            if point['label'] == 'other':
                transcription = "###"
            else:
                transcription = point['transcription']
            new_points.append({'transcription': transcription, 'points': point['points']})
        json_dict[img] = new_points


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
    process('train_data/fanatics/train/train.json', 'train_data/fanatics/train/train_ocr.txt')
    process('train_data/fanatics/val/val.json', 'train_data/fanatics/val/val_ocr.txt')
