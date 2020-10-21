def reading_order(articles):
    length = len(articles)
    sorted_article = []
    titles = []
    img = []
    img_text = []
    start = []
    for i in range(length):
        block = articles.pop(0)
        if block['type'] != 0:
            img.append(block)
            continue
        flag = True
        for line in block['lines']:
            if line['spans'][0]['size'] < 18:
                flag = False
                break
        if flag and block['lines'][0]['spans'][0]['color'] == 0:
            titles.append(block)
        else:
            articles.append(block)
    length = len(articles)
    for i in range(length):
        block = articles.pop(0)
        if block['lines'][0]['spans'][0]['size'] < 9 and block['lines'][0]['spans'][0]['font'] != "PoynterGothicText-BoldCond":
            img_text.append(block)
        elif block['lines'][0]['spans'][0]['color'] == 6909551 and block['lines'][0]['spans'][0]['size'] > 13:
            titles.append(block)
        else:
            articles.append(block)
    for title in titles:
        sorted_article.append(title)
    for text in img_text:
        min_dist = text['bbox'][3]
        index = -1
        for i, img_block in enumerate(img):
            if min(text['bbox'][2], img_block['bbox'][2]) - max(text['bbox'][0], img_block['bbox'][0]) > 0:
                dist = text['bbox'][3] - img_block['bbox'][3]
                if min_dist > dist and dist > 0:
                    min_dist = dist
                    index = i
            if min(text['bbox'][3], img_block['bbox'][3]) - max(text['bbox'][1], img_block['bbox'][1]) > 0:
                dist = text['bbox'][2] - img_block['bbox'][2]
                if min_dist > dist and dist > 0:
                    min_dist = dist
                    index = i
        if index == -1:
            start.append(text)
            continue
        sorted_article.append(img.pop(index))
        sorted_article.append(text)
    for img_block in img:
        sorted_article.append(img_block)
    for text in start:
        sorted_article.append(text)
    for article in articles:
        sorted_article.append(article)
    return sorted_article
