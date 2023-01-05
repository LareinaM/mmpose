
<!-- [ALGORITHM] -->

<details>
<summary align="right"><a href="http://openaccess.thecvf.com/content_CVPR_2019/html/Sun_Deep_High-Resolution_Representation_Learning_for_Human_Pose_Estimation_CVPR_2019_paper.html">ViTPose</a></summary>

```bibtex
@misc{https://doi.org/10.48550/arxiv.2204.12484,
  doi = {10.48550/ARXIV.2204.12484},
  url = {https://arxiv.org/abs/2204.12484},
  author = {Xu, Yufei and Zhang, Jing and Zhang, Qiming and Tao, Dacheng},
  keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {ViTPose: Simple Vision Transformer Baselines for Human Pose Estimation},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```

</details>

<!-- [DATASET] -->

<details>
<summary align="right"><a href="https://link.springer.com/chapter/10.1007/978-3-030-58545-7_12">COCO-WholeBody (ECCV'2020)</a></summary>

```bibtex
@inproceedings{jin2020whole,
  title={Whole-Body Human Pose Estimation in the Wild},
  author={Jin, Sheng and Xu, Lumin and Xu, Jin and Wang, Can and Liu, Wentao and Qian, Chen and Ouyang, Wanli and Luo, Ping},
  booktitle={Proceedings of the European Conference on Computer Vision (ECCV)},
  year={2020}
}
```

</details>

Results on COCO val2017 with detector having human AP of 56.4 on COCO val2017 dataset

> With classic decoder

| Model | Input Size | AP | AR | config | log |
| :-------------------------------------- | :--------: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :------: | :------: | :--------------------------------------: | :-------------------------------------: |
| [ViTPose-B](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-base_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |
| [ViTPose-L](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-large_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |
| [ViTPose-H](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-huge_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |

> With simple decoder

| Model | Input Size | AP | AR | config | log |
| :-------------------------------------- | :--------: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :------: | :------: | :--------------------------------------: | :-------------------------------------: |
| [ViTPose-B](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-base-simple_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |
| [ViTPose-L](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-large-simple_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |
| [ViTPose-H](/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-huge-simple_8xb64-210e_coco-256x192.py) |  256x192 |  |  | [ckpt]() | [log]() |