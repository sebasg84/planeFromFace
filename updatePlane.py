# ***************************************************************************
# *   Copyright (c) 2021 Sebastian Ernesto García <sebasg@outlook.com>      *
# *                                                                         *
# *   gears.py                                                            *
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

import FreeCAD as App
import FreeCADGui as Gui

from numpy import array, eye, pi


sel = Gui.Selection.getSelectionEx()

if len(sel) == 2:

    sel1 = sel[0]
    sel2 = sel[1]

    flag = False
    if sel1.Object.TypeId == 'PartDesign::Plane':
        datumPlane = sel1.Object
        subobjs = sel2.SubObjects
        flag = True
    elif sel2.Object.TypeId == 'PartDesign::Plane':
        datumPlane = sel2.Object
        subobjs = sel1.SubObjects
        flag = True

    if flag == True:
        if len(subobjs) == 1:
            face = subobjs[0]
            if face.ShapeType == 'Face':
                normalDatum = face.normalAt(0,0)
                normalXY = App.Vector(0, 0, 1)
                v = normalXY.cross(normalDatum)
                epsilon = 0.0000000001
                if v.Length > epsilon:
                    c = normalXY.dot(normalDatum)
                    s = v.normalize()
                    vx = array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
                    R = eye(3) + vx + vx.dot(vx) * ((1 - c) / (s.dot(s)))
                    rotation = App.Rotation(*R.reshape(9))
                    datumPlane.AttachmentOffset = App.Placement(face.CenterOfMass,App.Rotation(rotation.Axis, rotation.Angle * 180 / pi))
                else:
                    datumPlane.AttachmentOffset = App.Placement(face.CenterOfMass,App.Rotation(App.Vector(0,0,0), 0))

                datumPlane.recompute()
            else:
                App.Console.PrintWarning("You must choose one face and one datum Plane\n")
        else:
            App.Console.PrintWarning("You must choose one face and one datum Plane\n")
    else:
        App.Console.PrintWarning("You must choose one face and one datum Plane\n")
else:
    App.Console.PrintWarning("You must choose one face and one datum Plane\n")