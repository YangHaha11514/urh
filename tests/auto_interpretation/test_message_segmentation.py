import unittest

import numpy as np

from tests.test_util import get_path_for_data_file
from urh.ainterpretation.AutoInterpretation import segment_messages_from_magnitudes, merge_message_segments_for_ook
from urh.signalprocessing.Signal import Signal


class TestMessageSegmentation(unittest.TestCase):
    def test_segmentation_for_fsk(self):
        signal = np.fromfile(get_path_for_data_file("fsk.complex"), dtype=np.complex64)
        segments = segment_messages_from_magnitudes(np.abs(signal), 0.0009)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0], (0, 17742))

    def test_segmentation_for_ask(self):
        signal = np.fromfile(get_path_for_data_file("ask.complex"), dtype=np.complex64)
        segments = segment_messages_from_magnitudes(np.abs(signal), 0.02)
        segments = merge_message_segments_for_ook(segments)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0], (462, 12011))

    def test_segmentation_enocean_multiple_messages(self):
        signal = np.fromfile(get_path_for_data_file("enocean.complex"), dtype=np.complex64)
        segments = segment_messages_from_magnitudes(np.abs(signal), 0.025)
        segments = merge_message_segments_for_ook(segments)
        self.assertEqual(len(segments), 3)
        self.assertEqual(segments[0], (6086, 6753))
        self.assertEqual(segments[1], (9751, 10417))
        self.assertEqual(segments[2], (22208, 22876))

    def test_message_segmentation_fsk_xavax(self):
        signal = Signal(get_path_for_data_file("xavax.coco"), "")
        segments = segment_messages_from_magnitudes(np.abs(signal.data), noise_threshold=0.002)

        # Signal starts with overdrive, so one msessage more
        self.assertTrue(len(segments) == 6 or len(segments) == 7)
        if len(segments) == 7:
            segments = segments[1:]

        self.assertEqual(segments,
                         [(275146, 293697), (321073, 338819), (618213, 1631898), (1657890, 1678041), (1803145, 1820892),
                          (1846213, 1866364)])
