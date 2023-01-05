# Copyright (c) OpenMMLab. All rights reserved.
import argparse
from pathlib import Path

import torch


def convert_weights(weight):
    """Weight Converter.

    Converts the weights from timm to mmcls

    Args:
        weight (dict): weight dict from timm

    Returns: converted weight dict for mmcls
    """
    result = dict()
    result['meta'] = dict()
    temp = dict()
    mapping = {
        'patch_embed.proj': 'patch_embed.projection',
        'mlp.fc1': 'ffn.layers.0.0',
        'norm.': 'ln1.',
        'mlp.fc2': 'ffn.layers.1',
        'norm1': 'ln1',
        'norm2': 'ln2',
        'blocks': 'layers'
    }
    for k, v in weight["model"].items():
        print(k)
        for mk, mv in mapping.items():
            if mk in k:
                k = k.replace(mk, mv)
        print("=>",k)
        temp[k] = v
    result['state_dict'] = temp
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert model keys')
    parser.add_argument('src', help='src detectron model path')
    parser.add_argument('dst', help='save path')
    args = parser.parse_args()
    dst = Path(args.dst)
    if dst.suffix != '.pth':
        print('The path should contain the name of the pth format file.')
        exit(1)
    dst.parent.mkdir(parents=True, exist_ok=True)

    original_model = torch.load(args.src, map_location='cpu')
    converted_model = convert_weights(original_model)
    torch.save(converted_model, args.dst)