from warnings import warn

from OCC.BRepAlgoAPI import (BRepAlgoAPI_Common, BRepAlgoAPI_Cut,
                             BRepAlgoAPI_Fuse, BRepAlgoAPI_Section)
from OCC.GEOMAlgo import GEOMAlgo_Splitter

from afem.occ.utils import (to_lst_from_toptools_listofshape,
                            to_toptools_listofshape)
from afem.topology.check import CheckShape

__all__ = ["BopAlgo", "FuseShapes", "CutShapes", "CommonShapes",
           "IntersectShapes", "SplitShapes"]


class BopAlgo(object):
    """
    Base class for Boolean operations.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.
    :param bop: The OpenCASCADE class for the Boolean operation.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.
    """

    def __init__(self, shape1, shape2, parallel, fuzzy_val, bop):
        if CheckShape.is_shape(shape1) and CheckShape.is_shape(shape2):
            self._bop = bop(shape1, shape2)
        else:
            self._bop = bop()
        if parallel:
            self._bop.SetRunParallel(True)
        if fuzzy_val is not None:
            self._bop.SetFuzzyValue(fuzzy_val)

    @property
    def _is_splitter(self):
        return isinstance(self._bop, GEOMAlgo_Splitter)

    def set_args(self, shapes):
        """
        Set the arguments.

        :param list[OCC.TopoDS.TopoDS_Shape] shapes: The arguments.

        :return: None.
        """
        if self._is_splitter:
            for shape in shapes:
                self._bop.AddArgument(shape)
                return None
        args = to_toptools_listofshape(shapes)
        self._bop.SetArguments(args)

    def set_tools(self, shapes):
        """
        Set the tools.

        :param list[OCC.TopoDS.TopoDS_Shape] shapes: The tools.

        :return: None.
        """
        if self._is_splitter:
            for shape in shapes:
                self._bop.AddTool(shape)
                return None
        tools = to_toptools_listofshape(shapes)
        self._bop.SetTools(tools)

    def build(self):
        """
        Build the results.

        :return: None.
        """
        if self._is_splitter:
            self._bop.Perform()
        else:
            self._bop.Build()

    @property
    def is_done(self):
        """
        :return: *True* if operation is done, *False* if not.
        :rtype: bool
        """
        if self._is_splitter:
            return self._bop.ErrorStatus() == 0
        return self._bop.IsDone()

    @property
    def shape(self):
        """
        :return: The resulting shape.
        :rtype: OCC.TopoDS.TopoDS_Shape
        """
        return self._bop.Shape()

    def refine_edges(self):
        """
        Fuse C1 edges.

        :return: None.
        """
        if self._is_splitter:
            warn('Refine edges not implemented for GEOMAlgo_Splitter.',
                 RuntimeWarning)
        else:
            self._bop.RefineEdges()

    @property
    def fuse_edges(self):
        """
        :return: The result flag of edge refining.
        :rtype: bool
        """
        if self._is_splitter:
            return False
        else:
            return self._bop.FuseEdges()

    @property
    def section_edges(self):
        """
        :return: A list of section edges as a result of intersection between
            the shapes.
        :rtype: list[OCC.TopoDS.TopoDS_Edge]
        """
        if self._is_splitter:
            warn('Section edges not implemented for GEOMAlgo_Splitter. '
                 'Returning empty list.',
                 RuntimeWarning)
            return []
        else:
            return to_lst_from_toptools_listofshape(self._bop.SectionEdges())

    @property
    def has_modified(self):
        """
        :return: *True* if there is at least one modified shape.
        :rtype: bool
        """
        return self._bop.HasModified()

    @property
    def has_generated(self):
        """
        :return: *True* if there is at least one generated shape.
        :rtype: bool
        """
        return self._bop.HasGenerated()

    @property
    def has_deleted(self):
        """
        :return: *True* if there is at least one deleted shape.
        :rtype: bool
        """
        return self._bop.HasDeleted()

    def modified(self, shape):
        """
        Return a list of shapes modified from the given shape.

        :param OCC.TopoDS.TopoDS_Shape shape: The shape.

        :return: List of modified shapes.
        :rtype: list[OCC.TopoDS.TopoDS_Shape]
        """
        return to_lst_from_toptools_listofshape(self._bop.Modified(shape))

    def generated(self, shape):
        """
        Return a list of shapes generated from the given shape.

        :param OCC.TopoDS.TopoDS_Shape shape: The shape.

        :return: List of generated shapes.
        :rtype: list[OCC.TopoDS.TopoDS_Shape]
        """
        return to_lst_from_toptools_listofshape(self._bop.Generated(shape))

    def is_deleted(self, shape):
        """
        Check to see if shape is deleted.

        :param OCC.TopoDS.TopoDS_Shape shape: The shape.

        :return: *True* if deleted, *False* if not.
        :rtype: bool
        """
        return self._bop.IsDeleted(shape)


class FuseShapes(BopAlgo):
    """
    Boolean fuse operation.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.

    For more information see BRepAlgoAPI_Fuse_.

    .. _BRepAlgoAPI_Fuse: https://www.opencascade.com/doc/occt-7.1.0/refman/html/class_b_rep_algo_a_p_i___fuse.html

    Usage:

    >>> from afem.topology import *
    >>> e1 = EdgeByPoints((0., 0., 0.), (10., 0., 0.)).edge
    >>> e2 = EdgeByPoints((5., 1., 0.), (5., -1., 0.)).edge
    >>> bop = FuseShapes(e1, e2)
    >>> assert bop.is_done
    >>> shape = bop.shape
    >>> # Setting arguments and tools
    >>> bop = FuseShapes()
    >>> bop.set_args([e1])
    >>> bop.set_tools([e2])
    >>> bop.build()
    >>> assert bop.is_done
    """

    def __init__(self, shape1=None, shape2=None, parallel=True,
                 fuzzy_val=None):
        super(FuseShapes, self).__init__(shape1, shape2, parallel,
                                         fuzzy_val, BRepAlgoAPI_Fuse)


class CutShapes(BopAlgo):
    """
    Boolean cut operation.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.

    For more information see BRepAlgoAPI_Cut_.

    .. _BRepAlgoAPI_Cut: https://www.opencascade.com/doc/occt-7.1.0/refman/html/class_b_rep_algo_a_p_i___cut.html

    Usage:

    >>> from afem.topology import *
    >>> e1 = EdgeByPoints((0., 0., 0.), (10., 0., 0.)).edge
    >>> e2 = EdgeByPoints((5., 1., 0.), (5., -1., 0.)).edge
    >>> bop = CutShapes(e1, e2)
    >>> assert bop.is_done
    >>> shape = bop.shape
    >>> # Setting arguments and tools
    >>> bop = CutShapes()
    >>> bop.set_args([e1])
    >>> bop.set_tools([e2])
    >>> bop.build()
    >>> assert bop.is_done
    """

    def __init__(self, shape1=None, shape2=None, parallel=True,
                 fuzzy_val=None):
        super(CutShapes, self).__init__(shape1, shape2, parallel,
                                        fuzzy_val, BRepAlgoAPI_Cut)


class CommonShapes(BopAlgo):
    """
    Boolean common operation.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.

    For more information see BRepAlgoAPI_Common_.

    .. _BRepAlgoAPI_Common: https://www.opencascade.com/doc/occt-7.1.0/refman/html/class_b_rep_algo_a_p_i___common.html

    Usage:

    >>> from afem.topology import *
    >>> e1 = EdgeByPoints((0., 0., 0.), (10., 0., 0.)).edge
    >>> e2 = EdgeByPoints((5., 1., 0.), (5., -1., 0.)).edge
    >>> bop = CommonShapes(e1, e2)
    >>> assert bop.is_done
    >>> shape = bop.shape
    >>> # Setting arguments and tools
    >>> bop = CommonShapes()
    >>> bop.set_args([e1])
    >>> bop.set_tools([e2])
    >>> bop.build()
    >>> assert bop.is_done
    """

    def __init__(self, shape1=None, shape2=None, parallel=True,
                 fuzzy_val=None):
        super(CommonShapes, self).__init__(shape1, shape2, parallel,
                                           fuzzy_val, BRepAlgoAPI_Common)


class IntersectShapes(BopAlgo):
    """
    Boolean intersect operation.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.

    For more information see BRepAlgoAPI_Section_.

    .. _BRepAlgoAPI_Section: https://www.opencascade.com/doc/occt-7.1.0/refman/html/class_b_rep_algo_a_p_i___section.html

    Usage:

    >>> from afem.topology import *
    >>> e1 = EdgeByPoints((0., 0., 0.), (10., 0., 0.)).edge
    >>> e2 = EdgeByPoints((5., 1., 0.), (5., -1., 0.)).edge
    >>> bop = IntersectShapes(e1, e2)
    >>> assert bop.is_done
    >>> shape = bop.shape
    >>> # Setting arguments and tools
    >>> bop = IntersectShapes()
    >>> bop.set_args([e1])
    >>> bop.set_tools([e2])
    >>> bop.build()
    >>> assert bop.is_done
    """

    def __init__(self, shape1=None, shape2=None, parallel=True,
                 fuzzy_val=None):
        super(IntersectShapes, self).__init__(shape1, shape2, parallel,
                                              fuzzy_val, BRepAlgoAPI_Section)


class SplitShapes(BopAlgo):
    """
    Split arbitrary shapes. This is a wrapper for the SALOME
    GEOMAlgo_Splitter tool.

    :param shape1: The first shape.
    :type shape1: OCC.TopoDS.TopoDS_Shape or None
    :param shape2: The second shape.
    :type shape2: OCC.TopoDS.TopoDS_Shape or None
    :param bool parallel: Option to run in parallel mode.
    :param float fuzzy_val: Fuzzy tolerance value.

    .. note::

        If *shape1* or *shape2* is *None* then the user is expected to manually
        set the arguments and tools and build the result.

    Usage:

    >>> from afem.topology import *
    >>> e1 = EdgeByPoints((0., 0., 0.), (10., 0., 0.)).edge
    >>> e2 = EdgeByPoints((5., 1., 0.), (5., -1., 0.)).edge
    >>> bop = SplitShapes(e1, e2)
    >>> assert bop.is_done
    >>> shape = bop.shape
    >>> # Setting arguments and tools
    >>> bop = SplitShapes()
    >>> bop.set_args([e1])
    >>> bop.set_tools([e2])
    >>> bop.build()
    >>> assert bop.is_done
    """

    def __init__(self, shape1=None, shape2=None, parallel=True,
                 fuzzy_val=None):
        super(SplitShapes, self).__init__(None, None, parallel,
                                          fuzzy_val, GEOMAlgo_Splitter)
        if CheckShape.is_shape(shape1) and CheckShape.is_shape(shape2):
            self._bop.AddArgument(shape1)
            self._bop.AddArgument(shape2)
            self._bop.Perform()

    def add_arg(self, shape):
        """
        Add an argument.

        :param OCC.TopoDS.TopoDS_Shape shape: The argument.

        :return: None.
        """
        self._bop.AddArgument(shape)

    def add_tool(self, shape):
        """
        Add a tool.

        :param OCC.TopoDS.TopoDS_Shape shape: The tool.

        :return: None.
        """
        self._bop.AddTool(shape)


if __name__ == "__main__":
    import doctest

    doctest.testmod()