def _join_non_unique(self, other, how="left", return_indexers=False):
    left_idx, right_idx = _get_join_indexers(
        [lvalues], [rvalues], how=how, sort=True
    )
    left_idx = ensure_platform_int(left_idx)
    right_idx = ensure_platform_int(right_idx)

    join_index = np.asarray(lvalues.take(left_idx))
    join_index = self._wrap_joined_index(join_index, other)

    if return_indexers:
        return join_index, left_idx, right_idx
    else:
        return join_index
