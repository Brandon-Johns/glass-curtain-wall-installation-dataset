import numpy
import scipy
import copy

class CVm_T:
    """
    Homogeneous transformation matrix (immutable class)

    It can be
    - constructed from / deconstructed into position and rotation components
    - multiplied with the * operator
    - inverted with the inv() method

    PROPERTIES
    T : 4x4 numpy.array = homogeneous transformation matrix

    # Deconstruct the transformation matrix into
    # Position
    x : float = x coordinate
    y : float = y coordinate
    z : float = z coordinate
    P : 1x3 numpy.array = position vector
    Ph : 1x4 numpy.array = homogeneous position vector

    # Rotation
    R : 3x3 numpy.array = rotation matrix
    quat_wxyz : 4x1 numpy.array = quaternion as [w,x,y,z]
    quat_xyzw : 4x1 numpy.array = quaternion as [x,y,z,w]
    """
    #**********************************************************************
    # Create
    #***********************************
    def __init__(self, T=numpy.identity(4)):
        """
        EXAMPLE:
        a = CVm_T()
        a = CVm_T([[0,1,0,1],[1,0,0,2],[0,0,1,3],[0,0,0,1]])
        a = CVm_T().set_P([1;2;3]).set_R([0,1,0; 1,0,0; 0,0,1])
        """
        T = numpy.array(T)
        assert T.shape==(4,4), "Input must be a 4x4 matrix"
        self.T = T

    # Construct from components
    def set_x(self,val):  out=copy.copy(self.T); out[0,3]=val; return CVm_T(out)
    def set_y(self,val):  out=copy.copy(self.T); out[1,3]=val; return CVm_T(out)
    def set_z(self,val):  out=copy.copy(self.T); out[2,3]=val; return CVm_T(out)
    def set_P(self,val):
        if isinstance(val, numpy.ndarray): val = val.squeeze()
        out=copy.copy(self.T)
        out[0:3,3]=val
        return CVm_T(out)
    def set_Ph(self,val):
        if isinstance(val, numpy.ndarray): val = val.squeeze()
        out=copy.copy(self.T)
        out[:,3]=val
        return CVm_T(out)
    def set_R(self,val):  out=copy.copy(self.T); out[0:3,0:3]=val; return CVm_T(out)

    # Construct from quaternions
    def set_quat_wxyz(self, q_wxyz):
        q_xyzw = numpy.take(q_wxyz, [1,2,3,0])
        out=copy.copy(self.T)
        out[0:3,0:3] = scipy.spatial.transform.Rotation.from_quat(q_xyzw).as_matrix()
        return CVm_T(out)

    def set_quat_xyzw(self, q_xyzw):
        out=copy.copy(self.T)
        out[0:3,0:3] = scipy.spatial.transform.Rotation.from_quat(q_xyzw).as_matrix()
        return CVm_T(out)


    #********************************************************************************************************
    # Get properties
    #****************************************************
    # Deconstruct into position and rotation components
    @property
    def x(self):  return self.T[0,3]
    @property
    def y(self):  return self.T[1,3]
    @property
    def z(self):  return self.T[2,3]
    @property
    def P(self):  return copy.copy(self.T[0:3,[3]])
    @property
    def Ph(self): return copy.copy(self.T[:,[3]])
    @property
    def R(self):  return copy.copy(self.T[0:3,0:3])

    # Convert to quaternions
    @property
    def quat_wxyz(self):
        return scipy.spatial.transform.Rotation.from_matrix(self.R).as_quat()
    @property
    def quat_xyzw(self):
        return self.quat_xyzw().take([3,0,1,2])


    #**********************************************************************
    # Operator Overloads
    #***********************************
    def inv(self):
        """
        Matrix inverse

        This function uses mathematical properties of T => cleaner & more efficient than T^-1

        OUTPUT: A new object of type CVm_T, which is the inverse of T
        """
        R_inv = self.R.T
        P_inv = -R_inv @ self.P
        T_inv = CVm_T().set_R(R_inv).set_P(P_inv)
        return T_inv

    def __matmul__(self, other):
        """
        Matrix multiplication: result = self @ other

        INPUT: CVm_T, 4x4 numpy.array, 4x1 numpy.array
        OUTPUT:
            CVm_T
            4x1 numpy.array for the case of input (4x1 numpy.array)
        """
        if isinstance(other, self.__class__):
            return CVm_T(self.T @ other.T)
        elif isinstance(other, numpy.ndarray) and other.shape==(4,4):
            return CVm_T(self.T @ other)
        elif isinstance(other, numpy.ndarray) and other.shape==(4,1):
            return self.T @ other
        else:
            raise TypeError("Bad term on right hand side of multiplication")

    def __imatmul__(self, other):
        """
        Matrix multiplication: self @= other

        Identical behaviour to __matmul__
        """
        if isinstance(other, self.__class__):
            return CVm_T(self.T @ other.T)
        elif isinstance(other, numpy.ndarray) and other.shape==(4,4):
            return CVm_T(self.T @ other)
        elif isinstance(other, numpy.ndarray) and other.shape==(4,1):
            return self.T @ other
        else:
            raise TypeError("Bad term on right hand side of multiplication")

    def __rmatmul__(self, other):
        """
        Matrix multiplication: result = other @ self

        INPUT: CVm_T, 4x4 numpy.array
        OUTPUT: CVm_T
        """
        if isinstance(other, self.__class__):
            return CVm_T(other.T @ self.T)
        elif isinstance(other, numpy.ndarray) and other.shape==(4,4):
            return CVm_T(other @ self.T)
        else:
            raise TypeError("Bad term on left hand side of multiplication")
