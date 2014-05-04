# Purpose: dxf factory for R2000/AC1015
# Created: 12.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals


__author__ = "mozman <mozman@gmx.at>"

from .headervars import VARMAP
from ..legacy import LegacyDXFFactory
from . import tableentries
from . import graphics
from . import dxfobjects
from .layouts import Layouts, BlockLayout

UPDATE_ENTITY_WRAPPERS = {
    # DXF Objects
    'DICTIONARY': dxfobjects.DXFDictionary,
    'ACDBDICTIONARYWDFLT': dxfobjects.DXFDictionaryWithDefault,
    'PLOTSETTINGS': dxfobjects.DXFPlotSettings,
    'LAYOUT': dxfobjects.DXFLayout,
    'XRECORD': dxfobjects.XRecord,
    'DATATABLE': dxfobjects.DXFDataTable,
    # DXF Table Entries
    'LAYER': tableentries.Layer,
    'STYLE': tableentries.Style,
    'LTYPE': tableentries.Linetype,
    'DIMSTYLE': tableentries.DimStyle,
    'VIEW': tableentries.View,
    'VPORT': tableentries.Viewport,
    'UCS': tableentries.UCS,
    'APPID': tableentries.AppID,
    'BLOCK_RECORD': tableentries.BlockRecord,
    # DXF Entities
    'LINE': graphics.Line,
    'POINT': graphics.Point,
    'CIRCLE': graphics.Circle,
    'ARC': graphics.Arc,
    'TRACE': graphics.Trace,
    'SOLID': graphics.Solid,
    '3DFACE': graphics.Face,
    'TEXT': graphics.Text,
    'MTEXT': graphics.MText,
    'POLYLINE': graphics.Polyline,
    'VERTEX': graphics.Vertex,
    'SEQEND': graphics.SeqEnd,
    'LWPOLYLINE': graphics.LWPolyline,
    'BLOCK': graphics.Block,
    'ENDBLK': graphics.EndBlk,
    'INSERT': graphics.Insert,
    'ATTDEF': graphics.Attdef,
    'ATTRIB': graphics.Attrib,
    'ELLIPSE': graphics.Ellipse,
    'RAY': graphics.Ray,
    'XLINE': graphics.XLine,
    'SHAPE': graphics.Shape,
    'SPLINE': graphics.Spline,
    'BODY': graphics.Body,
    'REGION': graphics.Region,
    '3DSOLID': graphics.Solid3d,
}


class ModernDXFFactory(LegacyDXFFactory):
    """ DXf factory for DXF version AC1015 and later. (changed 04.05.2014)
    """
    HEADERVARS = dict(VARMAP)
    DEFAULT_WRAPPER = graphics.GraphicEntity
    TAGS_MODIFIER = {'VERTEX': graphics.Vertex.fix_tags}

    def __init__(self, drawing):
        super(ModernDXFFactory, self).__init__(drawing)
        self.ENTITY_WRAPPERS.update(UPDATE_ENTITY_WRAPPERS)

    @property
    def dxfversion(self):
        return self.drawing.dxfversion

    @property
    def rootdict(self):
        return self.drawing.rootdict

    @property
    def block_records(self):
        return self.drawing.sections.tables.block_records

    def create_block_entry_in_block_records_table(self, block_layout):
        # required for  DXFVERSION > ac1009: Entry in the BLOCK_RECORDS section
        block_record = self.block_records.create(block_layout.name)
        block_layout.set_block_record_handle(block_record.dxf.handle)

    def get_layouts(self):
        return Layouts(self.drawing)

    def new_block_layout(self, block_handle, endblk_handle):
        # Warning: Do not call create_block_entry_in_block_records_table() from this point, this will not work!
        return BlockLayout(self.entitydb, self, block_handle, endblk_handle)

    def copy_layout(self, source_entity, target_entity):
        # Place target_entity in same layout as source_entity
        target_entity.dxf.paperspace = source_entity.dxf.paperspace
        target_entity.dxf.owner = source_entity.dxf.owner

    def modify_tags(self, tags):
        modifier = self.TAGS_MODIFIER.get(tags.dxftype(), None)
        if modifier is not None:
            modifier(tags)