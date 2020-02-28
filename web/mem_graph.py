import svgwrite
CSS_STYLES = """
    .background { fill: lavenderblush; }
    .line { stroke: firebrick; stroke-width: .1mm; }
    .blacksquare { fill: indigo; }
    .whitesquare { fill: hotpink; }
"""
def get_mem(mem):
    d = svgwrite.Drawing()
    # add stuff
    d.defs.add(d.style(CSS_STYLES))
    for i in range(40):
        d.add(d.rect(insert=(21*i,10),size=(20,20),class_="whitesquare"))

    return d.tostring()

