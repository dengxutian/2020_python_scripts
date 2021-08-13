# @Time : 2021/7/19 2:01
# @Author : Deng Xutian
# @Email : dengxutian@126.com

import vtk
import math
import time
import numpy as np


def q2e(w, x, y, z):
    r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    p = math.asin(2 * (w * y - z * x))
    y = math.atan2(2 * (w * z + x * y), 1 - 2 * (z * z + y * y))

    angleR = r * 180 / math.pi
    angleP = p * 180 / math.pi
    angleY = y * 180 / math.pi

    return angleR, angleP, angleY


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

    return actor_x, actor_y, actor_z


def draw(w, x, y, z, file_index):
    model_offset_1 = -100
    model_offset_2 = -125
    model_offset_3 = -16

    # model_offset_1 = -38
    # model_offset_2 = -16
    # model_offset_3 = 0

    # (r1, p1, y1) = tf.transformations.euler_from_quaternion([w, x, y, z])
    # (r1, pi, y1) = (-180 * r1 / math.pi, 180 * p1 / math.pi, 180 * y1 / math.pi)
    r1, p1, y1 = q2e(w, x, y, z)
    print(r1, p1, y1)

    reader = vtk.vtkSTLReader()
    reader.SetFileName('probe.STL')

    transform = vtk.vtkTransform()
    transform.Translate(model_offset_1, model_offset_2, model_offset_3)
    transform.RotateX(-90)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(reader.GetOutputPort())
    transformFilter.SetTransform(transform)
    transformFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transformFilter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(175 / 255.0, 215 / 255.0, 233 / 255.0)

    actor.GetProperty().SetOpacity(1)

    # 零件的坐标轴
    actor_x0, actor_y0, actor_z0 = xyz_axes([0, 120, 80], 50, 5)
    actor_x, actor_y, actor_z = xyz_axes([38, 15, 0], 40, 5)

    actor.RotateZ(y1)
    actor.RotateY(p1)
    actor.RotateX(r1)

    actor_x.RotateZ(y1)
    actor_x.RotateY(p1)
    actor_x.RotateX(r1)

    actor_y.RotateZ(y1)
    actor_y.RotateY(p1)
    actor_y.RotateX(r1)

    actor_z.RotateZ(y1)
    actor_z.RotateY(p1)
    actor_z.RotateX(r1)

    camera = vtk.vtkCamera()
    camera.SetClippingRange(1, 1)
    camera.SetViewUp(0, 0, 0)
    camera.SetPosition(10, 10, 10)
    camera.SetFocalPoint(0, 0, 0)
    camera.Roll(-120)
    camera.ComputeViewPlaneNormal()

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
    ren.AddActor(actor)
    ren.AddActor(actor_x0)
    ren.AddActor(actor_y0)
    ren.AddActor(actor_z0)
    ren.AddActor(actor_x)
    ren.AddActor(actor_y)
    ren.AddActor(actor_z)

    ren.SetActiveCamera(camera)
    ren.ResetCamera()
    ren.SetBackground(200 / 255.0, 200 / 255.0, 200 / 255.0)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()

    # iren = vtk.vtkRenderWindowInteractor()
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # iren.Start()

    wif = vtk.vtkWindowToImageFilter()
    wif.SetInput(renWin)
    writer = vtk.vtkJPEGWriter()
    writer.SetFileName(str(file_index) + '.jpg')
    writer.SetInputConnection(wif.GetOutputPort())
    writer.Write()
    # iren.Start()

    # wif = vtk.vtkWindowToImageFilter()
    # wif.SetInput(renWin)
    # wif.SetScale(2)
    # # wif.SetMagnification(2)
    # wif.SetInputBufferTypeToRGBA()
    # wif.ReadFrontBufferOff()
    # wif.Update()
    #
    # bmpw = vtk.vtkBMPWriter()
    # bmpw.SetInputConnection(wif.GetOutputPort())
    # bmpw.SetFileName("test.avi")
    # bmpw.Write()
    #
    # iren.Start()
    #
    # bmpw.End()


def draw_test():
    # model_offset_1 = -100
    # model_offset_2 = -125
    # model_offset_3 = -16

    model_offset_1 = -38
    model_offset_2 = -16
    model_offset_3 = 128

    # (r1, p1, y1) = tf.transformations.euler_from_quaternion([w, x, y, z])
    # (r1, pi, y1) = (-180 * r1 / math.pi, 180 * p1 / math.pi, 180 * y1 / math.pi)
    r1, p1, y1 = (0, 0, 0)

    reader = vtk.vtkSTLReader()
    reader.SetFileName('probe.STL')

    transform = vtk.vtkTransform()
    transform.Translate(model_offset_1, model_offset_2, model_offset_3)
    transform.RotateX(-90)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(reader.GetOutputPort())
    transformFilter.SetTransform(transform)
    transformFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transformFilter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(220 / 255.0, 220 / 255.0, 220 / 255.0)

    actor.GetProperty().SetOpacity(0.6)

    # 零件的坐标轴
    # actor_x0, actor_y0, actor_z0 = xyz_axes([0, 120, 80], 50, 5)
    actor_x0, actor_y0, actor_z0 = xyz_axes([0, 0, 0], 50, 5)
    actor_x, actor_y, actor_z = xyz_axes([model_offset_1 + 38, model_offset_2 + 15, model_offset_3 + 1], 40, 5)

    actor.RotateZ(y1)
    actor.RotateY(p1)
    actor.RotateX(r1)

    actor_x.RotateZ(y1)
    actor_x.RotateY(p1)
    actor_x.RotateX(r1)

    actor_y.RotateZ(y1)
    actor_y.RotateY(p1)
    actor_y.RotateX(r1)

    actor_z.RotateZ(y1)
    actor_z.RotateY(p1)
    actor_z.RotateX(r1)

    camera = vtk.vtkCamera()
    camera.SetClippingRange(1, 1)
    camera.SetViewUp(0, 0, 0)
    camera.SetPosition(10, 10, 10)
    camera.SetFocalPoint(0, 0, 0)
    camera.Roll(-120)
    camera.ComputeViewPlaneNormal()

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
    ren.AddActor(actor)
    ren.AddActor(actor_x0)
    ren.AddActor(actor_y0)
    ren.AddActor(actor_z0)
    ren.AddActor(actor_x)
    ren.AddActor(actor_y)
    ren.AddActor(actor_z)

    ren.SetActiveCamera(camera)
    ren.ResetCamera()
    ren.SetBackground(0 / 255.0, 0 / 255.0, 0 / 255.0)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1920, 1080)
    renWin.Render()

    # iren = vtk.vtkRenderWindowInteractor()
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # iren.Start()

    wif = vtk.vtkWindowToImageFilter()
    wif.SetInput(renWin)
    wif.Update()

    writer = vtk.vtkOggTheoraWriter()
    writer.SetFileName('test.ogv')
    writer.SetInputConnection(wif.GetOutputPort())
    writer.Start()
    writer.Write()

    pose_list = np.loadtxt('fake_e.txt')
    for i in range(1000):
        r1, p1, y1 = pose_list[i][2] / math.pi, pose_list[i][1] / math.pi, pose_list[i][0] / math.pi
        r1, p1, y1 = r1/2, p1/2, y1/2

        actor.RotateZ(y1)
        actor.RotateY(p1)
        actor.RotateX(r1)

        actor_x.RotateZ(y1)
        actor_x.RotateY(p1)
        actor_x.RotateX(r1)

        actor_y.RotateZ(y1)
        actor_y.RotateY(p1)
        actor_y.RotateX(r1)

        actor_z.RotateZ(y1)
        actor_z.RotateY(p1)
        actor_z.RotateX(r1)

        renWin.Render()

        wif.Modified()
        writer.Write()

        print(time.time())
        # time.sleep(0.01)
    writer.End()

    # wif = vtk.vtkWindowToImageFilter()
    # wif.SetInput(renWin)
    # wif.SetScale(2)
    # # wif.SetMagnification(2)
    # wif.SetInputBufferTypeToRGBA()
    # wif.ReadFrontBufferOff()
    # wif.Update()
    #
    # bmpw = vtk.vtkBMPWriter()
    # bmpw.SetInputConnection(wif.GetOutputPort())
    # bmpw.SetFileName("test.avi")
    # bmpw.Write()
    #
    # iren.Start()
    #
    # bmpw.End()


if __name__ == '__main__':
    # pose_list = np.loadtxt('fake_data.txt')
    # for i in range(1000):
    #     draw(pose_list[i][1], pose_list[i][2], pose_list[i][3], pose_list[i][4], file_index = i)

    draw_test()
