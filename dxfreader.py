import sys
import ezdxf
import math

try:
    my_file = ezdxf.readfile("test.dxf")
    msp = my_file.modelspace()
    total_length = 0

    def get_lenght(start, end):
        return (math.dist(start, end), 2)

    def print_entity(e):
        global total_length
        total_length += get_lenght(e.dxf.start, e.dxf.end)[0]
        print("lenght: %s\n" % str(get_lenght(e.dxf.start, e.dxf.end)))

    for e in msp:
        if e.dxftype() == "LINE":
            print_entity(e)
    for e in msp.query("LINE"):
        print_entity(e)

    print("Total length: ", total_length)

except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    sys.exit(2)

