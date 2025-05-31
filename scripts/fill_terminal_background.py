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
    h, s, lightness = hex_to_working_space(hex_color)
    lightness = max(0, min(1, lightness + delta))
    return working_space_to_hex(h, s, lightness)


def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for attributes in root.findall('.//attributes'):
        for option in attributes.findall('.//option'):
            name = option.get('name', '')
            if (
                name.startswith('BLOCK_TERMINAL_') or
                (
                    name.startswith('CONSOLE_')
                    and name.endswith('_OUTPUT')
                )
            ):
                fg_option = bg_option = None
                for val in option.findall('.//value/option'):
                    opt_name = val.get('name')
                    if opt_name == 'FOREGROUND':
                        fg_option = val
                    elif opt_name == 'BACKGROUND':
                        bg_option = val

                if fg_option is not None and bg_option is not None:
                    fg_color = fg_option.get('value')
                    adjusted_bg_color = adjust_lightness(fg_color, delta=-0.03)
                    bg_option.set('value', adjusted_bg_color)

    tree.write(file_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <xml_file>')
        sys.exit(1)

    process_xml(sys.argv[1])
