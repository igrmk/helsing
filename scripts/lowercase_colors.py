#!/usr/bin/env python3

import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

HEX_DIGITS = set("0123456789abcdefABCDEF")


def _to_lower_hex(value: str) -> str:
    if not isinstance(value, str):
        return value
    prefix = "#" if value.startswith("#") else ""
    core = value.lstrip("#")
    if len(core) == 6 and all(c in HEX_DIGITS for c in core):
        return prefix + core.lower()
    return value


def lowercase_xml(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False
    for el in root.iter():
        for attr, val in el.attrib.items():
            new_val = _to_lower_hex(val)
            if new_val != val:
                el.set(attr, new_val)
                changed = True
    if changed:
        tree.write(path, encoding="utf-8", xml_declaration=True)


def _recurse_json(obj):
    if isinstance(obj, dict):
        return {k: _recurse_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_recurse_json(v) for v in obj]
    if isinstance(obj, str):
        return _to_lower_hex(obj)
    return obj


def lowercase_json(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    new_data = _recurse_json(data)
    if new_data != data:
        path.write_text(
            json.dumps(new_data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        lowercase_xml(Path(sys.argv[1]).expanduser().resolve())
    else:
        root_dir = Path(__file__).resolve().parent.parent
        lowercase_xml(root_dir / "resources" / "Helsing.xml")
        lowercase_json(root_dir / "resources" / "Helsing.theme.json")
