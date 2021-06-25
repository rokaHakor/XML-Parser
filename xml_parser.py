import re
import xml.etree.ElementTree as ET


def get_namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def parse_text(root, namespace):
    block = []
    for item in root.findall('.//' + namespace + 'formatting'):
        if item.text:
            block.append(item.text)
    return block


def find_text(text_list, text):
    for index, value in enumerate(text_list):
        if text in value:
            return index


def find_text_reverse(text_list, text, start_index):
    for index in range(start_index, -1, -1):
        if text in text_list[index]:
            return index


def find_vs(text_list, defend_index):
    for index in range(defend_index, -1, -1):
        if re.search('[Vv][Ss]{0,1}\.', text_list[index]):
            return index


def find_defendant(text_list, start, end):
    text = ''
    for index in range(start, end + 1):
        if ',' in text_list[index] and len(text_list[index]) > 3:
            text += text_list[index] + '\n'
    return text


def find_plaintiff(text_list, start):
    for index in range(start - 1, -1, -1):
        if ',' in text_list[index] and len(text_list[index]) > 3:
            return text_list[index]


def parse_xml(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    namespace = get_namespace(root)
    parse_list = parse_text(root, namespace)
    defend_index = find_text(parse_list, 'Defendant')
    vs_index = find_vs(parse_list, defend_index)
    plaint_index = find_text_reverse(parse_list, 'Plaintiff,', vs_index)
    plaintiff = find_plaintiff(parse_list, plaint_index).strip()
    defendant = find_defendant(parse_list, vs_index, defend_index).strip()
    return {'Plaintiff': plaintiff, 'Defendant': defendant}
