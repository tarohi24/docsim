import logging
from typing import List, Optional

import numpy as np

from docsim.embedding.base import return_matrix


logger = logging.getLogger(__file__)


@return_matrix
def _get_new_kemb_cand(cand_emb: np.ndarray,
                       keyword_embs: Optional[np.ndarray]) -> np.ndarray:
    if keyword_embs is None:
        return cand_emb.reshape(1, -1)
    else:
        assert keyword_embs.ndim == 2
        return np.concatenate([keyword_embs, cand_emb.reshape(1, -1)])


def rec_loss(embs: np.ndarray,
             keyword_embs: Optional[np.ndarray],
             cand_emb: np.ndarray) -> float:
    """
    Reconstruct error. In order to enable unittests, two errors are
    implemented individually.
    """
    dims: np.ndarray = _get_new_kemb_cand(cand_emb=cand_emb,
                                          keyword_embs=keyword_embs)
    maxes: np.ndarray = np.amax(np.dot(embs, dims.T), axis=1)
    return (1 - maxes).mean()


def cent_sim_loss(keyword_embs: np.ndarray,
                  cand_emb: np.ndarray) -> float:
    """
    Loss penalizing for similar dimensions
    """
    return np.dot(keyword_embs, cand_emb)


def calc_error(embs: np.ndarray,
               keyword_embs: Optional[np.ndarray],
               cand_emb: np.ndarray,
               coef: float) -> float:
    rec_error: float = rec_loss(embs, keyword_embs, cand_emb)
    if keyword_embs is not None:
        cent_sim_error: float = cent_sim_loss(keyword_embs, cand_emb)
    else:
        cent_sim_error: float = 0  # type: ignore
    logger.info(f'rec_error: {str(rec_error)}, cent_sim_error: {str(cent_sim_error)}')
    return rec_error + coef * cent_sim_error


@return_matrix
def get_keyword_embs(tokens: List[str],
                     embs: np.ndarray,
                     keyword_embs: Optional[np.ndarray],
                     n_remains: int,
                     coef: float) -> np.ndarray:
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
    new_dims: np.ndarray = _get_new_kemb_cand(cand_emb=new_keyword_emb,
                                              keyword_embs=keyword_embs)
    if n_remains == 1:
        return new_dims
    else:
        return get_keyword_embs(
            tokens=[t for t, is_valid in zip(tokens, residual_inds) if is_valid],
            embs=embs[residual_inds, :],
            keyword_embs=new_dims,
            n_remains=(n_remains - 1),
            coef=coef
        )
