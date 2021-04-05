"""Data manipulation helpers"""

import os.path
import pickle
from cirtorch.datasets.datahelpers import cid2filename
from cirtorch.datasets.testdataset import configdataset

# images = []
# qimages = []
# bbxs = []
# gnd = []

def load_dataset(dataset, data_root=''):
    """Return tuple (image list, query list, bounding boxes, gnd dictionary)"""

    if dataset == 'mitsubishi_dataset':
        global images
        global qimages
        global bbxs
        global gnd
        cfg = configdataset()
        images = [cfg['im_fname'](cfg, i) for i in range(cfg['n'])]
        qimages = [cfg['qim_fname'](cfg, i) for i in range(cfg['nq'])]
               
        if 'bbx' in cfg['gnd'][0].keys():
            #cfg['gnd']=[{'bbx':'','xx':''},{},...{}]
            bbxs = [tuple(cfg['gnd'][i]['bbx']) for i in range(cfg['nq'])]
        else:
            bbxs = None
        gnd=cfg['gnd']
    return images, qimages, bbxs, gnd
images, qimages, bbxs, gnd =load_dataset('mitsubishi_dataset', data_root='')
#breakpoint()

class AverageMeter:
    """Compute and store the average and last value"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        """Update the counter by a new value"""
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
