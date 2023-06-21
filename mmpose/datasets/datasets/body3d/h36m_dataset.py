# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp
from collections import defaultdict
from typing import Callable, List, Optional, Sequence, Tuple, Union

import numpy as np
from mmengine.fileio import exists, get_local_path
from mmengine.utils import is_abs

from mmpose.datasets.datasets import BaseMocapDataset
from mmpose.registry import DATASETS


@DATASETS.register_module()
class Human36mDataset(BaseMocapDataset):
    """Human3.6M dataset for 3D human pose estimation.

    "Human3.6M: Large Scale Datasets and Predictive Methods for 3D Human
    Sensing in Natural Environments", TPAMI`2014.
    More details can be found in the `paper
    <http://vision.imar.ro/human3.6m/pami-h36m.pdf>`__.

    Human3.6M keypoint indexes::

        0: 'root (pelvis)',
        1: 'right_hip',
        2: 'right_knee',
        3: 'right_foot',
        4: 'left_hip',
        5: 'left_knee',
        6: 'left_foot',
        7: 'spine',
        8: 'thorax',
        9: 'neck_base',
        10: 'head',
        11: 'left_shoulder',
        12: 'left_elbow',
        13: 'left_wrist',
        14: 'right_shoulder',
        15: 'right_elbow',
        16: 'right_wrist'

    Args:
        ann_file (str): Annotation file path. Default: ''.
        seq_len (int): Number of frames in a sequence. Default: 1.
        seq_step (int): The interval for extracting frames from the video.
            Default: 1.
        multiple_target (int): If larger than 0, merge every
            ``multiple_target`` sequence together. Default: 0.
        pad_video_seq (bool): Whether to pad the video so that poses will be
            predicted for every frame in the video. Default: ``False``.
        causal (bool): If set to ``True``, the rightmost input frame will be
            the target frame. Otherwise, the middle input frame will be the
            target frame. Default: ``True``.
        subset_frac (float): The fraction to reduce dataset size. If set to 1,
            the dataset size is not reduced. Default: 1.
        keypoint_2d_src (str): Specifies 2D keypoint information options, which
            should be one of the following options:

            - ``'gt'``: load from the annotation file
            - ``'detection'``: load from a detection
              result file of 2D keypoint
            - 'pipeline': the information will be generated by the pipeline

            Default: ``'gt'``.
        keypoint_2d_det_file (str, optional): The 2D keypoint detection file.
            If set, 2d keypoint loaded from this file will be used instead of
            ground-truth keypoints. This setting is only when
            ``keypoint_2d_src`` is ``'detection'``. Default: ``None``.
        factor_file (str, optional): The projection factors' file. If set,
            factor loaded from this file will be used instead of calculated
            factors. Default: ``None``.
        camera_param_file (str): Cameras' parameters file. Default: ``None``.
        data_mode (str): Specifies the mode of data samples: ``'topdown'`` or
            ``'bottomup'``. In ``'topdown'`` mode, each data sample contains
            one instance; while in ``'bottomup'`` mode, each data sample
            contains all instances in a image. Default: ``'topdown'``
        metainfo (dict, optional): Meta information for dataset, such as class
            information. Default: ``None``.
        data_root (str, optional): The root directory for ``data_prefix`` and
            ``ann_file``. Default: ``None``.
        data_prefix (dict, optional): Prefix for training data.
            Default: ``dict(img='')``.
        filter_cfg (dict, optional): Config for filter data. Default: `None`.
        indices (int or Sequence[int], optional): Support using first few
            data in annotation file to facilitate training/testing on a smaller
            dataset. Default: ``None`` which means using all ``data_infos``.
        serialize_data (bool, optional): Whether to hold memory using
            serialized objects, when enabled, data loader workers can use
            shared RAM from master process instead of making a copy.
            Default: ``True``.
        pipeline (list, optional): Processing pipeline. Default: [].
        test_mode (bool, optional): ``test_mode=True`` means in test phase.
            Default: ``False``.
        lazy_init (bool, optional): Whether to load annotation during
            instantiation. In some cases, such as visualization, only the meta
            information of the dataset is needed, which is not necessary to
            load annotation file. ``Basedataset`` can skip load annotations to
            save time by set ``lazy_init=False``. Default: ``False``.
        max_refetch (int, optional): If ``Basedataset.prepare_data`` get a
            None img. The maximum extra number of cycles to get a valid
            image. Default: 1000.
    """

    METAINFO: dict = dict(from_file='configs/_base_/datasets/h36m.py')
    SUPPORTED_keypoint_2d_src = {'gt', 'detection', 'pipeline'}

    def __init__(self,
                 ann_file: str = '',
                 seq_len: int = 1,
                 seq_step: int = 1,
                 multiple_target: int = 0,
                 pad_video_seq: bool = False,
                 causal: bool = True,
                 subset_frac: float = 1.0,
                 keypoint_2d_src: str = 'gt',
                 keypoint_2d_det_file: Optional[str] = None,
                 factor_file: Optional[str] = None,
                 camera_param_file: Optional[str] = None,
                 data_mode: str = 'topdown',
                 metainfo: Optional[dict] = None,
                 data_root: Optional[str] = None,
                 data_prefix: dict = dict(img=''),
                 filter_cfg: Optional[dict] = None,
                 indices: Optional[Union[int, Sequence[int]]] = None,
                 serialize_data: bool = True,
                 pipeline: List[Union[dict, Callable]] = [],
                 test_mode: bool = False,
                 lazy_init: bool = False,
                 max_refetch: int = 1000):
        # check keypoint_2d_src
        self.keypoint_2d_src = keypoint_2d_src
        if self.keypoint_2d_src not in self.SUPPORTED_keypoint_2d_src:
            raise ValueError(
                f'Unsupported `keypoint_2d_src` "{self.keypoint_2d_src}". '
                f'Supported options are {self.SUPPORTED_keypoint_2d_src}')

        if keypoint_2d_det_file:
            if not is_abs(keypoint_2d_det_file):
                self.keypoint_2d_det_file = osp.join(data_root,
                                                     keypoint_2d_det_file)
            else:
                self.keypoint_2d_det_file = keypoint_2d_det_file

        self.seq_step = seq_step
        self.pad_video_seq = pad_video_seq

        if factor_file:
            if not is_abs(factor_file):
                factor_file = osp.join(data_root, factor_file)
            assert exists(factor_file), 'Annotation file does not exist.'
        self.factor_file = factor_file

        super().__init__(
            ann_file=ann_file,
            seq_len=seq_len,
            multiple_target=multiple_target,
            causal=causal,
            subset_frac=subset_frac,
            camera_param_file=camera_param_file,
            data_mode=data_mode,
            metainfo=metainfo,
            data_root=data_root,
            data_prefix=data_prefix,
            filter_cfg=filter_cfg,
            indices=indices,
            serialize_data=serialize_data,
            pipeline=pipeline,
            test_mode=test_mode,
            lazy_init=lazy_init,
            max_refetch=max_refetch)

    def get_sequence_indices(self) -> List[List[int]]:
        """Split original videos into sequences and build frame indices.

        This method overrides the default one in the base class.
        """
        imgnames = self.ann_data['imgname']
        video_frames = defaultdict(list)
        for idx, imgname in enumerate(imgnames):
            subj, action, camera = self._parse_h36m_imgname(imgname)
            video_frames[(subj, action, camera)].append(idx)

        # build sample indices
        sequence_indices = []
        _len = (self.seq_len - 1) * self.seq_step + 1
        _step = self.seq_step

        if self.multiple_target:
            for _, _indices in sorted(video_frames.items()):
                n_frame = len(_indices)
                seqs_from_video = [
                    _indices[i:(i + self.multiple_target):_step]
                    for i in range(0, n_frame, self.multiple_target)
                ][:n_frame // self.multiple_target]
                sequence_indices.extend(seqs_from_video)

        else:
            for _, _indices in sorted(video_frames.items()):
                n_frame = len(_indices)

                if self.pad_video_seq:
                    # Pad the sequence so that every frame in the sequence will
                    # be predicted.
                    if self.causal:
                        frames_left = self.seq_len - 1
                        frames_right = 0
                    else:
                        frames_left = (self.seq_len - 1) // 2
                        frames_right = frames_left
                    for i in range(n_frame):
                        pad_left = max(0, frames_left - i // _step)
                        pad_right = max(
                            0, frames_right - (n_frame - 1 - i) // _step)
                        start = max(i % _step, i - frames_left * _step)
                        end = min(n_frame - (n_frame - 1 - i) % _step,
                                  i + frames_right * _step + 1)
                        sequence_indices.append([_indices[0]] * pad_left +
                                                _indices[start:end:_step] +
                                                [_indices[-1]] * pad_right)
                else:
                    seqs_from_video = [
                        _indices[i:(i + _len):_step]
                        for i in range(0, n_frame - _len + 1)
                    ]
                    sequence_indices.extend(seqs_from_video)

        # reduce dataset size if needed
        subset_size = int(len(sequence_indices) * self.subset_frac)
        start = np.random.randint(0, len(sequence_indices) - subset_size + 1)
        end = start + subset_size

        sequence_indices = sequence_indices[start:end]

        return sequence_indices

    def _load_annotations(self) -> Tuple[List[dict], List[dict]]:
        instance_list, image_list = super()._load_annotations()

        h36m_data = self.ann_data
        kpts_3d = h36m_data['S']

        if self.keypoint_2d_src == 'detection':
            assert exists(self.keypoint_2d_det_file)
            kpts_2d = self._load_keypoint_2d_detection(
                self.keypoint_2d_det_file)
            assert kpts_2d.shape[0] == kpts_3d.shape[0]
            assert kpts_2d.shape[2] == 3

            for idx, frame_ids in enumerate(self.sequence_indices):
                kpt_2d = kpts_2d[frame_ids].astype(np.float32)
                keypoints = kpt_2d[..., :2]
                keypoints_visible = kpt_2d[..., 2]
                instance_list[idx].update({
                    'keypoints':
                    keypoints,
                    'keypoints_visible':
                    keypoints_visible
                })
        if self.factor_file:
            with get_local_path(self.factor_file) as local_path:
                factors = np.load(local_path).astype(np.float32)
            assert factors.shape[0] == kpts_3d.shape[0]
            for idx, frame_ids in enumerate(self.sequence_indices):
                factor = factors[frame_ids].astype(np.float32)
                instance_list[idx].update({'factor': factor})

        return instance_list, image_list

    @staticmethod
    def _parse_h36m_imgname(imgname) -> Tuple[str, str, str]:
        """Parse imgname to get information of subject, action and camera.

        A typical h36m image filename is like:
        S1_Directions_1.54138969_000001.jpg
        """
        subj, rest = osp.basename(imgname).split('_', 1)
        action, rest = rest.split('.', 1)
        camera, rest = rest.split('_', 1)
        return subj, action, camera

    def get_camera_param(self, imgname) -> dict:
        """Get camera parameters of a frame by its image name."""
        assert hasattr(self, 'camera_param')
        subj, _, camera = self._parse_h36m_imgname(imgname)
        return self.camera_param[(subj, camera)]

    def _load_keypoint_2d_detection(self, det_file):
        """"Load 2D joint detection results from file."""
        with get_local_path(det_file) as local_path:
            kpts_2d = np.load(local_path).astype(np.float32)

        return kpts_2d
