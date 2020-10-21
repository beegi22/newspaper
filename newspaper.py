import cv2
import fitz
import sys
import json
import time
from pdf2image import convert_from_path
from newspaper_order import reading_order
from Article_lines import article_lines


def bbox_compare(bbox1, bbox2, value):
    # 2 box dawhtssan esehiig shalgah
    width = min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0])
    height = min(bbox1[3] + value, bbox2[3] + value) - max(bbox1[1], bbox2[1])
    if width <= 0 or height <= 0:
        return False
    else:
        return True


def bbox_compare_area(bbox1, bbox2):
    # 2 box dawhtsaliin talbaig olno.
    width = min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0])
    height = min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1])
    if width <= 0 or height <= 0:
        return 0.0
    area = width * height
    bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    area_percent = area / bbox1_area
    return area_percent


def text_line_segment(input_blocks):
    # text block-g line-r salgana
    blocks = []
    for number, block in enumerate(input_blocks):
        if block['type'] != 0:
            blocks.append(block)
            continue
        for line in block['lines']:
            flag = ""
            for text in line['spans']:
                flag += text["text"]
                flag = flag.replace(" ", "")
                if flag != "":
                    break
            if flag == "":
                continue
            blocks.append({'type': 0, 'bbox': line['bbox'], 'lines': [line], 'block_number': number})
    return blocks


def para_segment(blocks):
    # text blockuudiig paragraph-r ni niiluulne
    output_blocks = []
    output_blocks.append(blocks[0])
    for i in range(1, len(blocks)):
        if blocks[i]['type'] != 0 or output_blocks[-1]['type'] != 0:
            output_blocks.append(blocks[i])
            continue
        if bbox_compare(output_blocks[-1]['bbox'], blocks[i]['bbox'], 5):
            output_blocks[-1]['bbox'][0] = min(output_blocks[-1]['bbox'][0], blocks[i]['bbox'][0])
            output_blocks[-1]['bbox'][2] = max(output_blocks[-1]['bbox'][2], blocks[i]['bbox'][2])
            output_blocks[-1]['bbox'][3] = blocks[i]['bbox'][3]
            output_blocks[-1]['lines'] += blocks[i]['lines']
        else:
            output_blocks.append(blocks[i])
    return output_blocks


def line_detection(img):
    # Zurgaas zuraas ilruulne
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 150))

    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    cnts = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_vertical = cnts[0] if len(cnts) == 2 else cnts[1]

    cnts = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_horizontal = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts_vertical, cnts_horizontal


def remove_lines(bboxs, cnts_vertical, cnts_horizontal, ratio_w, ratio_h):
    # hereggui zuraasiig hasna (contenttoi dawhtsaj bui zuraasuudiig hasna)
    vertical_lines = []
    horizontal_lines = []
    for line_bbox in cnts_vertical:
        line_bbox = cv2.boundingRect(line_bbox)
        flag = True
        for bbox in bboxs:
            bbox2 = [line_bbox[0], line_bbox[1], line_bbox[0] + line_bbox[2], line_bbox[1] + line_bbox[3]]
            if bbox_compare(bbox, bbox2, 0):
                flag = False
                break
        if flag:
            line = [line_bbox[0] / ratio_w, line_bbox[1] / ratio_h, line_bbox[0] / ratio_w, (line_bbox[1] + line_bbox[3]) / ratio_h]
            vertical_lines.append(line)

    for line_bbox in cnts_horizontal:
        line_bbox = cv2.boundingRect(line_bbox)
        flag = True
        for bbox in bboxs:
            bbox2 = [line_bbox[0], line_bbox[1], line_bbox[0] + line_bbox[2], line_bbox[1] + line_bbox[3]]
            if bbox_compare(bbox, bbox2, 0):
                flag = False
                break
        if flag:
            line = [line_bbox[0] / ratio_w, line_bbox[1] / ratio_h, (line_bbox[0] + line_bbox[2]) / ratio_w, line_bbox[1] / ratio_h]
            horizontal_lines.append(line)
    return vertical_lines, horizontal_lines


def bboxs_sort(bboxs):
    # bbox uudiig talbaigaar ni sortlono.
    area = []
    for index, bbox in enumerate(bboxs):
        area.append(((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]), index))
    area.sort()
    bbox_sorted = []
    for index in area:
        bbox_sorted.append(bboxs[index[1]])
    return bbox_sorted


def combine_blocks(blocks):
    # blockuudiig pdf-n ugugdsun anhnii tom bbox-r negtgesenii daraa paragraphaar negtgene.
    block_numbers = {}
    output_blocks = []
    for block in blocks:
        if block.get('block_number') is None:
            output_blocks.append(block)
            continue
        if block_numbers.get(block['block_number']):
            block_numbers[block['block_number']].append(block)
        else:
            block_numbers[block['block_number']] = []
            block_numbers[block['block_number']].append(block)
    for key in block_numbers:
        temp = {'type': block_numbers[key][0]['type'], 'bbox': block_numbers[key][0]['bbox'], 'lines': []}
        for block in block_numbers[key]:
            temp['bbox'][0] = min(temp['bbox'][0], block['bbox'][0])
            temp['bbox'][2] = max(temp['bbox'][2], block['bbox'][2])
            temp['bbox'][1] = min(temp['bbox'][1], block['bbox'][1])
            temp['bbox'][3] = max(temp['bbox'][3], block['bbox'][3])
            temp['lines'] += block['lines']
        output_blocks.append(temp)
    output_blocks = para_segment(output_blocks)
    return output_blocks


print("Started")
total_time = time.time()
start_time = time.time()
ifile = sys.argv[1]
pages = convert_from_path(ifile)
doc = fitz.Document(ifile)
print("Pdf-loaded: " + str(time.time() - start_time))
for number, page in enumerate(pages):
    start_time = time.time()
    data = []
    page.save('out.jpg', 'JPEG')
    page_img = cv2.imread('out.jpg')
    page_content = json.loads(doc[number].getText('json'))
    ratio_w = page_img.shape[1] / page_content['width']
    ratio_h = page_img.shape[0] / page_content['height']
    output_blocks = text_line_segment(page_content["blocks"])
    height = int(page_content['height'])
    width = int(page_content['width'])
    bboxs = []
    for block in output_blocks:
        bbox = block['bbox']
        if block['type'] != 0:
            value = 0
            bboxs.append([bbox[0] * ratio_w, bbox[1] * ratio_h, bbox[2] * ratio_w, bbox[3] * ratio_h])
        else:
            value = 5
            if block['lines'][0]['spans'][0]['size'] >= 30:
                value = 15
            bboxs.append([bbox[0] * ratio_w + value, bbox[1] * ratio_h + value, bbox[2] * ratio_w - value, bbox[3] * ratio_h - value])
    cnts_vertical, cnts_horizontal = line_detection(page_img)
    vertical_lines, horizontal_lines = remove_lines(bboxs, cnts_vertical, cnts_horizontal, ratio_w, ratio_h)
    vertical_lines, horizontal_lines = article_lines(vertical_lines, horizontal_lines, height, width)
    points_x = set()
    points_x.update([(0, 0), (0, height), (width, height), (width, 0)])
    for h_line in horizontal_lines:
        points_x.add((h_line[0][0], h_line[0][1]))
        points_x.add((h_line[0][2], h_line[0][3]))
        for point in h_line[1]:
            points_x.add((point[0], point[1]))
    for v_line in vertical_lines:
        points_x.add((v_line[0][0], v_line[0][1]))
        points_x.add((v_line[0][2], v_line[0][3]))
        for point in v_line[1]:
            points_x.add((point[0], point[1]))
    points_x = sorted(points_x)
    points_x = list(points_x)
    bboxs_article = set()
    for index, point_start in enumerate(points_x):
        down = []
        for j in range(index + 1, len(points_x)):
            if points_x[j][0] != point_start[0]:
                break
            down.append(points_x[j])
        right = []
        for point in down:
            for x in points_x:
                if x[1] == point[1] and point[0] < x[0]:
                    right.append(x)
        for point in right:
            for x in points_x:
                if x[0] == point[0] and x[1] == point_start[1]:
                    bboxs_article.add((point_start[0], point_start[1], point[0], point[1]))
    bboxs_article = bboxs_sort(list(bboxs_article))
    articles = []
    for bbox in bboxs_article:
        article = []
        length = len(output_blocks)
        for i in range(length):
            block = output_blocks.pop(0)
            if bbox_compare_area(block['bbox'], bbox) >= 0.5:
                article.append(block)
            else:
                output_blocks.append(block)
        if len(article) > 0:
            articles.append((article, bbox))
        if len(output_blocks) == 0:
            break
    for j, article in enumerate(articles):
        bbox = article[1]
        blocks = combine_blocks(article[0])
        sorted_article = reading_order(blocks)
        data.append({'article_box': article[1], 'text': sorted_article})
        i = j + 1
        page_img = cv2.rectangle(page_img, (int(bbox[0] * ratio_w) + 10, int(bbox[1] * ratio_h) + 10), (int(bbox[2] * ratio_w) - 10, int(bbox[3] * ratio_h) - 10), (25 * i, 50 * i, 10 * i), 3)
        page_img = cv2.putText(page_img, str(i), (int(bbox[0] * ratio_w) + 20, int(bbox[1] * ratio_h) + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)
        for num, text in enumerate(sorted_article):
            bbox = text['bbox']
            page_img = cv2.rectangle(page_img, (int(bbox[0] * ratio_w), int(bbox[1] * ratio_h)), (int(bbox[2] * ratio_w), int(bbox[3] * ratio_h)), (25 * i, 50 * i, 10 * i), 3)
            page_img = cv2.putText(page_img, str(num + 1), (int(bbox[0] * ratio_w) + 20, int(bbox[1] * ratio_h) + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.imwrite('Output/Page_' + str(number + 1) + '.png', page_img)
    with open('Output/Page_' + str(number + 1) + '.json', 'w') as outfile:
        json.dump(data, outfile)
    print("Page-" + str(number + 1) + "-loaded: " + str(time.time() - start_time))
print("Done: " + str(time.time() - total_time))
