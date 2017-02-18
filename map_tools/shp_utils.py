import shapefile


def find_start_line(shape_file):
    """
    Finds the starting line segment in a shape file
    """
    reader = shapefile.Reader(shape_file)
    start_line = None
    lines = len(reader.shapes())
    for shapeIdx in range(0, lines):
        shape = reader.shapes()[shapeIdx]
        if len(shape.points) == 0:
            continue
        lng, lat = shape.points[0]
        found_next_line = False
        for shape2 in [s for s in reader.shapes() if len(s.points) > 0]:
            lng2, lat2 = shape2.points[-1]
            if lng == lng2 and lat == lat2:
                found_next_line = True
                break
        if not found_next_line:
            start_line = shapeIdx
            print "Start line index is", start_line
    return start_line
