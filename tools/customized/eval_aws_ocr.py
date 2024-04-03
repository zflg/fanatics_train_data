import json
import string

manufacturer_suffix_replace = ['COMPANY, INC.', 'COMPANY, INC',
                               'COMPANY,INC.', 'COMPANY,INC',
                               'COMPANY INC.', 'COMPANY INC']


def pre(transcription: str):
    for replacement in manufacturer_suffix_replace:
        transcription = transcription.replace(replacement, 'COMPANY, INC.')
    transcription = transcription.lower()
    transcription = transcription.rstrip(string.punctuation)
    return transcription


def judge(v_input: str, v_eval: str):
    i = pre(v_input)
    e = pre(v_eval)
    return i == e


def process(input_path: str, eval_path: str):
    eval_dict = {}
    with open(eval_path, 'r') as file:
        for line in file:
            key, json_str = line.strip().split('\t')
            key = key[key.rfind('/') + 1:]
            eval_dict[key] = json.loads(json_str)
    print(eval_dict)
    # load input.
    with open(input_path, 'r') as file:
        input_dict = json.loads(file.readline())

    hit_count = 0
    total_count = len(input_dict)
    for key in input_dict:
        if key in eval_dict:
            v_eval = eval_dict[key]
            v_input = input_dict[key]
            if judge(v_input, v_eval):
                hit_count += 1
            else:
                print(f"mismatch: [{key}-{v_input}], [{key}-{v_eval}]")
        else:
            print(f'cannot find key[{key}] in eval dict')

    print(f'eval result, hit count {hit_count}, total_count {total_count}')


if __name__ == '__main__':
    # process('./tools/customized/ams_ocr.json', './train_data/fanatics/ocr_det_img/train_extract.json')

    with open('./tools/customized/crop/data2.json', 'r') as file:
        input_dict = json.loads(file.readline())
        sorted_keys = sorted(input_dict.keys())
        for key in sorted_keys:
            print(f'{key}:{input_dict[key]}')
