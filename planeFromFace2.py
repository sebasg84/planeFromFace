# ***************************************************************************
# *   Copyright (c) 2021 Sebastian Ernesto García <sebasg@outlook.com>      *
# *                                                                         *
# *   gears.py                                                              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
#
# Changes: 18Turbo (Rafael Martínez)
#   * Change Center of Mass --> Bounding Box
#   * Show the geometry base

import FreeCAD as App
import FreeCADGui as Gui

from numpy import array, eye, pi
sel = Gui.Selection.getSelectionEx()

if len(sel) == 1:
    subobjs = sel[0].SubObjects
    if len(subobjs) == 1:
        face = subobjs[0]
        if face.ShapeType == 'Face':
            body = sel[0].Object._Body
            planeXY = body.Origin.OriginFeatures[3]

            datumPlane = body.newObject('PartDesign::Plane','DatumPlane')

            normalDatum = face.normalAt(0,0)
            if normalDatum.z < 0:
                normalXY = App.Vector(0, 0, -1)
            else:
                normalXY = App.Vector(0, 0, 1)
            v = normalXY.cross(normalDatum)
            epsilon = 0.0000000001
            if v.Length > epsilon:
                c = normalXY.dot(normalDatum)
                s = v.normalize()
                vx = array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
                R = eye(3) + vx + vx.dot(vx) * ((1 - c) / (s.dot(s)))
                rotation = App.Rotation(*R.reshape(9))
                if normalDatum.z < 0:
                    datumPlane.Placement = App.Placement( App.Vector(face.BoundBox.XMin, face.BoundBox.YMin, face.BoundBox.ZMin) ,App.Rotation(rotation.Axis, rotation.Angle * 180 / pi + 180))
                else:
                    datumPlane.Placement = App.Placement( App.Vector(face.BoundBox.XMin, face.BoundBox.YMin, face.BoundBox.ZMin) ,App.Rotation(rotation.Axis, rotation.Angle * 180 / pi))
            else:
                datumPlane.Placement = App.Placement( App.Vector(face.BoundBox.XMin, face.BoundBox.YMin, face.BoundBox.ZMin) ,App.Rotation(App.Vector(0,0,0), 0) )

            datumPlane.recompute()
            sketch = body.newObject('Sketcher::SketchObject','Sketch')
            sketch.Support = (datumPlane,'')
            sketch.MapMode = 'FlatFace'
            FreeCADGui.ActiveDocument.activeObject().HideDependent = False
            App.ActiveDocument.recompute()
            Gui.ActiveDocument.setEdit(body,0,sketch.Name+".")
            datumPlane.Visibility = False

        else:
            App.Console.PrintWarning("You must choose one face \n")
    else:
        App.Console.PrintWarning("You must choose one face \n")
else:
    App.Console.PrintWarning("You must choose one face \n")
