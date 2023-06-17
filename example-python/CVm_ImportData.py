import pathlib
import PIL
import natsort
import pandas
import numpy

from CVm_T import CVm_T

class CVm_ImportData:
    """
    This class provides helpers to import the
    - images
    - motion capture data

    It also holds the
    - camera calibration
    - experimental parameters

    PROPERTIES
    numImages
    CameraCalibration
    ExperimentalParams
    """
    #**********************************************************************
    # Create / Initialise
    #***********************************
    def __init__(self):
        """
        Load the data
        All paths are hardcoded into this init function only
        """
        imagePaths = pathlib.Path("../dataset/images").glob('*.png')
        imagePaths = [x for x in imagePaths if x.is_file()]
        imagePaths = natsort.natsorted(imagePaths, key=str)

        pathCSV = pathlib.Path("../dataset/MotionCaptureData.csv")

        assert len(imagePaths)>0, "Not found: images"
        assert pathCSV.exists(), "Not found: MotionCaptureData.csv"

        self.imagePaths = imagePaths
        self.mocapTable = pandas.read_csv(pathCSV)
        self.numImages = len(imagePaths)

        assert self.mocapTable.shape[0] == len(imagePaths), "Number of rows of MotionCaptureData.csv does not match number of images"
        assert self.mocapTable.shape[1] == 8, "Incorrect number of rows in MotionCaptureData.csv"


    #**********************************************************************
    # Import Data
    #***********************************
    def ImportImage(self, imageNumber):
        """
        Import image as a PIL.Image

        INPUT
        imageNumber = the number in the image's file name
        """
        imageNumber = int(imageNumber)
        assert 1<=imageNumber<=self.numImages, "Image number out of range"
        return PIL.Image.open(self.imagePaths[imageNumber-1])

    def ImportMocap_relWall(self, imageNumber):
        """
        Returns the transformation: wall reference frame <- camera reference frame

        INPUT
        imageNumber = the number in the image's file name
        """
        imageNumber = int(imageNumber)
        assert 1<=imageNumber<=self.numImages, "Image number out of range"
        q_wxyz = self.mocapTable.loc[imageNumber-1, ["qw","qx","qy","qz"]]
        P = self.mocapTable.loc[imageNumber-1, ["x","y","z"]]
        return CVm_T().set_quat_wxyz(q_wxyz).set_P(P)

    def ImportMocap_relCamera(self, imageNumber):
        """
        Returns the transformation: camera reference frame <- wall reference frame

        INPUT
        imageNumber = the number in the image's file name
        """
        return self.ImportMocap_relWall(imageNumber).inv()

    #********************************************************************************************************
    # Get properties
    #****************************************************
    # Camera Calibration
    @property
    def CameraCalibration(self):
        class out: pass

        # Radial Distortion Coefficients
        out.k1 = -0.1552775701035
        out.k2 = 0.0472686081157939
        out.k3 = 0
        # Tangential Distortion Coefficients
        out.p1 = 0
        out.p2 = 0

        # Focal Length [px]
        out.fx = 1821.04993399032
        out.fy = 1817.92066001349
        # Principal Point [px]
        out.cx = 741.82871031754
        out.cy = 1019.94855509992
        # Skew
        out.s = 0

        # Image Dimensions [px]
        out.ImageHeight = 2048
        out.ImageWidth  = 1536

        # Units of measure for world coordinates
        out.WorldUnits = 'millimeters'

        # Intrinsic Matrix
        out.K = numpy.array([[out.fx,out.s,out.cx],[0,out.fy,out.cy],[0,0,1]])
        return out

    # Parameters of experimental setup
    @property
    def ExperimentalParams(self):
        class out: pass

        # Size of individual panel [mm]
        # Dimensions including the aluminium frame
        out.panelH = 153.2
        out.panelW = 103.2
        # Dimensions of the exposed glass
        out.panelH_inner = 143.2
        out.panelW_inner = 93.2

        # Height from top of panel to the next concrete floor slab [mm]
        out.panelTopAboveFloor = 129
        return out


