import json


# check rectangle
def is_rectangle(points):
    # 检测四个点是否能够构成矩形
    if len(points) != 4:
        return False

    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    if len(set(x_coords)) != 2 or len(set(y_coords)) != 2:
        return False

    return True


# check overlap
def check_overlap(points1, points2):
    # pointer index range
    x1 = min(p[0] for p in points1)
    y1 = min(p[1] for p in points1)
    x2 = max(p[0] for p in points1)
    y2 = max(p[1] for p in points1)

    x3 = min(p[0] for p in points2)
    y3 = min(p[1] for p in points2)
    x4 = max(p[0] for p in points2)
    y4 = max(p[1] for p in points2)

    # overlap check
    if x1 <= x4 and x2 >= x3 and y1 <= y4 and y2 >= y3:
        return True

    return False


def de_overlap(json_dict: dict):
    for img in json_dict:
        de_overlap_points = []
        points = json_dict[img]
        img_dup = False
        for point0 in points:
            # check list
            dup = False
            for point1 in points:
                if (point0 != point1
                        and check_overlap(point0['points'], point1['points'])
                        and point0['label'] == 'other'
                        and point1['label'] != 'other'):
                    print(
                        'Image {} has overlap pointers, dup0 label-{} transcription-{} pointers-{}, dup1 label-{} transcription-{} pointers-{}'
                        .format(img, point0['label'], point0['transcription'], point0['points'],
                                point1['label'], point1['transcription'], point1['points']))
                    dup = True
                    img_dup = True
                    break
                if (point0['label'] == 'year'
                        and point1['label'] == 'manufacturer'
                        and check_overlap(point0['points'], point1['points'])):
                    print('Image {} year and manufacturer overlap, year pointers-{}, manufacturer pointers-{}'
                          .format(img, point0['points'], point1['points']))
                    max_x = max(point0['points'], key=lambda point: point[0])[0]
                    print('year max x is ', max_x)
                    point1['points'][0][0] = max_x
                    point1['points'][3][0] = max_x
                    print('After process, year pointers-{}, manufacturer pointers-{}'
                          .format(img, point0['points'], point1['points']))
                    break
            if not dup:
                de_overlap_points.append(point0)
        if not img_dup:
            print('Image {} no overlap!'.format(img))
        json_dict[img] = de_overlap_points


def process(input_path: str, output_path: str):
    data = {}
    # load data.
    with open(input_path, 'r') as file:
        for line in file:
            key, json_str = line.strip().split('\t')
            data[key] = json.loads(json_str)
    # de_dup
    de_overlap(data)
    # export
    with open(output_path, 'w') as file:
        for key, value in data.items():
            json_str = json.dumps(value)
            file.write(f"{key}\t{json_str}\n")


if __name__ == '__main__':
    process('train_data/fanatics/train/train.json', 'train_data/fanatics/train/train_de_overlap.json')
    process('train_data/fanatics/val/val.json', 'train_data/fanatics/val/val_de_overlap.json')
