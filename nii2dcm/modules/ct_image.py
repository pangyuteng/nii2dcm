"""
IOD Module – MR Image

C.8.3.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1

Note: Tags labelled ":missing:" are defined in the NEMA MR standard, but I have not found in real DICOMs exported from
an MRI scanner.
"""


from nii2dcm.module import Module


class CTImage(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'MRImage'

        # For now, will omit thereby inheriting parent value
        # self.ds.ImageType = ''

        self.ds.SamplesPerPixel = 1

        # PhotometricInterpretation
        self.ds.PhotometricInterpretation = 'MONOCHROME2'
    
        # PresentationLUTShape
        # depends on PhotometricInterpretation: https://dicom.innolitics.com/ciods/mr-image/general-image/20500020
        if self.ds.PhotometricInterpretation == 'MONOCHROME2':
            self.ds.PresentationLUTShape = 'IDENTITY'
        elif self.ds.PhotometricInterpretation == 'MONOCHROME1':
            self.ds.PresentationLUTShape = 'INVERSE'
    
        # Bits Allocated
        # defined to equal 16 for MR Image Module
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1.1.4
        self.ds.BitsAllocated = 16
        self.ds.BitsStored = 12
        self.ds.HighBit = self.ds.BitsStored - 1
    
        self.ds.KVP = ''
        self.ds.TubeCurrent = ''
        self.ds.ExposureTime = ''
        self.ds.Exposure = ''
        self.ds.SliceThickness = ''
        self.ds.GantryDetectorTilt = ''
        self.ds.TableHeight = ''
        self.ds.RotationDirection = ''
        self.ds.ScanLength = ''
        self.ds.TotalCollimationWidth = ''
        self.ds.DataCollectionDiameter = ''
        self.ds.ReconstructionDiameter = ''
        self.ds.ConvolutionKernel = ''
        self.ds.RevolutionTime = ''
        self.ds.SingleCollimationWidth = ''
        self.ds.PitchFactor = ''
        self.ds.ExposureModulationType = ''
        self.ds.EstimatedDoseSaving = ''

