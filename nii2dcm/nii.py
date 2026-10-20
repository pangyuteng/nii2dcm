"""
Classes for manipulating NIfTI files

Tom Roberts
"""

import numpy as np


class Nifti:

    def get_nii2dcm_parameters(nib_nii):
        """
        Get general NIfTI header parameters relevant for DICOM tag transferal.
        :nib_nii - NIfTI loaded with nibabel
        :nii_parameters - parameters to transfer to DICOM header
        """

        def fnT1N(A, N):
            # Subfn: calculate T1N vector
            # A = affine matrix [4x4]
            # N = slice number (counting from 1)
            T1N = A.dot([0, 0, N - 1, 1])
            return T1N

        # load nifti
        nii_img = nib_nii.get_fdata()

        # volume dimensions
        if nib_nii.header['dim'][4] == 1:
            nX, nY, nZ, nF = nib_nii.header['dim'][1], nib_nii.header['dim'][2], nib_nii.header['dim'][3], 1
            dimX, dimY, dimZ = nib_nii.header['pixdim'][1], nib_nii.header['pixdim'][2], nib_nii.header['pixdim'][3]

        elif nib_nii.header['dim'][0] == 3 and all([x > 1 for x in nib_nii.header['dim'][1:4]]):
            nX, nY, nZ, nF = (nib_nii.header['dim'][1:4].tolist() + [1])
            dimX, dimY, dimZ = nib_nii.header['pixdim'][1:4].tolist()

        else:
            raise ValueError("Error: NIfTI is not 3-dimensional.")

        # Instances & Slice Spacing
        nInstances = nZ*nF
        sliceIndices = np.repeat(range(1, nZ+1), nF)
        voxelSpacing = dimZ
        zLocLast = (voxelSpacing * nZ) - voxelSpacing
        sliceLoca = np.repeat(np.linspace(0, zLocLast, num=nZ), nF)

        # Windowing & Signal Intensity
        maxI = np.amax(nii_img)
        minI = np.amin(nii_img)
        windowCenter = round((maxI - minI) / 2)
        windowWidth = round(maxI - minI)
        rescaleIntercept = 0
        rescaleSlope = 1

        # FOV
        fovX = nX * dimX
        fovY = nY * dimY
        fovZ = nZ * dimZ

        # slice positioning in 3-D space
        # nb: -1 for dir cosines gives consistent orientation between Nifti and DICOM in ITK-Snap
        A = nib_nii.affine

        # copied from https://github.com/ml-workgroup/nifti_to_dicom/blob/main/nifti_to_dicom.py
        # Flip from RAS to LPS for the 3x3 rotation and the translation vector
        flip = np.diag([-1, -1, 1, 1])
        A = flip @ A

        # Extract row and column direction vectors (normalize them → direction cosines)
        R_lps = A[:3, :3]
        row_dir = R_lps[:, 0] / np.linalg.norm(R_lps[:, 0])
        col_dir = R_lps[:, 1] / np.linalg.norm(R_lps[:, 1])
        image_orientation_patient = np.concatenate([row_dir, col_dir]).tolist()  # 6-element array

        sliceLoca = []
        image_pos_patient_array = []
        for iInstance in range(0, nInstances):
            T1N = fnT1N(A, iInstance)
            image_pos_patient_array.append([T1N[0], T1N[1], T1N[2]])
            sliceLoca.append(T1N[2])

        # output dictionary
        nii2dcm_parameters = {

            # series parameters
            'dimX': dimX,
            'dimY': dimY,
            'SliceThickness': str(dimZ),
            'SpacingBetweenSlices': str(dimZ),
            'AcquisitionMatrix': [0, nX, nY, 0],
            'Rows': nX,
            'Columns': nY,
            'NumberOfSlices': nZ,
            'NumberOfInstances': nZ*nF,
            'PixelSpacing': [dimX, dimY],
            'FOV': [fovX, fovY, fovZ],
            'SmallestImagePixelValue': minI,
            'LargestImagePixelValue': maxI,
            'WindowCenter': str(windowCenter),
            'WindowWidth': str(windowWidth),
            'RescaleIntercept': str(rescaleIntercept),
            'RescaleSlope': str(rescaleSlope),
            'SpacingBetweenSlices': round(float(dimZ), 2),
            'ImageOrientationPatient': image_orientation_patient,

            # instance parameters
            'InstanceNumber': sliceIndices,
            'SliceLocation': sliceLoca,
            'ImagePositionPatient': image_pos_patient_array

        }

        return nii2dcm_parameters
