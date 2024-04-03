from PIL import Image
from pathlib import Path
import json

extract_base_path = './train_data/fanatics/ocr_det_img'


# extract img
def extract(source_path: str, pos, target_path: str):
    # open source image
    source = Image.open(source_path)
    if pos[1][0] < pos[0][0] or pos[3][1] < pos[0][1]:
        raise ValueError(f'position error: {pos}')
    # empty target img
    target_img = Image.new('RGB', (pos[1][0] - pos[0][0], pos[3][1] - pos[0][1]))
    # extract to targe img
    for y in range(pos[0][1], pos[3][1]):
        for x in range(pos[0][0], pos[1][0]):
            pixel = source.getpixel((x, y))
            target_img.putpixel((x - pos[0][0], y - pos[0][1]), pixel)
    # save extract img
    target_img.save(target_path)


def extract_img_path(img_path_str: str, index: int):
    img_path = Path(img_path_str)
    # batch: 1,2,3,4,5,6,7,8
    batch_path = img_path.parent
    # train of val
    type_path = batch_path.parent
    # create extract path
    extract_path = Path(f'{extract_base_path}/{type_path.name}/{batch_path.name}')
    if not extract_path.exists():
        extract_path.mkdir(parents=True)
    # return relative img path
    return f'{type_path.name}/{batch_path.name}/{img_path.name}_{index}.jpg'


def extract_img(json_dict: dict, source_base_path: Path):
    extract_dict = {}
    for img in json_dict:
        img_path = str(source_base_path.joinpath(img))
        points = json_dict[img]
        for index, point in enumerate(points):
            # get extract img relative path
            extract_path = extract_img_path(img_path, index)
            try:
                if point['transcription'] == '###':
                    continue
                # extract img
                extract(img_path, point['points'], extract_base_path + '/' + extract_path)
                # set to extract dict.
                extract_dict[extract_path] = point['transcription']
            except ValueError as ve:
                print(f'extract error: {ve}')
                continue
    return extract_dict


def process(input_path: str, output_path: str):
    data = {}
    source_base_path = Path(input_path).parent
    # load data.
    with open(input_path, 'r') as file:
        for line in file:
            key, json_str = line.strip().split('\t')
            data[key] = json.loads(json_str)
    # de_dup
    extract_data = extract_img(data, source_base_path)
    # export
    with open(output_path, 'w') as file:
        for key, value in extract_data.items():
            json_str = json.dumps(value)
            file.write(f"{key}\t{json_str}\n")


if __name__ == '__main__':
    process('train_data/fanatics/train/train_ocr.txt', f'{extract_base_path}/train_extract.json')
    process('train_data/fanatics/val/val_ocr.txt', f'{extract_base_path}/val_extract.json')
