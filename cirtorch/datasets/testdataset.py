import os
import pickle
import os
import sys
#sys.path.append(os.path.realpath(f"{__file__}/../"))
from cirtorch.utils.download import download_test

DATASETS = ['mitsubishi_dataset']

def configdataset():

    #dataset = dataset.lower()

    # if dataset not in DATASETS:    
    #     raise ValueError('Unknown dataset: {}!'.format(dataset))

    # loading imlist, qimlist, and gnd, in cfg as a dict
    #dataset's path
    #gnd_fname = os.path.join(dir_main, dataset, 'gnd_{}.pkl'.format(dataset))
    # gnd_fname = os.path.join(dir_main, dataset, 'gnd_{}.pkl'.format(dataset))
    # with open(gnd_fname, 'rb') as f:
    #     cfg = pickle.load(f)
    # cfg['gnd_fname'] = gnd_fname
    cfg=download_test()
    # cfg['ext'] = '.jpg'
    # cfg['qext'] = '.jpg'
    #cfg['dir_data'] = os.path.join(dir_main, dataset)
    cfg['dir_images'] = cfg['png_file']
    cfg['gnd']=cfg['l_file']
    cfg['n'] = len(cfg['imlist'])
    cfg['nq'] = len(cfg['qimlist'])
#file path
    cfg['im_fname'] = config_imname
    cfg['qim_fname'] = config_qimname

    return cfg
#cfg=configdataset()
#breakpoint()

def config_imname(cfg, i):
    return cfg['imlist'][i]

def config_qimname(cfg, i):
    return cfg['qimlist'][i]
cfg=configdataset()
#breakpoint()

'''
DATASETS = ['oxford5k', 'paris6k', 'roxford5k', 'rparis6k']

def configdataset(dataset, dir_main):

    dataset = dataset.lower()

    if dataset not in DATASETS:    
        raise ValueError('Unknown dataset: {}!'.format(dataset))

    # loading imlist, qimlist, and gnd, in cfg as a dict
    gnd_fname = os.path.join(dir_main, dataset, 'gnd_{}.pkl'.format(dataset))
    with open(gnd_fname, 'rb') as f:
        cfg = pickle.load(f)
    cfg['gnd_fname'] = gnd_fname

    cfg['ext'] = '.jpg'
    cfg['qext'] = '.jpg'
    cfg['dir_data'] = os.path.join(dir_main, dataset)
    cfg['dir_images'] = os.path.join(cfg['dir_data'], 'jpg')

    cfg['n'] = len(cfg['imlist'])
    cfg['nq'] = len(cfg['qimlist'])

    cfg['im_fname'] = config_imname
    cfg['qim_fname'] = config_qimname

    cfg['dataset'] = dataset

    return cfg

def config_imname(cfg, i):
    return os.path.join(cfg['dir_images'], cfg['imlist'][i] + cfg['ext'])

def config_qimname(cfg, i):
    return os.path.join(cfg['dir_images'], cfg['qimlist'][i] + cfg['qext'])
'''