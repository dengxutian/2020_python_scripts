#!/usr/bin/env python
# coding: utf-8

import cv2 as cv
import numpy as np
import math

class img_calibration():
    def __init__(self):
        self.zoom_factor = 0.4
        self.zero_point = [260, -50]
        self.mid_point = [260, 106]
        pass
    
    def callback(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            dx = (x - self.mid_point[0]) * self.zoom_factor
            dy = (y - self.mid_point[1]) * self.zoom_factor
            dx_ = (x - self.zero_point[0])
            dy_ = (y - self.zero_point[1])
            angle = math.atan(dx_/dy_)
            
            print('dx = %.2f' %dx)
            print('dy = %.2f' %dy)
            print('angle = ' + str(angle))
            
        pass
    
    def main_loop(self):
        cv.namedWindow('img')
        cv.setMouseCallback('img', self.callback)
        img = cv.imread('1.jpg')
        while True:
            cv.imshow('img', img)
            if cv.waitKey(10)&0xFF==27:
                break
        cv.destroyAllWindows()
        print('Finish!')
        pass

if __name__ == '__main__':
    demo = img_calibration()
    demo = img_calibration()
    demo.main_loop()