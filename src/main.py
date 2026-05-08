import argparse
import os
from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt


def create_sample_image(width=256, height=256):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        img[i, :, 0] = np.linspace(0, 255, width, dtype=np.uint8)
        img[i, :, 1] = 255 - img[i, :, 0]
        img[i, :, 2] = (img[i, :, 0] // 2)
    return img


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def process_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return gray, edges


def save_results(out_dir: Path, original, gray, edges):
    ensure_dir(out_dir)
    orig_path = out_dir / "original.png"
    gray_path = out_dir / "gray.png"
    edges_path = out_dir / "edges.png"
    cv2.imwrite(str(orig_path), original)
    cv2.imwrite(str(gray_path), gray)
    cv2.imwrite(str(edges_path), edges)

    # also save a matplotlib figure
    fig_path = out_dir / "comparison.png"
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 3, 1); plt.title('Original'); plt.axis('off'); plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 3, 2); plt.title('Gray'); plt.axis('off'); plt.imshow(gray, cmap='gray')
    plt.subplot(1, 3, 3); plt.title('Edges'); plt.axis('off'); plt.imshow(edges, cmap='gray')
    plt.tight_layout()
    plt.savefig(str(fig_path), dpi=150)
    plt.close()

    return orig_path, gray_path, edges_path, fig_path


def main():
    parser = argparse.ArgumentParser(description='Simple OpenCV test script')
    parser.add_argument('--image', help='Path to input image (optional)')
    parser.add_argument('--out', help='Output folder', default='results')
    args = parser.parse_args()

    out_dir = Path(args.out)
    ensure_dir(out_dir)

    if args.image and Path(args.image).exists():
        img = cv2.imread(args.image)
        if img is None:
            print('Gagal membaca gambar, membuat contoh sintetik.')
            img = create_sample_image()
    else:
        print('Tidak ada gambar diberikan; membuat contoh citra sintetik.')
        img = create_sample_image()

    gray, edges = process_image(img)
    saved = save_results(out_dir, img, gray, edges)
    print('Hasil tersimpan di:', saved[0].parent)


if __name__ == '__main__':
    main()
