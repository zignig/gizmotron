import svgwrite
CSS_STYLES = """
    .background { fill: lavenderblush; }
    .line { stroke: firebrick; stroke-width: .1mm; }
    .blacksquare { fill: indigo; }
    .whitesquare { fill: skyblue ; stroke: black ; stroke-width: 0.2px ; transition: fill 1s ;}
    .whitesquare:hover { fill: green ; } 
    .blocklabel { font-size: 0.9em ; alignment-baseline: middle ; font-weight: bold ; fill: red ; }
"""
def get_mem(mem,width=32,size=20):
    d = svgwrite.Drawing()
    # add stuff
    d.defs.add(d.style(CSS_STYLES))
    y = 0 
    for i in range(64):
        d.add(d.rect(insert=(21*i,10),size=(20,20),class_="whitesquare"))
        d.add(d.text("R",insert=(21*i+size/4,20+size/4),class_="blocklabel"))

    return d.tostring()


def signal(sig):
    d = svgwrite.Drawing()
    return d.tostring()
 
