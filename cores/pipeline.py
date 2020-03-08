" Single input single output stream binder"

from nmigen import *
import stream

class Pipeline:
    def __init__(self,pipeline):
        if type(pipeline) != type([]):
            raise ValueError('must be list')
        for i in pipeline:
            print(i)

if __name__ == "__main__":
    print("pipeline")
