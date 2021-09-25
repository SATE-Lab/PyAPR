def astype(self, dtype, copy=True):
    dtype = pandas_dtype(dtype)
    if is_dtype_equal(dtype, self.dtype):
        if copy:
            return self.copy()
        return self
    elif isinstance(dtype, _IntegerDtype):
        arr = self._ndarray.copy()
        mask = self.isna()
        arr[mask] = 0
        values = arr.astype(dtype.numpy_dtype)
        return IntegerArray(values, mask, copy=False)
    elif isinstance(dtype, FloatingDtype):
        # error: Incompatible types in assignment (expression has type
        # "StringArray", variable has type "ndarray")
        arr = self.copy()  # type: ignore[assignment]
        mask = self.isna()
        arr[mask] = "0"
        values = arr.astype(dtype.numpy_dtype)
        return FloatingArray(values, mask, copy=False)
    elif np.issubdtype(dtype, np.floating):
        arr = self._ndarray.copy()
        mask = self.isna()
        arr[mask] = 0
        values = arr.astype(dtype)
        values[mask] = np.nan
        return values
    return super().astype(dtype, copy)
