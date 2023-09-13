"""
(*)~----------------------------------------------------------------------------------
Pupil LSL Relay
Copyright (C) 2012 Pupil Labs

Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""
from .channel import (
    confidence_channel,
    norm_pos_channels,
)
from .outlet import Outlet


class SurfaceGaze(Outlet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g_pool = None

    @property
    def name(self) -> str:
        return "pupil_capture_surface"

    @property
    def event_key(self) -> str:
        return "surfaces"

    def setup_channels(self):
        return (
            confidence_channel(),
            *norm_pos_channels(),
        )

    def push_sample(self, sample):
        # filter out off-surface gazes
        surface_gazes = filter(lambda x: x['on_surf'], sample['gaze_on_surfaces'])

        # if both eyes are enabled, only push samples that use combined-eyes data
        if all(x.value for x in self.g_pool.eye_procs_alive):
            surface_gazes = filter(lambda x: x['topic'] == 'gaze.3d.01._on_surface', surface_gazes)

        for subsample in surface_gazes:
            super().push_sample(subsample)
