"""
IOD Module - CT Image

C.8.2.1
https://dicom.nema.org/medical/Dicom/2024c/output/chtml/part03/sect_C.8.2.html

"""


from nii2dcm.module import Module


class CTImage(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'CTImage'

        # For now, will omit thereby inheriting parent value
        # self.ds.ImageType = ''

        self.ds.SamplesPerPixel = 1

        # PhotometricInterpretation
        self.ds.PhotometricInterpretation = 'MONOCHROME2'

        # Bits Allocated
        # defined to equal 16 for CT Image Module
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.2.html
        self.ds.BitsAllocated = 16
        self.ds.BitsStored = 16
        self.ds.HighBit = self.ds.BitsStored - 1

        # NOTE: RescaleSlope, RescaleIntercept set at run_nii2dcm.py and nii.py
        self.ds.RescaleType = "HU"

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

