import zeep
import asyncio, sys
from onvif import ONVIFCamera
from config.setting import *

ptz = None
active = False


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue


class CameraController:
    presets = []
    status = None

    def get_current_preset(self):
        mycam = ONVIFCamera(CAMERA_IP, CAMERA_PASSWORD, CAMERA_USER_NAME, CAMERA_PASSWORD)
        # Create media service object
        media = mycam.create_media_service()
        print("setup_move {} {}", mycam, media)
        # Create ptz service object

        ptz = mycam.create_ptz_service()
        # Get target profile
        media_profile = media.GetProfiles()[0]
        profileToken = media_profile.token

        # GetStatus
        print("GetStatus")
        self.status = ptz.GetStatus({'ProfileToken': profileToken})
        print('status {} {} {}   ? => {}'.format(self.status.Position.PanTilt.x, self.status.Position.PanTilt.y,
                                                 self.status.Position.Zoom.x,
                                                 self.status.MoveStatus.PanTilt))

        min_dist = 100
        current_prest = None
        for preset in self.presets:
            position = preset['PTZPosition']
            dist = pow((self.status.Position.PanTilt.x - position.PanTilt.x), 2) + pow((self.status.Position.PanTilt.y - position.PanTilt.y), 2)
            if dist < min_dist:
                min_dist = dist
                current_prest = preset

        snapshot = media.GetSnapshotUri({'ProfileToken': profileToken})
        print('snapshot uri {}'.format(snapshot))
        return current_prest, self.status.MoveStatus.PanTilt, snapshot

    def get_presets(self):
        mycam = ONVIFCamera(CAMERA_IP, CAMERA_PASSWORD, CAMERA_USER_NAME, CAMERA_PASSWORD)
        # Create media service object
        media = mycam.create_media_service()
        print("setup_move {} {}", mycam, media)
        # Create ptz service object

        ptz = mycam.create_ptz_service()
        # Get target profile
        media_profile = media.GetProfiles()[0]
        profileToken = media_profile.token

        # Get presets
        print("Get Presets...")
        gp = ptz.create_type('GetPresets')
        gp.ProfileToken = profileToken
        self.presets = ptz.GetPresets(gp)
        for preset in self.presets:
            if (hasattr(preset, "Name")):
                name = preset.Name
            else:
                name = ""
            position = preset['PTZPosition']

            print("preset {} => ({}, {}, {})".format(name, position.PanTilt.x,
                                                 position.PanTilt.y,
                                                 position.Zoom.x))
        return self.presets