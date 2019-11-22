import logging
from typing import List

import numpy as np


logger = logging.getLogger(__file__)


def rec_loss(embs: np.ndarray,
             keyword_embs: np.ndarray,
             cand_emb: np.ndarray) -> float:
    """
    Reconstruct error. In order to enable unittests, two errors are
    implemented individually.
    """
    if keyword_embs.ndim == 2:
        dims: np.ndarray = np.append(keyword_embs, cand_emb)
    else:
        dims: np.ndarray = np.array([cand_emb])  # type: ignore
    maxes: np.ndarray = np.amax(np.dot(embs, dims.T), axis=1)
    return (1 - maxes).mean()


def cent_sim_loss(keyword_embs: np.ndarray,
                  cand_emb: np.ndarray) -> float:
    """
    Loss penalizing for similar dimensions
    """
    if keyword_embs.ndim == 1:
        return 0
    return np.dot(keyword_embs, cand_emb)


def calc_error(embs: np.ndarray,
               keyword_embs: np.ndarray,
               cand_emb: np.ndarray,
               coef: float) -> float:
    rec_error: float = rec_loss(embs, keyword_embs, cand_emb)
    cent_sim_error: float = cent_sim_loss(keyword_embs, cand_emb)
    logger.info(f'rec_error: {str(rec_error)}, cent_sim_error: {str(cent_sim_error)}')
    return rec_error + coef * cent_sim_error


def get_keyword_embs(tokens: List[str],
                     embs: np.ndarray,
                     keyword_embs: np.ndarray,
                     n_remains: int,
                     coef: float) -> np.ndarray:
    if n_remains == 0:
        return []
    errors: List[float] = [calc_error(embs=embs,
                                      keyword_embs=keyword_embs,
                                      cand_emb=embs[i],
                                      coef=coef)
                           for i in range(len(tokens))]
    argmin: int = np.argmin(errors)
    keyword: str = tokens[argmin]
    new_keyword_emb = embs[argmin]
    residual_inds = [(t != keyword) for t in tokens]
    logger.info(f'keyword: {keyword}')
    if n_remains == 1:
        return np.append(keyword_embs, new_keyword_emb)
    else:
        residual_embs: np.ndarray = get_keyword_embs(
            tokens=[t for t, is_valid in zip(tokens, residual_inds) if is_valid],
            embs=embs[residual_inds, :],
            keyword_embs=np.append(keyword_embs, new_keyword_emb),
            n_remains=(n_remains - 1),
            coef=coef
        )
        return np.concatenate([keyword_embs, residual_embs])
