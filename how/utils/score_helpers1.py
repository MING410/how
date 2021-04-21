"""Helper functions for computing evaluation scores"""

import numpy as np

from cirtorch.utils.evaluate1 import compute_map


def compute_map_and_log(dataset, ranks, qg,ig, kappas=(1, 5, 10), logger=None):
    """Computed mAP and log it

    :param str dataset: Dataset to compute the mAP on (e.g. roxford5k)
    :param np.ndarray ranks: 2D matrix of ints corresponding to previously computed ranks
    :param dict gnd: Ground-truth dataset structure
    :param list kappas: Compute mean precision at each kappa
    :param logging.Logger logger: If not None, use it to log mAP and all mP@kappa
    :return tuple: mAP and mP@kappa (medium difficulty for roxford5k and rparis6k)
    """
    '''
    # new evaluation protocol
    if dataset.startswith('roxford5k') or dataset.startswith('rparis6k'):
        gnd_t = []
        for gndi in gnd:
            g = {}
            g['ok'] = np.concatenate([gndi['easy']])
            g['junk'] = np.concatenate([gndi['junk'], gndi['hard']])
            gnd_t.append(g)
        mapE, apsE, mprE, prsE = compute_map(ranks, gnd_t, kappas)

        gnd_t = []
        for gndi in gnd:
            g = {}
            g['ok'] = np.concatenate([gndi['easy'], gndi['hard']])
            g['junk'] = np.concatenate([gndi['junk']])
            gnd_t.append(g)
        mapM, apsM, mprM, prsM = compute_map(ranks, gnd_t, kappas)

        gnd_t = []
        for gndi in gnd:
            g = {}
            g['ok'] = np.concatenate([gndi['hard']])
            g['junk'] = np.concatenate([gndi['junk'], gndi['easy']])
            gnd_t.append(g)
        mapH, apsH, mprH, prsH = compute_map(ranks, gnd_t, kappas)

        if logger:
            fmap = lambda x: np.around(x*100, decimals=2)
            logger.info(f"Evaluated {dataset}: mAP E: {fmap(mapE)}, M: {fmap(mapM)}, H: {fmap(mapH)}")
            logger.info(f"Evaluated {dataset}: mP@k{kappas} E: {fmap(mprE)}, M: {fmap(mprM)}, H: {fmap(mprH)}")

        scores = {"map_easy": mapE.item(), "mp@k_easy": mprE, "ap_easy": apsE, "p@k_easy": prsE,
                  "map_medium": mapM.item(), "mp@k_medium": mprM, "ap_medium": apsM, "p@k_medium": prsM,
                  "map_hard": mapH.item(), "mp@k_hard": mprH, "ap_hard": apsH, "p@k_hard": prsH}
        return scores
    '''
    # old evaluation protocol
    breakpoint()
    map_score, ap_scores = compute_map(ranks, qg,ig, kappas=kappas)
    #breakpoint()
    if logger:
        fmap = lambda x: np.around(x*100, decimals=2)
        logger.info(f"Evaluated {dataset}: mAP {fmap(map_score)}")
        logger.info(f"Evaluated {dataset}: aps {fmap(ap_scores)}")
    return {"map": map_score,  "aps": ap_scores}