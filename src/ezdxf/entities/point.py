# Copyright (c) 2019-2020 Manfred Moitzi
# License: MIT License
# Created 2019-02-15
from typing import TYPE_CHECKING
from ezdxf.math import Vector, Matrix44
from ezdxf.math.transformtools import transform_thickness_and_extrusion_without_ocs
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass, XType
from ezdxf.lldxf.const import DXF12, SUBCLASS_MARKER
from .dxfentity import base_class, SubclassProcessor
from .dxfgfx import DXFGraphic, acdb_entity
from .factory import register_entity

if TYPE_CHECKING:
    from ezdxf.eztypes import TagWriter, DXFNamespace, UCS

__all__ = ['Point']

acdb_point = DefSubclass('AcDbPoint', {
    'location': DXFAttr(10, xtype=XType.point3d, default=Vector(0, 0, 0)),
    'thickness': DXFAttr(39, default=0, optional=True),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=Vector(0, 0, 1), optional=True),
    # angle of the X axis for the UCS in effect when the point was drawn (optional, default = 0); used when PDMODE is
    # nonzero
    'angle': DXFAttr(50, default=0, optional=True),
})


@register_entity
class Point(DXFGraphic):
    """ DXF POINT entity """
    DXFTYPE = 'POINT'
    DXFATTRIBS = DXFAttributes(base_class, acdb_entity, acdb_point)

    def load_dxf_attribs(self, processor: SubclassProcessor = None) -> 'DXFNamespace':
        """ Loading interface. (internal API) """
        dxf = super().load_dxf_attribs(processor)
        if processor:
            tags = processor.load_dxfattribs_into_namespace(dxf, acdb_point)
            if len(tags) and not processor.r12:
                processor.log_unprocessed_tags(tags, subclass=acdb_point.name)
        return dxf

    def export_entity(self, tagwriter: 'TagWriter') -> None:
        """ Export entity specific data as DXF tags. (internal API) """
        # base class export is done by parent class
        super().export_entity(tagwriter)
        # AcDbEntity export is done by parent class
        if tagwriter.dxfversion > DXF12:
            tagwriter.write_tag2(SUBCLASS_MARKER, acdb_point.name)
        # for all DXF versions
        self.dxf.export_dxf_attribs(tagwriter, ['location', 'thickness', 'extrusion', 'angle'])

    def transform(self, m: Matrix44) -> 'Point':
        """ Transform POINT entity by transformation matrix `m` inplace.

        .. versionadded:: 0.13

        """
        self.dxf.location = m.transform(self.dxf.location)
        transform_thickness_and_extrusion_without_ocs(self, m)
        # ignore dxf.angle!
        return self

    def translate(self, dx: float, dy: float, dz: float) -> 'Point':
        """ Optimized POINT translation about `dx` in x-axis, `dy` in y-axis and `dz` in z-axis,
        returns `self` (floating interface).

        .. versionadded:: 0.13

        """
        self.dxf.location = Vector(dx, dy, dz) + self.dxf.location
        return self
