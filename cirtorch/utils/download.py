import os
import sys
#sys.path.append(os.path.realpath(f"{__file__}/../../"))
from cirtorch.utils import read_xml


def download_test():
    """
    DOWNLOAD_TEST Checks, and, if required, downloads the necessary datasets for the testing.
      
        download_test(DATA_ROOT) checks if the data necessary for running the example script exist.
        If not it downloads it in the folder structure:
            DATA_ROOT/test/oxford5k/  : folder with Oxford images and ground truth file
            DATA_ROOT/test/paris6k/   : folder with Paris images and ground truth file
            DATA_ROOT/test/roxford5k/ : folder with Oxford images and revisited ground truth file
            DATA_ROOT/test/rparis6k/  : folder with Paris images and revisited ground truth file
    """

    # Download datasets folders test/DATASETNAME/
    datasets = ['mitsubishi_dataset']
    cfg = {}
    dl=[]
    al=[]
    qil=[]
    il=[]
    for di in range(len(datasets)):
        dataset = datasets[di]

        if dataset == 'mitsubishi_dataset':
            src_dir = '/home/ubuntu/local/mitsubishi_dataset'
    #png and annotation
        for dir in os.listdir(src_dir):
            if dir == 'png_images':
                dir_path=os.path.join(src_dir, dir)
                for dir in os.listdir(dir_path):
                    ddir_path=os.path.join(dir_path,dir)
                    for file in os.listdir(ddir_path):
                        if '.dxf' in file:
                            continue
                        elif '.DS_Store' in file:
                            continue
                        else:
                            dst_dir = os.path.join(ddir_path,file)
                            dl.append(dst_dir)
                    
            elif dir == 'annotation':
                ldir_path=os.path.join(src_dir, dir)
                for d in os.listdir(ldir_path):
                    lldir_path=os.path.join(ldir_path, d)
                    for file in os.listdir(lldir_path):
                        if '.dxf' in file:
                            continue
                        elif '.DS_Store' in file:
                            continue
                        else:
                            l_dir = os.path.join(lldir_path,file)
                            al.append(l_dir)
                        #cfg['l_name'].append(file.split('.')[0])

        for i in range(len(dl)):
            #cfg['gnd']=[if dic_list['id'].values()==i]
            # cfg['png_name'].append(dst_dir.split('.')[0])
            if i%5 == 0:
                qil.append(dl[i])
                #cfg['qimg_name'].append(file.split('.')[0])
            else :
                il.append(dl[i])
                #cfg['img_name'].append(file.split('.')[0]) 
    cfg['png_file'] = dl
    cfg['l_file'] = read_xml.dic_list
    cfg['qimlist'] = qil
    cfg['imlist'] = il
    #breakpoint()
    return cfg
#cfg=download_test()
#breakpoint()
def download_train(data_dir):
    """
    DOWNLOAD_TRAIN Checks, and, if required, downloads the necessary datasets for the training.
      
        download_train(DATA_ROOT) checks if the data necessary for running the example script exist.
        If not it downloads it in the folder structure:
            DATA_ROOT/train/retrieval-SfM-120k/  : folder with rsfm120k images and db files
            DATA_ROOT/train/retrieval-SfM-30k/   : folder with rsfm30k images and db files
    """

    # Create data folder if it does not exist
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    
    # Create datasets folder if it does not exist
    datasets_dir = os.path.join(data_dir, 'train')
    if not os.path.isdir(datasets_dir):
        os.mkdir(datasets_dir)

    # Download folder train/retrieval-SfM-120k/
    src_dir = os.path.join('http://cmp.felk.cvut.cz/cnnimageretrieval/data', 'train', 'ims')
    dst_dir = os.path.join(datasets_dir, 'retrieval-SfM-120k', 'ims')
    dl_file = 'ims.tar.gz'
    if not os.path.isdir(dst_dir):
        src_file = os.path.join(src_dir, dl_file)
        dst_file = os.path.join(dst_dir, dl_file)
        print('>> Image directory does not exist. Creating: {}'.format(dst_dir))
        os.makedirs(dst_dir)
        print('>> Downloading ims.tar.gz...')
        os.system('wget {} -O {}'.format(src_file, dst_file))
        print('>> Extracting {}...'.format(dst_file))
        os.system('tar -zxf {} -C {}'.format(dst_file, dst_dir))
        print('>> Extracted, deleting {}...'.format(dst_file))
        os.system('rm {}'.format(dst_file))

    # Create symlink for train/retrieval-SfM-30k/ 
    dst_dir_old = os.path.join(datasets_dir, 'retrieval-SfM-120k', 'ims')
    dst_dir = os.path.join(datasets_dir, 'retrieval-SfM-30k', 'ims')
    if not os.path.isdir(dst_dir):
        os.makedirs(os.path.join(datasets_dir, 'retrieval-SfM-30k'))
        os.system('ln -s {} {}'.format(dst_dir_old, dst_dir))
        print('>> Created symbolic link from retrieval-SfM-120k/ims to retrieval-SfM-30k/ims')

    # Download db files
    src_dir = os.path.join('http://cmp.felk.cvut.cz/cnnimageretrieval/data', 'train', 'dbs')
    datasets = ['retrieval-SfM-120k', 'retrieval-SfM-30k']
    for dataset in datasets:
        dst_dir = os.path.join(datasets_dir, dataset)
        if dataset == 'retrieval-SfM-120k':
            dl_files = ['{}.pkl'.format(dataset), '{}-whiten.pkl'.format(dataset)]
        elif dataset == 'retrieval-SfM-30k':
            dl_files = ['{}-whiten.pkl'.format(dataset)]

        if not os.path.isdir(dst_dir):
            print('>> Dataset directory does not exist. Creating: {}'.format(dst_dir))
            os.mkdir(dst_dir)

        for i in range(len(dl_files)):
            src_file = os.path.join(src_dir, dl_files[i])
            dst_file = os.path.join(dst_dir, dl_files[i])
            if not os.path.isfile(dst_file):
                print('>> DB file {} does not exist. Downloading...'.format(dl_files[i]))
                os.system('wget {} -O {}'.format(src_file, dst_file))
