from . import BBox
class SampleImage():
    def __init__(self, filePath:str):
        self.filePath = filePath
        self.name = filePath.split('/')[-1].split('.')[0]
        self.BBox = []

    def AddBBox(self,bbox:BBox):
        self.BBox.append(bbox)
        return

