def astype(self, dtype, copy=True):
    dtype = pandas_dtype(dtype)

    if is_dtype_equal(dtype, self.dtype):
        if copy:
            return self.copy()
        return self

    elif isinstance(dtype, NumericDtype):
        data = self._data.cast(pa.from_numpy_dtype(dtype.numpy_dtype))
        return dtype.__from_arrow__(data)

    elif isinstance(dtype, ExtensionDtype):
        cls = dtype.construct_array_type()
        return cls._from_sequence(self, dtype=dtype, copy=copy)

    return super().astype(dtype, copy)
