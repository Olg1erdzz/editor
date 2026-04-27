from bs4 import BeautifulSoup
import re


def get_prefix_format(text):
    prefix = ''
    for char in text:
        if re.match(r'\d|\.|、|\)|\(|一|二|三|四|五|六|七|八|九|十|（|）', char):
            prefix += char
        else:
            break
    prefix_format = re.sub(r'\d', 'N', prefix)
    prefix_format = re.sub(r'一|二|三|四|五|六|七|八|九|十', '*', prefix_format)
    return prefix_format


def split_paragraphs(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    p_tags = soup.find_all(['p', 'h1'])
    paragraphs = []
    heading_formats = {}
    counter = 1  # 初始化计数器
    for p in p_tags:
        text = p.get_text().strip()
        label = ''
        if text:
            if p.name == 'h1':
                label = 'Title'
            elif p.name == 'p' and (re.match(r'^(\d+|一|二|三|四|五|六|七|八|九|十).*(\.){7,}\d+$', text) or re.match(r'.*[\u4e00-\u9fa5]\s*(\.){7,}\d+$', text)):
                label = 'Tables'
            elif p.name == 'p' and (re.match(r'^(图|表)\s*(\d+|一|二|三|四|五|六|七|八|九|十)\s*[^\d]*\s*(\d+)*\s*.*$', text) or re.match(r'^(图|表)\s*(\d+|一|二|三|四|五|六|七|八|九|十)\s*.*$', text) or re.match(r'^(图|表)\s*(\d+|一|二|三|四|五|六|七|八|九|十)\s', text)):
                label = 'Caption'
            # elif p.name == 'p' and text.startswith('注释'):
            #     break
            elif p.name == 'p' and len(text) >= 50 and text.endswith('。'):
                prefix_format = get_prefix_format(text)
                if prefix_format:
                    break
                else:
                    label = 'Body'
            elif p.name == 'p':
                prefix_format = get_prefix_format(text)
                if prefix_format and not (text.endswith('。')):
                    if 'Heading 1' not in heading_formats:
                        heading_formats['Heading 1'] = prefix_format
                        label = 'Heading 1'
                    elif prefix_format != heading_formats['Heading 1']:
                        if 'Heading 2' not in heading_formats:
                            heading_formats['Heading 2'] = prefix_format
                            label = 'Heading 2'
                        elif prefix_format != heading_formats['Heading 2']:
                            label = 'Heading 3'
                        else:
                            label = 'Heading 2'
                    else:
                        label = 'Heading 1'
                # elif prefix_format and text.endswith('。'):
                #     if 'List' not in heading_formats:
                #         heading_formats['List'] = prefix_format
                #         label = 'List'
                #     elif prefix_format == heading_formats['List']:
                #         label = 'List'
                elif re.match(r'^\[\d+\]', text):
                    label = 'Quote'
                else:
                    label = 'Body'
            paragraphs.append((text, label))
            counter += 1
    return paragraphs

