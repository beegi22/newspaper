def doIntersect(line_hor, line_ver):
    # Hewtee bolon Bosoo zuraasuud ogtloltsoj baigaa esehiig shalgana
    flag1 = line_ver[0] > line_hor[0] and line_ver[0] < line_hor[2]
    flag2 = line_ver[1] < line_hor[1] and line_ver[3] > line_hor[1]
    if flag1 and flag2:
        return (int(line_ver[0]), int(line_hor[1]))
    return False


def article_lines(vertical, horizontal, h, w):
    # Article-n zuraasiig ylgaj awna
    horizontal_lines = []
    vertical_lines = []
    for line_hor in horizontal:
        width = line_hor[2] - line_hor[0]
        urt = False
        if width >= w * 0.5:
            urt = False
        if width > w * 0.4:
            width *= 0.3
        else:
            width *= 0.7
        x1 = line_hor[0] - width
        x2 = line_hor[2] + width
        if x1 < 0:
            x1 = 0
        if x2 > w:
            x2 = w
        points = []
        for line_ver in vertical:
            height = line_ver[3] - line_ver[1]
            if height > h * 0.4:
                height *= 0.3
            else:
                height *= 0.7
            y1 = line_ver[1] - height
            y2 = line_ver[3] + height
            if y1 < 0:
                y1 = 0
            flag = doIntersect([x1, line_hor[1], x2, line_hor[3]], [line_ver[0], y1, line_ver[2], y2])
            if flag:
                points.append(flag)
        if urt and (points or x1 == 0 or x2 == w):
            min_y = 0
            max_y = h
            left_flag = True
            right_flag = True
            for point in points:
                if line_hor[0] > point[0] and x1 < point[0]:
                    x1 = point[0]
                    left_flag = False
                elif line_hor[2] < point[0] and x2 > point[0]:
                    right_flag = False
                    x2 = point[0]
            if left_flag and x1 != 0:
                for temp in horizontal:
                    if temp[0] < line_hor[0] and temp[2] > line_hor[0]:
                        if temp[1] < line_hor[1] and min_y < temp[1]:
                            min_y = temp[1]
                        if temp[1] > line_hor[1] and max_y > temp[1]:
                            max_y = temp[1]
                vertical.append([line_hor[0], min_y, line_hor[0], max_y])
                x1 = line_hor[0]
            min_y = 0
            max_y = h
            if right_flag and x2 != w:
                for temp in horizontal:
                    if temp[0] < line_hor[2] and temp[2] > line_hor[2]:
                        if temp[1] < line_hor[1] and min_y < temp[1]:
                            min_y = temp[1]
                        if temp[1] > line_hor[1] and max_y > temp[1]:
                            max_y = temp[1]
                vertical.append([line_hor[2], min_y, line_hor[2], max_y])
                x2 = line_hor[2]
            horizontal_lines.append([[int(x1), int(line_hor[1]), int(x2), int(line_hor[1])], points])
        elif points and (x1 == 0 or x2 == w):
            # x1 = 0
            # x2 = w
            flag_x1 = True
            flag_x2 = True
            for point in points:
                if line_hor[0] > point[0] and x1 < point[0]:
                    x1 = point[0]
                    flag_x1 = False
                elif line_hor[2] < point[0] and x2 > point[0]:
                    x2 = point[0]
                    flag_x2 = False
            if flag_x1 and x1 != 0:
                x1 = line_hor[0]
            if flag_x2 and x2 != w:
                x2 = line_hor[2]
            horizontal_lines.append([[int(x1), int(line_hor[1]), int(x2), int(line_hor[1])], points])
        elif x1 == 0 and x2 == w:
            horizontal_lines.append([[0, int(line_hor[1]), int(w), int(line_hor[1])], []])
    for line_ver in vertical:
        height = line_ver[3] - line_ver[1]
        urt = False
        if height >= h * 0.5:
            urt = False
        if height > h * 0.4:
            height *= 0.3
        else:
            height *= 0.7
        y1 = line_ver[1] - height
        y2 = line_ver[3] + height
        if y1 < 0:
            y1 = 0
        if y2 > h:
            y2 = h
        flag = False
        points = []
        for temp in horizontal_lines:
            line_hor = temp[0]
            width = line_hor[2] - line_hor[0]
            if width > w * 0.4:
                width *= 0.3
            else:
                width *= 0.7
            x1 = line_hor[0] - width
            x2 = line_hor[2] + width
            if x1 < 0:
                x1 = 0
            flag = doIntersect([x1, line_hor[1], x2, line_hor[3]], [line_ver[0], y1, line_ver[2], y2])
            if flag:
                points.append(flag)
        if urt and (points or y1 == 0 or y2 == h):
            min_x = 0
            max_x = w
            down_flag = True
            up_flag = True
            for point in points:
                if line_ver[1] > point[1] and y1 < point[1]:
                    y1 = point[1]
                    up_flag = False
                elif line_ver[3] < point[1] and y2 > point[1]:
                    y2 = point[1]
                    down_flag = False
            if up_flag and y1 != 0:
                for temp in vertical:
                    if temp[1] < line_ver[1] and temp[3] > line_ver[1]:
                        if temp[0] < line_ver[0] and min_x < temp[0]:
                            min_x = temp[0]
                        if temp[0] > line_ver[0] and max_x > temp[0]:
                            max_x = temp[0]
                horizontal_lines.append([[int(min_x), int(line_ver[1]), int(max_x), int(line_ver[1])], []])
                y1 = line_ver[1]
            min_x = 0
            max_x = w
            if down_flag and y2 != h:
                for temp in vertical:
                    if temp[1] < line_ver[3] and temp[3] > line_ver[3]:
                        if temp[0] < line_ver[0] and min_x < temp[0]:
                            min_x = temp[0]
                        if temp[0] > line_ver[0] and max_x > temp[0]:
                            max_y = temp[0]
                horizontal_lines.append([[int(min_x), int(line_ver[3]), int(max_x), int(line_ver[3])], []])
                y2 = line_ver[3]
            vertical_lines.append([[int(line_ver[0]), int(y1), int(line_ver[0]), int(y2)], points])
        elif points and (y1 == 0 or y2 == h):
            # y1 = 0
            # y2 = h
            flag_y1 = True
            flag_y2 = True
            for point in points:
                if line_ver[1] > point[1] and y1 < point[1]:
                    y1 = point[1]
                    flag_y1 = False
                elif line_ver[3] < point[1] and y2 > point[1]:
                    y2 = point[1]
                    flag_y2 = False
            if flag_y1 and y1 != 0:
                y1 = line_ver[1]
            if flag_y2 and y2 != h:
                y2 = line_ver[3]
            vertical_lines.append([[int(line_ver[0]), int(y1), int(line_ver[0]), int(y2)], points])
        elif y1 == 0 and y2 >= h:
            vertical_lines.append([[int(line_ver[0]), 0, int(line_ver[0]), int(h)], []])
    return horizontal_lines, vertical_lines
