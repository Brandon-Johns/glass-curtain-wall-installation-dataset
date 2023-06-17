classdef CVm_T
% This class provides the Homogeneous transformation matrix
% 
% CONSTRUCTION
% Create identity matrix
%   a = CVm_T()
% Create from a 4x4 matrix that represents a transformation matrix
%   a = CVm_T([0,1,0,1; 1,0,0,2; 0,0,1,3; 0,0,0,1])
% Construct from components by chaining the set methods
%   a = CVm_T().set_P([1;2;3]).set_R([0,1,0; 1,0,0; 0,0,1])
%
% OVERLOADS
%   * operator: multiplication
%   inv(): invert
%   zeros(): create array of identity matrices
%
% DATA ACCESS
%   The properties deconstruct the matrix into position and rotation components
% 
% NOTE: Quaternion construction/deconstruction requires one of the following
%   Navigation Toolbox
%   Robotics System Toolbox
%   UAV Toolbox

properties
    T(4,4) % homogeneous transformation matrix
end
properties (Dependent)
    % Deconstruct the transformation matrix into position and rotation
    
    x  % x coordinate
    y  % y coordinate
    z  % z coordinate
    P  % position vector
    Ph % homogeneous position vector

    R         % rotation matrix
    quat_wxyz % quaternion as [w,x,y,z]
    quat_xyzw % quaternion as [x,y,z,w]
end
methods
    %**********************************************************************
    % Create
    %***********************************
    function this = CVm_T(T)
        arguments
            T(4,4) = eye(4);
        end
        this.T = T;
    end

    function this = set_x(this,val);  this.T(1,4) = val; end
    function this = set_y(this,val);  this.T(2,4) = val; end
    function this = set_z(this,val);  this.T(3,4) = val; end
    function this = set_P(this,val);  this.T(1:3,4) = val; end
    function this = set_Ph(this,val); this.T(:,4) = val; end
    function this = set_R(this,val);  this.T(1:3,1:3) = val; end

    function this = set_quat_wxyz(this, q_wxyz)
        this.T(1:3,1:3) = quat2rotm(q_wxyz);
    end
    function this = set_quat_xyzw(this, q_xyzw)
        q_wxyz = q_xyzw([4,1,2,3]);
        this.T(1:3,1:3) = quat2rotm(q_wxyz);
    end

    %********************************************************************************************************
    % Get properties
    %****************************************************
    % Deconstruct into position and rotation components
    function out = get.x(this);  out = this.T(1,4); end
    function out = get.y(this);  out = this.T(2,4); end
    function out = get.z(this);  out = this.T(3,4); end
    function out = get.P(this);  out = this.T(1:3,4); end
    function out = get.Ph(this); out = this.T(:,4); end
    function out = get.R(this);  out = this.T(1:3,1:3); end

    % Convert to quaternions
    function out = get.quat_wxyz(this)
        out = rotm2quat( this.T(1:3,1:3) );
    end
    function out = get.quat_xyzw(this)
        out = this.quat_wxyz([2,3,4,1]);
    end

    %**********************************************************************
    % Operator Overloads
    %***********************************
    function out = inv(this)
        % Matrix inverse
        % This function uses mathematical properties of T => cleaner & more efficient than T^-1
        % OUTPUT:
        %   A new object of type CVm_T, which is the inverse of T
        % EXAMPLE:
        %   a=CVm_T; b=inv(a)
        R_inv = this.R.';
        P_inv = -R_inv * this.P;
        out = CVm_T( [[R_inv,P_inv];[0,0,0,1]] );
    end

    function c = mtimes(a,b)
        % Matrix multiplication with the * operator
        % INPUT:
        %   a(1,1) CVm_T
        %   a(4,4) double | sym
        %   b(1,1) CVm_T
        %   b(4,4) double | sym
        %   b(1,4) double | sym
        % OUTPUT:
        %   c(:,:) CVm_T
        %   c(4,1) double | sym    For the case of b(1,4)
        % EXAMPLE:
        %   a=CVm_T; b=CVm_T; c=a*b
        %   a=CVm_T; b=[1;2;3,1]; c=a*b
        if isa(a, "CVm_T") && isscalar(a)
            a = a.T;
        elseif ~isa(a, "CVm_T") && all(size(a)==[4,4])
            % 'a' is good as is
        else
            error("Bad term on left hand side of multiplication");
        end

        if isa(b, "CVm_T") && isscalar(b)
            c = CVm_T(a * b.T);
        elseif ~isa(b, "CVm_T") && all(size(b)==[4,4])
            c = CVm_T(a * b);
        elseif ~isa(b, "CVm_T") && all(size(b)==[4,1])
            c = a * b;
        else
            error("Bad term on right hand side of multiplication");
        end
    end
end
methods (Static)
    function objectArray = zeros(varargin)
        % Create an array of default objects
        % INPUT:
        %   An array or comma separated list of the size of the array to create
        % EXAMPLE:
        %   objectArray = CVm_T.zeros([4,5]);
        %   objectArray = CVm_T.zeros(4,5);
        sizeArray = [varargin{:}];
        sizeAsCell = num2cell(sizeArray);
        objectArray(sizeAsCell{:}) = CVm_T();
    end
end
end
