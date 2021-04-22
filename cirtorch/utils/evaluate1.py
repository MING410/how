import numpy as np
#ap = compute_ap(pos, len(qgnd))
def compute_ap(ranks, nres):
    """
    Computes average precision for given ranked indexes.
    
    Arguments
    ---------
    ranks : zerro-based ranks of positive images
    nres  : number of positive images
    
    Returns
    -------
    ap    : average precision
    """

    # number of images ranked by the system
    nimgranks = len(ranks)

    # accumulate trapezoids in PR-plot
    ap = 0
    if nres != 0:
        recall_step = 1. / nres
        for j in np.arange(nimgranks):
            rank = ranks[j]

            if rank == 0:
                precision_0 = 1.
            else:
                precision_0 = float(j) / rank

            precision_1 = float(j + 1) / (rank + 1)

            ap += (precision_0 + precision_1) * recall_step / 2.
    else:
        ap = 0
    return ap

def compute_map(ranks, qg,ig, kappas=[]):

    nmap = 0.
    map = 0.
    pos_num=0.
    npos=0.
    nq = len(qg) # number of queries
    aps = np.zeros(nq)
    num_array=np.zeros(nq)
    #pr = np.zeros(len(kappas))
    #prs = np.zeros((nq, len(kappas)))
    dic_evaluate={}
    debug_list=[]
    #i回目の検索
    #for i in range(nq):
    with open('debug_list_asmk.txt', 'a', encoding='utf-8') as f1:
        for i in range(nq):
            #qgnd = np.array(gnd[i]['ok'])
            qgnd = np.array(qg[i]['label'])
            #print(qgnd)

            #breakpoint()
            # sorted positions of positive and junk images (0 based)
            pos  = np.arange(ranks.shape[0])[np.in1d(ranks.iloc[:,i], qgnd)]
            #breakpoint()
            #junk = np.arange(ranks.shape[0])[np.in1d(ranks[:,i], qgndj)]

            # compute ap
            ap = compute_ap(pos, len(pos))
            nmap = nmap + ap
            #map=nmap/(i+1)
            aps[i] = ap
            #breakpoint()
            pos_num=len(pos)/10
            num_array[i]=pos_num
            npos=npos+pos_num
            pos_images=ranks.iloc[:,i]
            dic_evaluate['qgnd']=qgnd
            dic_evaluate['ranks']=pos_images
            debug_list.append(dic_evaluate)
            f1.write('\n'+str(pos_num)+'\n')
            f1.write(str(qgnd)+ '\n')
            f1.write(str(pos_images))
            #breakpoint()
    #map = map / (nq - nempty)
    #pr = pr / (nq - nempty)
    map = nmap / nq
    num_pos = npos / nq
    print(debug_list)
    return map, aps,num_pos,num_array
    #return map, aps, pr, prs


def compute_map_and_print(dataset, ranks, qg,ig, kappas=[1, 5, 10]):
    
    # old evaluation protocol
    if dataset == 'mitsubishi_dataset':
        #map, aps, _, _ = compute_map(ranks, qg,ig)
        map, aps,num_pos,num_array = compute_map(ranks, qg,ig)
        print('>> {}: mAP {:.2f}'.format(dataset, np.around(map*100, decimals=2)))
        print('>> {}: aps {}'.format(dataset,aps))
        print('>> {}: num_pos {}'.format(dataset,num_pos))
        print('>> {}: num_array {}'.format(dataset,num_array))