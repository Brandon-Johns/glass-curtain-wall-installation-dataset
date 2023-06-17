classdef CVm_ImportData < handle
% This class provides helpers to import the
%     images
%     motion capture data
% 
% It also holds the
%     camera calibration
%     experimental parameters

properties (SetAccess=private)
    numImages          % number of images in the dataset
    CameraCalibration  % struct holding the camera calibration data
    ExperimentalParams % struct holding the experimental parameters
end
properties (Access=private)
    imageStore
    mocapTable
end
methods
    %**********************************************************************
    % Create / Initialise
    %***********************************
    function this = CVm_ImportData()
        % Loads the data
        % Contains hard coded paths to the data

        % Full path to this file (no matter where it is called from)
        [pathHere_Dir,~,~] = fileparts( mfilename('fullpath') );

        % Path to data
        pathImages_Dir = fullfile(pathHere_Dir,"..","dataset","images");
        pathCSV = fullfile(pathHere_Dir,"..","dataset","MotionCaptureData.csv");

        this.imageStore = datastore(pathImages_Dir, "Type","image");
        this.mocapTable = readtable(pathCSV, "Delimiter",",");
        this.numImages = size(this.mocapTable,1);
    end

    %**********************************************************************
    % Import Data
    %***********************************
    function I = ImportImage(this, imageNumber)
        % Import an image from the dataset
        % INPUT
        %   imageNumber = the number in the image's file name
        arguments
            this(1,1)
            imageNumber(1,1) uint32
        end
        mustBeInRange(imageNumber, 1,this.numImages);
        I = imread( this.imageStore.Files{imageNumber} );
        I = im2double(I);
    end

    function T_W_C = ImportMocap_relWall(this, imageNumber)
        % Returns the transformation: wall reference frame <- camera reference frame
        % INPUT
        %   imageNumber = the number in the image's file name
        arguments
            this(1,1)
            imageNumber(1,1) uint32
        end
        mustBeInRange(imageNumber, 1,this.numImages);
        q_wxyz = this.mocapTable{imageNumber, ["qw","qx","qy","qz"]};
        P = this.mocapTable{imageNumber, ["x","y","z"]}.';
        T_W_C = CVm_T().set_quat_wxyz(q_wxyz).set_P(P);
    end

    function T_C_W = ImportMocap_relCamera(this, imageNumber)
        % Returns the transformation: camera reference frame <- wall reference frame
        % INPUT
        %   imageNumber = the number in the image's file name
        T_C_W = this.ImportMocap_relWall(imageNumber).inv;
    end

    %********************************************************************************************************
    % Get properties
    %****************************************************
    function out = get.CameraCalibration(~)
        % Camera calibration parameters
        out = struct;

        % Radial Distortion Coefficients
        out.k1 = -0.1552775701035;
        out.k2 = 0.0472686081157939;
        out.k3 = 0;
        % Tangential Distortion Coefficients
        out.p1 = 0;
        out.p2 = 0;

        % Focal Length [px]
        out.fx = 1821.04993399032;
        out.fy = 1817.92066001349;
        % Principal Point [px]
        out.cx = 741.82871031754;
        out.cy = 1019.94855509992;
        % Skew
        out.s = 0;

        % Image Dimensions [px]
        out.ImageHeight = 2048;
        out.ImageWidth  = 1536;

        % Units of measure for world coordinates
        out.WorldUnits = 'millimeters';

        % Intrinsic Matrix
        out.K = [out.fx,out.s,out.cx; 0,out.fy,out.cy; 0,0,1];
    end

    function out = get.ExperimentalParams(~)
        % Parameters of experimental setup
        out = struct;

        % Size of individual panel [mm]
        % Dimensions including the aluminium frame
        out.panelH = 153.2;
        out.panelW = 103.2;
        % Dimensions of the exposed glass
        out.panelH_inner = 143.2;
        out.panelW_inner = 93.2;

        % Height from top of panel to the next concrete floor slab [mm]
        out.panelTopAboveFloor = 129;
    end
end
end

