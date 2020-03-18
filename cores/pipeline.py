" Single input single output stream binder"

from nmigen import *
import stream
from nmigen.hdl.rec import Layout
""" 
Connecting a pipeline together 
        m.d.comb += [
            self.morse.sink.connect(self.input.source),
            self.output.sink.connect(self.morse.source),
            self.blink.sink.connect(self.output.source),
        ]
"""

class Pipeline:
    def __init__(self,pipeline):
        if type(pipeline) != type([]):
            raise ValueError('must be list')
        " check the pipeline "
        for item in pipeline:
            if hasattr(item,'sink'):
                print(item.sink)


class Widget(Elaboratable):
    " testing widget for pipeline builds " 

    def __init__(self,layout):
        self.sink = stream.StreamSink(layout)
        self.source = stream.StreamSource(layout)

    def elaborate(self,platform):
        m = Module()
        m.submodules.sink = self.sink
        m.submodules.source = self.source 

        return m


if __name__ == "__main__":
    print("pipeline test")
    layout = Layout([("data", 8),("stuff",4),("enable",1)])
    w1 = Widget(layout)
    w2 = Widget(layout)
    w3 = Widget(layout)
    p = Pipeline([w1,w2,w3])

