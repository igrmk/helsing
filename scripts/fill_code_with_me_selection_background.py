#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import colorsys


def hex_to_working_space(hex_color):
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v


def working_space_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))


def adjust_lightness(hex_color, delta=-0.1):
    h, s, v = hex_to_working_space(hex_color)
    v = max(0, min(1, v + delta))
    return working_space_to_hex(h, s, v)


def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for attributes in root.findall('.//attributes'):
        marker_colors = {}
        for option in attributes.findall('.//option'):
            name = option.get('name', '')

            if name.startswith('CodeWithMe.USER_') and name.endswith('_MARKER'):
                user_number = name.split('_')[1]
                bg_option = option.find(".//option[@name='BACKGROUND']")

                if bg_option is not None:
                    marker_colors[user_number] = bg_option.get('value')

        # Adjust USER_n_SELECTION based on marker background
        for option in attributes.findall('.//option'):
            name = option.get('name', '')

            if name.startswith('CodeWithMe.USER_') and name.endswith('_SELECTION'):
                user_number = name.split('_')[1]
                selection_bg_option = option.find(".//option[@name='BACKGROUND']")

                if selection_bg_option is not None and user_number in marker_colors:
                    selection_bg_color = adjust_lightness(marker_colors[user_number], delta=-0.5)
                    selection_bg_option.set('value', selection_bg_color)

    tree.write(file_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <xml_file>')
        sys.exit(1)

    process_xml(sys.argv[1])

