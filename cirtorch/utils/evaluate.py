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
    """
    Computes the mAP for a given set of returned results.

         Usage: 
           map = compute_map (ranks, gnd) 
                 computes mean average precsion (map) only
        
           map, aps, pr, prs = compute_map (ranks, gnd, kappas) 
                 computes mean average precision (map), average precision (aps) for each query
                 computes mean precision at kappas (pr), precision at kappas (prs) for each query
        
         Notes:
         1) ranks starts from 0, ranks.shape = db_size X #queries
         2) The junk results (e.g., the query itself) should be declared in the gnd stuct array
         3) If there are no positive images for some query, that query is excluded from the evaluation
    """
    nmap = 0.
    map = 0.
    pos_num=0.
    npos=0.
    nq = len(qg) # number of queries
    aps = np.zeros(nq)
    num_array=np.zeros(nq)
    #pr = np.zeros(len(kappas))
    #prs = np.zeros((nq, len(kappas)))
    nempty = 0
    debug_list=[]
    dic_evaluate={}
    #i回目の検索
    #for i in range(nq):
    with open('debug_list_global.txt', 'a', encoding='utf-8') as f1:
        for i in range(nq):
            #qgnd = np.array(gnd[i]['ok'])
            qgnd = np.array(qg[i]['label'])
            print(qgnd)
            '''
            # no positive images, skip from the average
            if qgnd.shape[0] == 0:
                aps[i] = float('nan')
                prs[i, :] = float('nan')
                nempty += 1
                continue
            
            try:
                qgndj = np.array(gnd[i]['junk'])
            except:
                qgndj = np.empty(0)
            '''
            #breakpoint()
            # sorted positions of positive and junk images (0 based)
            pos  = np.arange(ranks.shape[0])[np.in1d(ranks.iloc[:,i], qgnd)]
            #breakpoint()
            #junk = np.arange(ranks.shape[0])[np.in1d(ranks[:,i], qgndj)]
            '''
            k = 0;
            ij = 0;
            if len(junk):
                # decrease positions of positives based on the number of
                # junk images appearing before them
                ip = 0
                while (ip < len(pos)):
                    while (ij < len(junk) and pos[ip] > junk[ij]):
                        k += 1
                        ij += 1
                    pos[ip] = pos[ip] - k
                    ip += 1
            '''
            # compute ap
            ap = compute_ap(pos, len(pos))
            nmap = nmap + ap
            #map=nmap/(i+1)
            aps[i] = ap
            #breakpoint()
            #num_pos検索画像数について評価する
            pos_num=len(pos)/10
            num_array[i]=pos_num
            npos=npos+pos_num
            pos_images=ranks.iloc[:,i]
            dic_evaluate['qgnd']=qgnd
            dic_evaluate['ranks']=pos_images
            debug_list.append(dic_evaluate)
            # compute precision @ k
            '''
            pos += 1 # get it to 1-based
            for j in np.arange(len(kappas)):
                kq = min(max(pos), kappas[j]); 
                prs[i, j] = (pos <= kq).sum() / kq
            pr = pr + prs[i, :]
            '''
            f1.write('\n'+str(pos_num)+'\n')
            f1.write(str(qgnd)+ '\n')
            f1.write(str(pos_images))
    map = nmap / nq
    num_pos = npos / nq
    #print(debug_list)
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