# --coding=utf-8--

import vtk
import math
import tf
import kdl
import linecache
from scipy.spatial.transform import Rotation as R


# true_data = [[0.9954, 0.0140, 0.0440, -0.0840],
# [0.9855, 0.0565, 0.0520, -0.1510],
# [0.9937, 0.0524, 0.0982, -0.0102],
# [0.9757, 0.0265, 0.0877, -0.1990],
# [-0.3800, 0.0817, -0.3384, 0.8570]]

# calculated_data = [[0.9879, 0.0503, 0.0475, -0.1387],
# [0.9525, 0.1822, 0.0902, 0.2267],
# [0.9850, -0.0458, 0.1657, 0.0115],
# [0.7801, 0.0150, 0.3346, -0.5285],
# [0.9984, -0.0244, 0.0280, 0.0426]]


def q2e(w, x, y, z):
    # r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    # temp1 = w * y
    # temp2 = z * z
    # p = math.asin(2 * (temp1 - temp2))
    # return 180 * r, 180 * p, 180 * y

    r = R.from_quat([w, x, y, z])
    euler = r.as_euler('xyz', degrees=True)
    return euler


def xyz_axes(origin_point, line_length, line_width):
    line_x = vtk.vtkLineSource()
    line_y = vtk.vtkLineSource()
    line_z = vtk.vtkLineSource()
    line_x.SetPoint1(origin_point[0], origin_point[1], origin_point[2])
    line_y.SetPoint1(origin_point[0], origin_point[1], origin_point[2])
    line_z.SetPoint1(origin_point[0], origin_point[1], origin_point[2])
    line_x.SetPoint2(origin_point[0] + line_length, origin_point[1], origin_point[2])
    line_y.SetPoint2(origin_point[0], origin_point[1] + line_length, origin_point[2])
    line_z.SetPoint2(origin_point[0], origin_point[1], origin_point[2] + line_length)

    append = vtk.vtkAppendPolyData()
    append.AddInputConnection(line_x.GetOutputPort())
    append.AddInputConnection(line_y.GetOutputPort())
    append.AddInputConnection(line_z.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(append.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    mapper_x = vtk.vtkPolyDataMapper()
    mapper_y = vtk.vtkPolyDataMapper()
    mapper_z = vtk.vtkPolyDataMapper()
    mapper_x.SetInputConnection(line_x.GetOutputPort())
    mapper_y.SetInputConnection(line_y.GetOutputPort())
    mapper_z.SetInputConnection(line_z.GetOutputPort())

    actor_x = vtk.vtkActor()
    actor_y = vtk.vtkActor()
    actor_z = vtk.vtkActor()

    actor_x.SetMapper(mapper_x)
    actor_y.SetMapper(mapper_y)
    actor_z.SetMapper(mapper_z)

    actor_x.GetProperty().SetColor(1, 0, 0)
    actor_y.GetProperty().SetColor(0, 1, 0)
    actor_z.GetProperty().SetColor(0, 0, 1)

    actor_x.GetProperty().SetLineWidth(line_width)
    actor_y.GetProperty().SetLineWidth(line_width)
    actor_z.GetProperty().SetLineWidth(line_width)

    # text_property = vtk.vtkTextProperty()
    # text_property.SetColor(1,1,1)
    # text_property.SetFontSize(18)
    # actor_text_x = vtk.vtkActor()
    # actor_text_y = vtk.vtkActor()
    # actor_text_z = vtk.vtkActor()

    # text_x = vtk.vtkVectorText()
    # text_y = vtk.vtkVectorText()
    # text_z = vtk.vtkVectorText()
    # text_x.SetText(str(text1))
    # text_y.SetText(str(text2))
    # text_z.SetText(str(text3))
    # mapper_text_x = vtk.vtkPolyDataMapper()
    # mapper_text_y = vtk.vtkPolyDataMapper()
    # mapper_text_z = vtk.vtkPolyDataMapper()
    # mapper_text_x.SetInputConnection(text_x.GetOutputPort())
    # mapper_text_y.SetInputConnection(text_y.GetOutputPort())
    # mapper_text_z.SetInputConnection(text_z.GetOutputPort())
    # actor_text_x = vtk.vtkActor()
    # actor_text_y = vtk.vtkActor()
    # actor_text_z = vtk.vtkActor()
    # actor_text_x.SetMapper(mapper_text_x)
    # actor_text_y.SetMapper(mapper_text_y)
    # actor_text_z.SetMapper(mapper_text_z)
    # actor_text_x.SetPosition(origin_point[0] + line_length, origin_point[1], origin_point[2])
    # actor_text_y.SetPosition(origin_point[0], origin_point[1] + line_length, origin_point[2])
    # actor_text_z.SetPosition(origin_point[0], origin_point[1], origin_point[2] + line_length)
    # actor_text_x.SetScale(10,10,10)
    # actor_text_y.SetScale(10,10,10)
    # actor_text_z.SetScale(10,10,10)
    return actor_x, actor_y, actor_z


def main(m):
    # 导入数据
    # for n in range(1400):
    # 	n = n + 1000
    # 	print(n)
    n = m + 1

    # model_offset_1 = -38
    # model_offset_2 = -16

    model_offset_1 = -100
    model_offset_2 = -125
    model_offset_3 = -16

    true_value = linecache.getline('fake_data.txt', m)
    calculated_value = linecache.getline('fake_data.txt', n)

    # temp = true_value.split()
    # # (r1, p1, y1) = q2e(float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]))
    # (r1, p1, y1) = q2e(1, 0, 0, 0)
    # temp = calculated_value.split()
    # (r2, p2, y2) = q2e(0.5, 0.3, 0, 0)

    (r1, p1, y1) = (0, 0, 0)
    (r2, p2, y2) = (-90, 0, 0)

    # temp = true_value.split()
    # print(q2e(float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3])))
    # (r1, p1, y1) = tf.transformations.euler_from_quaternion([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3])])
    # (r1, pi, y1) = (-180 * r1 / math.pi, 180 * p1 / math.pi, 180 * y1 / math.pi)
    # print(r1, p1, y1)
    # temp = calculated_value.split()
    # (r2, p2, y2) = tf.transformations.euler_from_quaternion([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3])])
    # (r2, p2, y2) = (-180 * r2 / math.pi, 180 * p2 / math.pi, 180 * y2 / math.pi)
    # print(r2, p2, y2)
    # (r2, p2, y2) = tf.transformations.euler_from_quaternion(calculated_data[n+2])

    # r1,p1,y1 = q2e(true_data[n][0], true_data[n][1], true_data[n][2], true_data[n][3])
    # r2,p2,y2 = q2e(calculated_data[n][0], calculated_data[n][1], calculated_data[n][2], calculated_data[n][3])
    # r1,p1,y1 = q2e(1,0,0,0)
    # r2,p2,y2 = q2e(1,0,0,0)
    # print('1->True Posture')
    # print('2->Calculated Posture')
    # print(r1,p1,y1)
    # print(r2,p2,y2)

    # 导入模型
    reader1 = vtk.vtkSTLReader()
    reader1.SetFileName('probe.STL')
    reader2 = vtk.vtkSTLReader()
    reader2.SetFileName('probe.STL')

    transform = vtk.vtkTransform()
    transform.Translate(model_offset_1, model_offset_2, model_offset_3)
    # transform.RotateX(-90)

    transformFilter1 = vtk.vtkTransformPolyDataFilter()
    transformFilter1.SetInputConnection(reader1.GetOutputPort())
    transformFilter1.SetTransform(transform)
    transformFilter1.Update()

    transformFilter2 = vtk.vtkTransformPolyDataFilter()
    transformFilter2.SetInputConnection(reader2.GetOutputPort())
    transformFilter2.SetTransform(transform)
    transformFilter2.Update()

    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputConnection(transformFilter1.GetOutputPort())
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(transformFilter2.GetOutputPort())

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    # actor1.GetProperty().SetColor(255/255.0,215/255.0,0/255.0)
    actor1.GetProperty().SetColor(175 / 255.0, 215 / 255.0, 233 / 255.0)
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(150 / 255.0, 150 / 255.0, 150 / 255.0)

    # print(actor1.GetProperty())
    actor1.GetProperty().SetOpacity(1)
    actor2.GetProperty().SetOpacity(0.4)
    # 零件的坐标轴
    actor_x0, actor_y0, actor_z0 = xyz_axes([0, 120, 80], 50, 5)
    actor_x1, actor_y1, actor_z1 = xyz_axes([0, 0, 128], 40, 5)
    actor_x2, actor_y2, actor_z2 = xyz_axes([0, 0, 128], 40, 5)

    # actor_x_text = vtk.vtkTextActor()
    # actor_y_text = vtk.vtkTextActor()
    # actor_z_text = vtk.vtkTextActor()
    # actor_x_text.SetInput('X')
    # actor_y_text.SetInput('Y')
    # actor_z_text.SetInput('Z')
    # actor_x_text.SetPosition(0,0,0)
    # actor_x_text.SetPosition(0,0,0)
    # actor_x_text.SetPosition(0,0,0)

    # actor_axes_1 = xyz_axes([38,0,128],40)
    # line_x1 = vtk.vtkLineSource()
    # line_y1 = vtk.vtkLineSource()
    # line_z1 = vtk.vtkLineSource()
    # line_x1.SetPoint1(0,0,0)
    # line_x1.SetPoint2(100,0,0)
    # line_y1.SetPoint1(0,0,0)
    # line_y1.SetPoint2(0,100,0)
    # line_z1.SetPoint1(0,0,0)
    # line_z1.SetPoint2(0,0,100)
    # mapper_x1 = vtk.vtkPolyDataMapper()
    # mapper_x1.SetInputConnection(line_x1.GetOutputPort())
    # mapper_y1 = vtk.vtkPolyDataMapper()
    # mapper_y1.SetInputConnection(line_y1.GetOutputPort())
    # mapper_z1 = vtk.vtkPolyDataMapper()
    # mapper_z1.SetInputConnection(line_z1.GetOutputPort())
    # actor_x1 = vtk.vtkActor()
    # actor_x1.SetMapper(mapper_x1)
    # actor_y1 = vtk.vtkActor()
    # actor_y1.SetMapper(mapper_y1)
    # actor_z1 = vtk.vtkActor()
    # actor_z1.SetMapper(mapper_z1)
    # merge = vtk.vtkMergeFilter()
    # merge.SetGeometryConnection(line_x1.GetOutputPort())
    # merge.SetGeometryConnection(line_y1.GetOutputPort())
    # merge.SetGeometryConnection(line_z1.GetOutputPort())
    # append = vtk.vtkAppendPolyData()
    # append.AddInputConnection(line_x1.GetOutputPort())
    # append.AddInputConnection(line_y1.GetOutputPort())
    # append.AddInputConnection(line_z1.GetOutputPort())
    # mapper_merge = vtk.vtkPolyDataMapper()
    # mapper_merge.SetInputConnection(append.GetOutputPort())
    # actor_merge = vtk.vtkActor()
    # actor_merge.SetMapper(mapper_merge)

    actor1.RotateZ(y1)
    actor1.RotateY(p1)
    actor1.RotateX(r1)

    actor2.RotateZ(y2)
    actor2.RotateY(p2)
    actor2.RotateX(r2)

    actor_x1.RotateZ(y1)
    actor_x1.RotateY(p1)
    actor_x1.RotateX(r1)

    actor_y1.RotateZ(y1)
    actor_y1.RotateY(p1)
    actor_y1.RotateX(r1)

    actor_z1.RotateZ(y1)
    actor_z1.RotateY(p1)
    actor_z1.RotateX(r1)

    actor_x2.RotateZ(y2)
    actor_x2.RotateY(p2)
    actor_x2.RotateX(r2)

    actor_y2.RotateZ(y2)
    actor_y2.RotateY(p2)
    actor_y2.RotateX(r2)

    actor_z2.RotateZ(y2)
    actor_z2.RotateY(p2)
    actor_z2.RotateX(r2)

    camera = vtk.vtkCamera()
    camera.SetPosition(10, 10, 10)
    camera.SetFocalPoint(0, 0, 0)
    camera.Roll(-120)

    axes = vtk.vtkAxesActor()
    axes.SetPosition(0, 0, 0)
    axes.SetTotalLength(50, 50, 50)
    axes.SetShaftType(1)
    axes.SetAxisLabels(1)
    axes.SetCylinderRadius(0.02)
    axes_transform = vtk.vtkTransform()
    axes_transform.Translate(0, 50, 0)
    axes.SetUserTransform(axes_transform)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor1)
    ren.AddActor(actor2)
    ren.AddActor(actor_x0)
    ren.AddActor(actor_y0)
    ren.AddActor(actor_z0)
    ren.AddActor(actor_x1)
    ren.AddActor(actor_y1)
    ren.AddActor(actor_z1)
    ren.AddActor(actor_x2)
    ren.AddActor(actor_y2)
    ren.AddActor(actor_z2)
    # ren.AddActor(actor_x_text)
    # ren.AddActor(actor_y_text)
    # ren.AddActor(actor_z_text)
    ren.SetActiveCamera(camera)
    ren.ResetCamera()
    ren.SetBackground(200 / 255.0, 200 / 255.0, 200 / 255.0)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    renWin.Render()


# wif = vtk.vtkWindowToImageFilter()
# wif.SetInput(renWin)
# writer = vtk.vtkJPEGWriter()
# writer.SetFileName('test.jpg')
# writer.SetInputConnection(wif.GetOutputPort())
# writer.Write()


# wif = vtk.vtkWindowToImageFilter()
# wif.SetInput(renWin)
# wif.SetScale(2)
# wif.SetMagnification(2)
# wif.SetInputBufferTypeToRGBA()
# wif.ReadFrontBufferOff()
# wif.Update()
# bmpw = vtk.vtkBMPWriter()
# bmpw.SetInputConnection(wif.GetOutputPort())
# bmpw.SetFileName("test")
# bmpw.SetFilePattern('bmp')
# bmpw.Write()


for m in [2, 3, 4, 5, 6]:
    print(m)
    m = m + 1
    main(m)
