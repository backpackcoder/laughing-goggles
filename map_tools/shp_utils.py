import shapefile
from geopy.distance import vincenty


def find_start_line(shape_file):
    """
    Finds the starting line segment in a shape file
    """
    reader = shapefile.Reader(shape_file)
    orig_recs = [sr for sr in reader.shapeRecords() if len(sr.shape.points) > 0]
    bad_recs = []
    rec = orig_recs.pop()
    start_pt = rec.shape.points[0]
    end_pt = rec.shape.points[-1]
    tolerance = 0.00001  # in meters
    recs = [rec]
    current_len = len(orig_recs)
    attempts = 0
    while current_len > 0:
        # See if we can find next segment best chance is previous index
        rec = orig_recs.pop()
        d_end_start = vincenty(start_pt, rec.shape.points[-1]).meters
        d_start_end = vincenty(end_pt, rec.shape.points[0]).meters
        d_start_start = vincenty(start_pt, rec.shape.points[0]).meters
        d_end_end = vincenty(end_pt, rec.shape.points[-1]).meters

        # check if rec end point connects to start point
        if d_end_start <= tolerance:
            recs.insert(0, rec)
            start_pt = rec.shape.points[0]
            attempts = 0
            tolerance = 0
        # check if rec start point connects to end point
        elif d_start_end <= tolerance:
            recs.append(rec)
            end_pt = rec.shape.points[-1]
            attempts = 0
            tolerance = 0
        # check if rec start point connect to start point
        elif d_start_start <= tolerance:
            rec.shape.points.reverse()
            recs.insert(0, rec)
            start_pt = rec.shape.points[0]
            attempts = 0
            tolerance = 0
        # check if rec end point connects to end point
        elif d_end_end <= tolerance:
            rec.shape.points.reverse()
            recs.append(rec)
            end_pt = rec.shape.points[-1]
            attempts = 0
            tolerance = 0
        else:
            orig_recs.insert(0, rec)
            if attempts == current_len:
                if tolerance < 1:
                    tolerance = 1
                elif tolerance == 1:
                    tolerance = 20
                else:
                    tolerance += 10
                attempts = 0
                if tolerance > 20:
                    orig_recs.remove(rec)
                    print "Removing record"
                    attempts = 0
                    tolerance = 0
                    bad_recs.append(rec)
            attempts += 1

        if current_len != len(orig_recs):
            print "Current record count", current_len
        current_len = len(orig_recs)

    js_str = 'var line = ['
    for r in recs:
        for pt in r.shape.points:
            js_str += 'new L.LatLng(' + str(pt[1]) + ', ' \
                      + str(pt[0]) + '),'
            # We only want fields 2, 26, and 28
            # print r.record[26], r.record[28]
    js_str = js_str[:-1] + '];'

    print len(bad_recs), 'bad records'
    for idx in range(0, len(bad_recs)):
        js_str += 'var line' + str(idx + 1) + ' = ['
        for pt in bad_recs[idx].shape.points:
            js_str += 'new L.LatLng(' + str(pt[1]) + ', ' \
                      + str(pt[0]) + '),'
        js_str = js_str[:-1] + '];'

    js_file = open('../node_modules/leaflet/dist/line.js', 'w')
    js_file.write(js_str)
    js_file.close()
