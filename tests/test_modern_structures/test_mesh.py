# Copyright (c) 2014-2019, Manfred Moitzi
# License: MIT License
import pytest
import ezdxf
from ezdxf.modern.mesh import Mesh, tag_processor
from ezdxf.lldxf.extendedtags import ExtendedTags


@pytest.fixture(scope='module')
def dwg():
    return ezdxf.new('AC1015')


@pytest.fixture(scope='module')
def msp(dwg):
    return dwg.modelspace()


@pytest.fixture
def mesh(dwg):
    tags = tag_processor(ExtendedTags.from_text(MESH))
    return Mesh(tags, dwg)


def test_mesh_properties(mesh):
    assert 'MESH' == mesh.dxftype()
    assert 256 == mesh.dxf.color
    assert '0' == mesh.dxf.layer
    assert 'BYLAYER' == mesh.dxf.linetype
    assert mesh.dxf.paperspace == 0


def test_mesh_dxf_attribs(mesh):
    assert 2 == mesh.dxf.version
    assert 0 == mesh.dxf.blend_crease
    assert 3 == mesh.dxf.subdivision_levels


def test_mesh_geometric_data(mesh):
    with mesh.edit_data() as mesh_data:
        assert 56 == len(mesh_data.vertices)
        assert 54 == len(mesh_data.faces)
        assert 108 == len(mesh_data.edges)
        assert 108 == len(mesh_data.edge_crease_values)


def test_create_empty_mesh(msp):
    mesh = msp.add_mesh()
    assert 2 == mesh.dxf.version
    assert 0 == mesh.dxf.blend_crease
    assert 0 == mesh.dxf.subdivision_levels


def test_add_faces(msp):
    mesh = msp.add_mesh()
    with mesh.edit_data() as mesh_data:
        mesh_data.add_face([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
        assert 4 == len(mesh_data.vertices)
        assert 1 == len(mesh_data.faces)
        assert [0, 1, 2, 3] == mesh_data.faces[0]


def test_add_edges(msp):
    mesh = msp.add_mesh()
    with mesh.edit_data() as mesh_data:
        mesh_data.add_edge([(0, 0, 0), (1, 0, 0)])
        assert 2 == len(mesh_data.vertices)
        assert 1 == len(mesh_data.edges)
        assert [0, 1] == mesh_data.edges[0]


def test_vertex_format(msp):
    mesh = msp.add_mesh()
    with mesh.edit_data() as mesh_data:
        with pytest.raises(ezdxf.DXFValueError):
            mesh_data.add_vertex((0, 0))  # only (x, y, z) vertices allowed


def test_optimize(msp):
    vertices = [
        (0, 0, 0),
        (1, 0, 0),
        (1, 1, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (1, 1, 1),
        (0, 1, 1),
    ]

    # 6 cube faces
    cube_faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [3, 2, 6, 7],
        [0, 3, 7, 4]
    ]
    mesh = msp.add_mesh()
    with mesh.edit_data() as mesh_data:
        for face in cube_faces:
            mesh_data.add_face([vertices[index] for index in face])
        assert 24 == len(mesh_data.vertices)
        assert 6 == len(mesh_data.faces)
        mesh_data.optimize()
        assert 8 == len(mesh_data.vertices), "Doublettes not removed"
        assert 6 == len(mesh_data.faces)
        assert 0 == len(mesh_data.edges)


MESH = """  0
MESH
5
2E2
330
1F
100
AcDbEntity
8
0
100
AcDbSubDMesh
71
2
72
0
91
3
92
56
10
284.7875769672455
20
754.2780370501814
30
64.23540699023241
10
284.7875769672455
20
754.2780370501814
30
0.0
10
284.7875769672455
20
616.8856749189314
30
64.23540699023241
10
284.7875769672455
20
616.8856749189314
30
0.0
10
284.7875769672455
20
360.4098446797661
30
193.4439639884759
10
284.7875769672455
20
479.4933127876815
30
0.0
10
284.7875769672455
20
463.228394722746
30
102.3121531918951
10
284.7875769672455
20
342.1009506564315
30
0.0
10
427.8287432817834
20
754.2780370501814
30
64.23540699023241
10
427.8287432817834
20
754.2780370501814
30
0.0
10
427.8287432817834
20
616.8856749189314
30
64.23540699023241
10
427.8287432817834
20
616.8856749189314
30
0.0
10
427.8287432817834
20
360.4098446797661
30
193.4439639884759
10
427.8287432817834
20
479.4933127876815
30
0.0
10
427.8287432817834
20
463.228394722746
30
102.3121531918951
10
427.8287432817834
20
342.1009506564315
30
0.0
10
570.8699095963213
20
754.2780370501814
30
64.23540699023241
10
570.8699095963213
20
754.2780370501814
30
0.0
10
570.8699095963213
20
616.8856749189314
30
64.23540699023241
10
570.8699095963213
20
616.8856749189314
30
0.0
10
570.8699095963213
20
360.4098446797661
30
193.4439639884759
10
570.8699095963213
20
479.4933127876815
30
0.0
10
570.8699095963213
20
463.228394722746
30
102.3121531918951
10
570.8699095963213
20
342.1009506564315
30
0.0
10
713.9110759108594
20
754.2780370501814
30
64.23540699023241
10
713.9110759108594
20
754.2780370501814
30
0.0
10
713.9110759108594
20
616.8856749189314
30
64.23540699023241
10
713.9110759108594
20
616.8856749189314
30
0.0
10
713.9110759108594
20
360.4098446797661
30
193.4439639884759
10
713.9110759108594
20
479.4933127876815
30
0.0
10
713.9110759108594
20
463.228394722746
30
102.3121531918951
10
713.9110759108594
20
342.1009506564315
30
0.0
10
427.8287432817834
20
342.1009506564315
30
21.41180233007747
10
427.8287432817834
20
754.2780370501814
30
21.41180233007747
10
427.8287432817834
20
342.1009506564315
30
42.82360466015493
10
427.8287432817834
20
754.2780370501814
30
42.82360466015493
10
570.8699095963213
20
342.1009506564315
30
21.41180233007747
10
570.8699095963213
20
754.2780370501814
30
21.41180233007747
10
570.8699095963213
20
342.1009506564315
30
42.82360466015493
10
570.8699095963213
20
754.2780370501814
30
42.82360466015493
10
713.9110759108594
20
616.8856749189314
30
21.41180233007747
10
284.7875769672455
20
616.8856749189314
30
21.41180233007747
10
713.9110759108594
20
616.8856749189314
30
42.82360466015493
10
284.7875769672455
20
616.8856749189314
30
42.82360466015493
10
713.9110759108594
20
479.4933127876815
30
21.41180233007747
10
284.7875769672455
20
479.4933127876815
30
21.41180233007747
10
713.9110759108594
20
479.4933127876815
30
42.82360466015493
10
284.7875769672455
20
479.4933127876815
30
42.82360466015493
10
284.7875769672455
20
754.2780370501814
30
21.41180233007747
10
284.7875769672455
20
342.1009506564315
30
21.41180233007747
10
713.9110759108594
20
754.2780370501814
30
21.41180233007747
10
713.9110759108594
20
342.1009506564315
30
21.41180233007747
10
284.7875769672455
20
754.2780370501814
30
42.82360466015493
10
284.7875769672455
20
342.1009506564315
30
42.82360466015493
10
713.9110759108594
20
754.2780370501814
30
42.82360466015493
10
713.9110759108594
20
342.1009506564315
30
42.82360466015493
93
270
90
4
90
2
90
10
90
8
90
0
90
4
90
4
90
12
90
10
90
2
90
4
90
6
90
14
90
12
90
4
90
4
90
10
90
18
90
16
90
8
90
4
90
12
90
20
90
18
90
10
90
4
90
14
90
22
90
20
90
12
90
4
90
18
90
26
90
24
90
16
90
4
90
20
90
28
90
26
90
18
90
4
90
22
90
30
90
28
90
20
90
4
90
1
90
9
90
11
90
3
90
4
90
3
90
11
90
13
90
5
90
4
90
5
90
13
90
15
90
7
90
4
90
9
90
17
90
19
90
11
90
4
90
11
90
19
90
21
90
13
90
4
90
13
90
21
90
23
90
15
90
4
90
17
90
25
90
27
90
19
90
4
90
19
90
27
90
29
90
21
90
4
90
21
90
29
90
31
90
23
90
4
90
15
90
32
90
49
90
7
90
4
90
32
90
34
90
53
90
49
90
4
90
34
90
14
90
6
90
53
90
4
90
23
90
36
90
32
90
15
90
4
90
36
90
38
90
34
90
32
90
4
90
38
90
22
90
14
90
34
90
4
90
31
90
51
90
36
90
23
90
4
90
51
90
55
90
38
90
36
90
4
90
55
90
30
90
22
90
38
90
4
90
48
90
33
90
9
90
1
90
4
90
52
90
35
90
33
90
48
90
4
90
0
90
8
90
35
90
52
90
4
90
33
90
37
90
17
90
9
90
4
90
35
90
39
90
37
90
33
90
4
90
8
90
16
90
39
90
35
90
4
90
37
90
50
90
25
90
17
90
4
90
39
90
54
90
50
90
37
90
4
90
16
90
24
90
54
90
39
90
4
90
50
90
40
90
27
90
25
90
4
90
54
90
42
90
40
90
50
90
4
90
24
90
26
90
42
90
54
90
4
90
40
90
44
90
29
90
27
90
4
90
42
90
46
90
44
90
40
90
4
90
26
90
28
90
46
90
42
90
4
90
44
90
51
90
31
90
29
90
4
90
46
90
55
90
51
90
44
90
4
90
28
90
30
90
55
90
46
90
4
90
1
90
3
90
41
90
48
90
4
90
48
90
41
90
43
90
52
90
4
90
52
90
43
90
2
90
0
90
4
90
3
90
5
90
45
90
41
90
4
90
41
90
45
90
47
90
43
90
4
90
43
90
47
90
4
90
2
90
4
90
5
90
7
90
49
90
45
90
4
90
45
90
49
90
53
90
47
90
4
90
47
90
53
90
6
90
4
94
108
90
2
90
10
90
8
90
10
90
0
90
8
90
0
90
2
90
4
90
12
90
10
90
12
90
2
90
4
90
6
90
14
90
12
90
14
90
4
90
6
90
10
90
18
90
16
90
18
90
8
90
16
90
12
90
20
90
18
90
20
90
14
90
22
90
20
90
22
90
18
90
26
90
24
90
26
90
16
90
24
90
20
90
28
90
26
90
28
90
22
90
30
90
28
90
30
90
1
90
9
90
9
90
11
90
3
90
11
90
1
90
3
90
11
90
13
90
5
90
13
90
3
90
5
90
13
90
15
90
7
90
15
90
5
90
7
90
9
90
17
90
17
90
19
90
11
90
19
90
19
90
21
90
13
90
21
90
21
90
23
90
15
90
23
90
17
90
25
90
25
90
27
90
19
90
27
90
27
90
29
90
21
90
29
90
29
90
31
90
23
90
31
90
15
90
32
90
32
90
49
90
7
90
49
90
32
90
34
90
34
90
53
90
49
90
53
90
14
90
34
90
6
90
53
90
23
90
36
90
32
90
36
90
36
90
38
90
34
90
38
90
22
90
38
90
31
90
51
90
36
90
51
90
51
90
55
90
38
90
55
90
30
90
55
90
33
90
48
90
9
90
33
90
1
90
48
90
35
90
52
90
33
90
35
90
48
90
52
90
8
90
35
90
0
90
52
90
33
90
37
90
17
90
37
90
35
90
39
90
37
90
39
90
16
90
39
90
37
90
50
90
25
90
50
90
39
90
54
90
50
90
54
90
24
90
54
90
40
90
50
90
27
90
40
90
42
90
54
90
40
90
42
90
26
90
42
90
40
90
44
90
29
90
44
90
42
90
46
90
44
90
46
90
28
90
46
90
44
90
51
90
46
90
55
90
3
90
41
90
41
90
48
90
41
90
43
90
43
90
52
90
2
90
43
90
5
90
45
90
41
90
45
90
45
90
47
90
43
90
47
90
4
90
47
90
45
90
49
90
47
90
53
95
108
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
140
0.0
90
0
"""
