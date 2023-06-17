# Written By: Brandon Johns
# Date Version Created: 2023-06-15
# Date Last Edited: 2023-06-15
# Status: functional
# Project: Glass Curtain Wall Installation Dataset

# %%% PURPOSE %%%
# Demonstrate the relationship between the images, camera calibration, and motion capture data

# INPUT:
#   An image from the dataset
#   The coordinates of an arbitrary point, as measured in the wall coordinate frame (W).

# INTERNALS:
# 1) The motion capture data is used to find coordinates of the input point
#     as measured in the camera coordinate frame (C).
# 2) The camera calibration is then used to find the pixel coordinates of the point
#     with respect to the original (distorted) image.

# OUTPUT:
#   The input point is drawn on the image.

import matplotlib
import numpy

from CVm_T import CVm_T
from CVm_ImportData import CVm_ImportData


def WorldToImage(cal, T_C_W, P):
    #**********************************************************************
    # Convert user provided point to as measured in the camera coordinate frame
    #***********************************
    # Notation for homogeneous transformation matrix: T_frameOld_frameNew
    T_W_UserPoint = CVm_T().set_P(P)
    T_C_UserPoint = T_C_W @ T_W_UserPoint

    # Point as measured in the camera coordinate frame
    Xc = T_C_UserPoint.x
    Yc = T_C_UserPoint.y
    Zc = T_C_UserPoint.z


    #**********************************************************************
    # Convert user provided point to as measured in pixel coordinates
    #   with respect to the original (distorted) image
    #***********************************
    # K: Intrinsic Matrix
    # k: Radial Distortion Coefficients
    K = cal.K
    k1 = cal.k1
    k2 = cal.k2
    k3 = cal.k3
    r2 = (Xc/Zc)**2 + (Yc/Zc)**2
    alpha = 1 + k1*r2 + k2*(r2**2) + k3*(r2**3)
    uv_distorted = K @ numpy.array([[(Xc/Zc)*alpha], [(Yc/Zc)*alpha], [1]])

    # Pixel coordinates
    u_distorted = uv_distorted[0]
    v_distorted = uv_distorted[1]
    return (u_distorted, v_distorted)


data = CVm_ImportData()
params = data.ExperimentalParams
cal = data.CameraCalibration

#**********************************************************************
# User input
#***********************************
# Image number, according to the file name
imNum = 57

# Location of a point, as measured in the coordinate frame W. Specified as [x;y;z]
# Try different points to move along the wall
points = [
    (0, 0, 0),
    (0, params.panelH, 0),
    (params.panelW, params.panelH, 0),
    (params.panelW, 0, 0)
]


#**********************************************************************
# Automated
# Plot user provided points on the image
#***********************************
T_C_W = data.ImportMocap_relCamera(imNum)
I = data.ImportImage(imNum)

fig, ax = matplotlib.pyplot.subplots()
fig.dpi=300
ax.imshow(I)

for point in points:
    [u_d, v_d] = WorldToImage(cal, T_C_W, point)
    ax.plot(u_d, v_d, 'x', markersize=8)


