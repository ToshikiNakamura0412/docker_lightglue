import sys

import matplotlib.pyplot as plt
import torch
from lightglue import DISK, LightGlue, SuperPoint, viz2d
from lightglue.utils import load_image, rbd


def demo(level: str = "easy"):
    torch.set_grad_enabled(False)

    print("torch.cuda.is_available():", torch.cuda.is_available())
    print("torch.cuda.current_device():", torch.cuda.current_device())
    print("torch.cuda.get_device_name(0):", torch.cuda.get_device_name(0))

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )  # 'mps', 'cpu'

    extractor = (
        SuperPoint(max_num_keypoints=2048).eval().to(device)
    )  # load the extractor
    matcher = LightGlue(features="superpoint").eval().to(device)

    image0, image1 = torch.Tensor(), torch.Tensor()
    if level == "easy":
        image0 = load_image("images/DSC_0411.JPG")
        image1 = load_image("images/DSC_0410.JPG")
    if level == "difficult":
        image0 = load_image("images/sacre_coeur1.jpg")
        image1 = load_image("images/sacre_coeur2.jpg")

    feats0 = extractor.extract(image0.to(device))
    feats1 = extractor.extract(image1.to(device))
    matches01 = matcher({"image0": feats0, "image1": feats1})
    feats0, feats1, matches01 = [
        rbd(x) for x in [feats0, feats1, matches01]
    ]  # remove batch dimension

    kpts0, kpts1, matches = (
        feats0["keypoints"],
        feats1["keypoints"],
        matches01["matches"],
    )
    m_kpts0, m_kpts1 = kpts0[matches[..., 0]], kpts1[matches[..., 1]]

    axes = viz2d.plot_images([image0, image1])
    viz2d.plot_matches(m_kpts0, m_kpts1, color="lime", lw=0.2)
    viz2d.add_text(0, f'Stop after {matches01["stop"]} layers', fs=20)

    kpc0, kpc1 = viz2d.cm_prune(matches01["prune0"]), viz2d.cm_prune(
        matches01["prune1"]
    )
    viz2d.plot_images([image0, image1])
    viz2d.plot_keypoints([kpts0, kpts1], colors=[kpc0, kpc1], ps=10)

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        demo()
    elif sys.argv[1] == "difficult":
        demo("difficult")
