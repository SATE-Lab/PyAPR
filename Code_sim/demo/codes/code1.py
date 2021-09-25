def _join_multi(self, other, how, return_indexers=True):
    (join_idx, lidx, ridx) = self_jnlevels.join(other_jnlevels, how, return_indexers=True)
    multi_join_idx = MultiIndex(levels=levels, codes=codes, names=names, verify_integrity=False)
    multi_join_idx = multi_join_idx.remove_unused_levels()
    return (multi_join_idx, lidx, ridx)

