#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from skimage import color
import numpy as np
from pathlib import Path
import json


def hex_to_rgb(hex_color):
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]


def hex_to_lab(hex_color):
    rgb = np.array(hex_to_rgb(hex_color)).reshape(1, 1, 3)
    return color.rgb2lab(rgb).reshape(3)


def color_distance_lab(color1, color2):
    lab1 = hex_to_lab(color1)
    lab2 = hex_to_lab(color2)
    return np.linalg.norm(lab1 - lab2)


def extract_xml_colors(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    results = []

    for option in root.findall('.//colors/option'):
        current_hex = option.get('value')
        if current_hex != '':
            results.append(('COLOR', current_hex, option.get('name')))

    for option in root.findall('.//attributes/option'):
        for val in option.findall('.//value/option'):
            value_name = val.get('name')
            if value_name in ('FOREGROUND', 'BACKGROUND'):
                current_hex = val.get('value')
                results.append((value_name, current_hex, option.get('name')))

    return results


def extract_json_colors(json_path):
    results = []

    def recurse(d, prefix):
        if isinstance(d, dict):
            for k, v in d.items():
                recurse(v, f'{prefix}.{k}')
        elif isinstance(d, str):
            v = d.lstrip('#')
            if len(v) == 6 and all(c in '0123456789abcdefABCDEF' for c in v):
                results.append(('JSON', v, prefix))

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        recurse(data.get('ui', {}), 'ui')

    return results


def find_closest_colors(xml_file, json_file, target_hex, filter):
    results = []

    for kind, color_hex, label in (extract_json_colors(json_file) + extract_xml_colors(xml_file)):
        dist = color_distance_lab(target_hex, color_hex)
        results.append((dist, kind, color_hex, label))

    if filter:
        results = [x for x in results if x[1] in filter]
    results.sort()

    for dist, opt_type, hex_col, opt_name in results:
        print(f'{opt_type:<10} | {hex_col} | distance: {dist:6.2f} | from: {opt_name}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <hex_color> [<filter>]')
        sys.exit(1)

    root_dir = Path(__file__).resolve().parent.parent
    xml_file = root_dir / 'resources' / 'Helsing.xml'
    json_file = root_dir / 'resources' / 'Helsing.theme.json'
    target_color = sys.argv[1].lstrip('#')
    if len(sys.argv) >= 3:
        filter = sys.argv[2].split(',')
    else:
        filter = None

    find_closest_colors(xml_file, json_file, target_color, filter)
