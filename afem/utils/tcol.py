from OCC.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal, \
    TColStd_Array2OfReal
from OCC.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, \
    TColgp_Array2OfPnt, TColgp_HArray1OfPnt
from OCC.gp import gp_Pnt, gp_Pnt2d
from numpy import array as np_array, zeros

from .misc import is_array_like

__all__ = ["to_tcolstd_array2_real", "to_tcolstd_array1_real",
           "to_tcolstd_array1_integer", "to_tcolgp_harray1_pnt",
           "to_tcolgp_array2_pnt", "to_tcolgp_array1_pnt2d",
           "to_tcolgp_array1_pnt", "to_np_from_tcolstd_array2_real",
           "to_np_from_tcolstd_array1_real",
           "to_np_from_tcolstd_array1_integer",
           "to_np_from_tcolgp_array2_pnt", "to_np_from_tcolgp_array1_pnt"]


def _to_gp_pnt(p):
    """
    Convert the point_like entity to a Point.
    """
    if isinstance(p, gp_Pnt):
        return p
    if is_array_like(p) and len(p) == 3:
        return gp_Pnt(*p)
    return None


def _to_gp_pnt2d(p):
    """
    Convert the point_like entity to a Point2D.
    """
    if isinstance(p, gp_Pnt2d):
        return p
    if is_array_like(p) and len(p) == 2:
        return gp_Pnt2d(*p)
    return None


def to_tcolgp_array1_pnt(pnts):
    """
    Convert the 1-D array of point_like entities to OCC data.

    :param pnts: Array of points to convert.

    :return: OCC array of points.
    :rtype: TColgp_Array1OfPnt
    """
    # Convert each entity to a Point.
    gp_pnts = []
    for gp in pnts:
        gp = _to_gp_pnt(gp)
        if not gp:
            continue
        gp_pnts.append(gp)

    # Create OCC array.
    n = len(gp_pnts)
    array = TColgp_Array1OfPnt(1, n)
    for i, gp in enumerate(gp_pnts, 1):
        array.SetValue(i, gp)

    return array


def to_tcolgp_array1_pnt2d(pnts):
    """
    Convert the 1-D array of point_like entities to OCC data.

    :param pnts: Array of points to convert.

    :return: OCC array of points.
    :rtype: TColgp_Array1OfPnt2d
    """
    # Convert each entity to a Point2D.
    gp_pnts = []
    for gp in pnts:
        gp = _to_gp_pnt2d(gp)
        if not gp:
            continue
        gp_pnts.append(gp)

    # Create OCC array.
    n = len(gp_pnts)
    array = TColgp_Array1OfPnt2d(1, n)
    for i, gp in enumerate(gp_pnts, 1):
        array.SetValue(i, gp)

    return array


def to_tcolgp_harray1_pnt(pnts):
    """
    Convert the 1-D array of point_like entities to OCC data.

    :param pnts: Array of points to convert.

    :return: OCC array of points.
    :rtype: TColgp_HArray1OfPnt
    """
    # Convert each entity to a Point.
    gp_pnts = []
    for gp in pnts:
        gp = _to_gp_pnt(gp)
        if not gp:
            continue
        gp_pnts.append(gp)

    # Create OCC array.
    n = len(gp_pnts)
    harray = TColgp_HArray1OfPnt(1, n)
    for i, gp in enumerate(gp_pnts, 1):
        harray.SetValue(i, gp)

    return harray


def to_tcolstd_array1_real(array):
    """
    Convert the 1-D array of floats to OCC data.

    :param array: Array of floats.

    :return: OCC array of reals.
    :rtype: TColStd_Array1OfReal
    """
    # Convert the data to floats.
    flts = [float(x) for x in array]

    # Create OCC array.
    n = len(flts)
    array = TColStd_Array1OfReal(1, n)
    for i, x in enumerate(flts, 1):
        array.SetValue(i, x)

    return array


def to_tcolstd_array1_integer(array):
    """
    Convert the 1-D array of integers to OCC data.

    :param array: Array of integers.

    :return: OCC array of integers.
    :rtype: TColStd_Array1OfInteger
    """
    # Convert the data to integers.
    ints = [int(x) for x in array]

    # Create OCC array.
    n = len(ints)
    array = TColStd_Array1OfInteger(1, n)
    for i, x in enumerate(ints, 1):
        array.SetValue(i, x)

    return array


def to_tcolgp_array2_pnt(pnts):
    """
    Convert the 2-D array of point_like entities to OCC data.

    :param pnts: Array of points to convert.

    :return: OCC array of points.
    :rtype: TColgp_Array2OfPnt
    """
    # Convert to array.
    pnts = np_array(pnts, dtype=float)

    # Convert each entity to a Point.
    n, m = pnts.shape[0:2]
    gp_pnts = []
    for i in range(0, n):
        row = []
        for j in range(0, m):
            gp = _to_gp_pnt(pnts[i, j])
            row.append(gp)
        gp_pnts.append(row)

    # Create OCC array.
    array = TColgp_Array2OfPnt(1, n, 1, m)
    for i, row in enumerate(gp_pnts, 1):
        for j, gp in enumerate(row, 1):
            array.SetValue(i, j, gp)

    return array


def to_tcolstd_array2_real(array):
    """
    Convert the 2-D array of floats to OCC data.

    :param array: Array of floats.

    :return: OCC array of reals.
    :rtype: TColStd_Array2OfReal
    """
    # Convert the data to floats.
    flts = np_array(array, dtype=float)

    # Create OCC array.
    n, m = flts.shape
    array = TColStd_Array2OfReal(1, n, 1, m)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            x = float(flts[i - 1, j - 1])
            array.SetValue(i, j, x)

    return array


def to_np_from_tcolstd_array1_real(tcol_array):
    """
    Convert OCC data to NumPy array.

    :param tcol_array:
    :return:
    """
    n = tcol_array.Length()
    array = zeros(n, dtype=float)
    for i in range(n):
        x = tcol_array.Value(i + 1)
        array[i] = x
    return array


def to_np_from_tcolstd_array1_integer(tcol_array):
    """
    Convert OCC data to NumPy array.

    :param tcol_array:
    :return:
    """
    n = tcol_array.Length()
    array = zeros(n, dtype=int)
    for i in range(n):
        x = tcol_array.Value(i + 1)
        array[i] = x
    return array


def to_np_from_tcolgp_array1_pnt(tcol_array):
    """
    Convert OCC data to NumPy array.

    :param tcol_array:
    :return:
    """
    n = tcol_array.Length()
    array = zeros((n, 3), dtype=float)
    for i in range(n):
        p = tcol_array.Value(i + 1)
        array[i, :] = p.X(), p.Y(), p.Z()
    return array


def to_np_from_tcolgp_array2_pnt(tcol_array):
    """
    Convert OCC data to NumPy array.

    :param tcol_array:
    :return:
    """
    n, m = tcol_array.ColLength(), tcol_array.RowLength()
    array = zeros((n, m, 3), dtype=float)
    for i in range(n):
        for j in range(m):
            p = tcol_array.Value(i + 1, j + 1)
            array[i, j, :] = p.X(), p.Y(), p.Z()
    return array


def to_np_from_tcolstd_array2_real(tcol_array):
    """
    Convert OCC data to NumPy array.

    :param tcol_array:
    :return:
    """
    n, m = tcol_array.ColLength(), tcol_array.RowLength()
    array = zeros((n, m), dtype=float)
    for i in range(n):
        for j in range(m):
            x = tcol_array.Value(i + 1, j + 1)
            array[i, j] = x
    return array