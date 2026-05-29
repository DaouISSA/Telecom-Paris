import sys
import cv2
import numpy as np

def norm(vect):
    return float(np.sqrt(vect[0][0]**2+vect[1][0]**2+vect[2][0]**2))

# Array for markers of size 2cm
marker_points2 = np.array([[-2 / 2, 2 / 2, 0],
                                [2 / 2, 2 / 2, 0],
                                [2 / 2, -2 / 2, 0],
                                [-2 / 2, -2 / 2, 0]], dtype=np.float32)

# Array for markers of size 10cm
marker_points10 = np.array([[-10 / 2, 10 / 2, 0],
                                [10 / 2, 10 / 2, 0],
                                [10 / 2, -10 / 2, 0],
                                [-10 / 2, -10 / 2, 0]], dtype=np.float32)

# Dictionnaire des positions par rapport à un markerID donné
DPose = {}

# These are the matrix from the camera calibration
# Warning, the parameters are different for each camera, you'll have to compute them again if you were to change the camera.
# Use Camera_calibration.py for that
cam_param = np.load('/home/go4t/team5/Calibration/Cam_calib.npz')

# Dictionnary for arUco markers
ARUCO_DICT = {"DICT_6X6_50": cv2.aruco.DICT_6X6_50}

# Load the ArUCo dictionary and grab the ArUCo parameters
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT['DICT_6X6_50'])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

frame = cv2.imread(sys.argv[1])
# Detect ArUco markers in the input frame
(corners, ids, rejected) = arucoDetector.detectMarkers(frame)
if len(corners) > 0:
    # Flatten the ArUco IDs list
    ids = ids.flatten()
    # Loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # Extract the marker corners (which are always returned
        # in top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # Convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # Compute and draw the center (x, y)-coordinates of the ArUco marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        # Get pos estimation with respect to aruco markers size and ID
        if markerID < 5 and markerID != 0:
            rt, rv, t = cv2.solvePnP(marker_points10, markerCorner, cam_param['mtx'], cam_param['dist'],
                                     cam_param['rvecs'], cam_param['tvecs'])
        else:
            rt, rv, t = cv2.solvePnP(marker_points2, markerCorner, cam_param['mtx'], cam_param['dist'],
                                     cam_param['rvecs'], cam_param['tvecs'])
            
        # Dictionary associating the translation vector and distance to their aruco marker with respect to ID
        DPose[markerID] = str(cX) + " " +str(cY) + " " + str(norm(t)) + " " + str(np.arctan(t[0][0]/t[2][0])*180/np.pi)

for i in DPose.keys():
    print(str(i)+' '+DPose[i])
