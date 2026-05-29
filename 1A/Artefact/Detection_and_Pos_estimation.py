import cv2
import numpy as np

def detection(marker_points2, marker_points10, arucoDetector, cam_param, frame) -> dict :
    '''
    Detects the ArUco markers from the 6x6_50 arUco dictionnary on a given frame and outputs a dictionnary
    which assign a dictionnary { "Coord", "Dist", "Angle" } to each marker ID detected.
    Coord is the coordinates (x, y) of the camera in a local base assigned to each markers.
    Dist is the distance to the marker
    Angle is the horizontal angle between the marker and the optical axis of the camera
    '''
    # Dictionnary described above
    DPose = {}
    # Detect ArUco markers in the input frame
    (corners, ids, rejected) = arucoDetector.detectMarkers(frame)
    if len(corners) > 0:
        # Flatten the ArUco IDs list
        ids = ids.flatten()
        # Offset to make the camera differentiate each markers of ID 0 so that they don't overwrite each other in DPose
        offset = 1
        # Loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # Get pos estimation with respect to aruco markers size and ID
            if markerID < 5 and markerID != 0:
                rt, rv, t = cv2.solvePnP(marker_points10, markerCorner, cam_param['mtx'], cam_param['dist'],
                                         cam_param['rvecs'], cam_param['tvecs'])
            else:
                rt, rv, t = cv2.solvePnP(marker_points2, markerCorner, cam_param['mtx'], cam_param['dist'],
                                         cam_param['rvecs'], cam_param['tvecs'])
                # If markerID is 0 we want to avoid overwrite so we offset starting at 50 because 50 is the
                # size of the ArUco dictionnary
                if markerID == 0:
                    markerID = 50 + offset
                    offset += 1

            DPose[markerID] = {
                                "Coord" : (t[0][0],  t[2][0]),
                                "Dist" : np.sqrt(t[0][0]**2 + t[1][0]**2 + t[2][0]**2),
                                "Angle" : np.arctan(t[0][0]/t[2][0])*180/np.pi
                              }
    return DPose
