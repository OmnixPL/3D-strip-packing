from box import Box


def levels_algorithm(outer_box, inner_boxes):
    for i in range(len(inner_boxes)):   # rotate boxes
        z = max(inner_boxes[i].x, inner_boxes[i].y, inner_boxes[i].z)        # z in box is always longest
        x = min(inner_boxes[i].x, inner_boxes[i].y, inner_boxes[i].z)        # x in box is always shortest
        y = (inner_boxes[i].x + inner_boxes[i].y + inner_boxes[i].z) - z - x # y is always middle
        inner_boxes[i] = Box(x, y, z)
    inner_sorted = sorted(inner_boxes, key=lambda x: x.z, reverse=True)  # sort boxes by max height

    # TODO debug
    for box in inner_sorted:
        print(box.x, box.y, box.z)

    if outer_box.x < outer_box.y:   # from now on we assume x >= y
        outer_box.x, outer_box.y = outer_box.y, outer_box.x

    heightZ = 0
    while inner_sorted:
        box = inner_sorted.pop(0)
        heightZ += box.z                # this whole level has height of biggest box
        levels2D = [[box.x, box.y]]     # holds 2D levels, currently one, that has height of y(unchangeable) and used width of x (gets filled)
        leftY = outer_box.y - levels2D[0][1]
        remaining = []

        for box_i in range(len(inner_sorted)):
            box = inner_sorted[box_i]
            used = False
            for lvl_i in range(len(levels2D)):      # try to fit in existing box
                if box.y <= levels2D[lvl_i][1]:     # fits on Y axis
                    if box.x <= outer_box.x - levels2D[lvl_i][0]:  # fits on X axis
                        levels2D[lvl_i][0] += box.x        # use up some x space
                        used = True
                        break                           # stop fitting levels

            if used is False:                       # try to create new level
                if box.y > leftY:                   # this box doesnt fit in this 2D level
                    remaining.append(box)
                    continue
                levels2D.append([box.x, box.y])
                leftY -= box.y

        inner_sorted = remaining

    return heightZ;


def simple_algorithm(outer_box, inner_boxes):
    total_height = 0
    for box in inner_boxes:
        height = min(box.x, box.y, box.z)
        total_height += height      # one box per level so two other dimensions are ignorable
    return total_height;


def list_algorithm(outer_box, inner_boxes):
    return 3;