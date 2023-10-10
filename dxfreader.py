import sys
import ezdxf
import math

try:
    my_file = ezdxf.readfile("testreader.dxf")
    msp = my_file.modelspace()

    def longitude(start, end):
        return (math.dist(start, end), 2)

    def print_entity(e):
        print("LINE on layer: %s\n" % e.dxf.layer)
        print("start point: %s\n" % e.dxf.start)
        print("end point: %s\n" % e.dxf.end)
        print("lenght: %s\n" % str(longitude(e.dxf.start, e.dxf.end)))

    for e in msp:
        if e.dxftype() == "LINE":
            print_entity(e)
    
    for e in msp.query("LINE"):
        print_entity(e)

except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    sys.exit(2)
