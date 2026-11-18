#!/usr/bin/env python3
"""
make_video_slides.py — turn a rendered carousel's flat JPG slides into flat MP4s.

Each slide becomes its own silent 3-second video at the same 1080x1350 frame,
with NO motion and NO animation: it is the still card, held, so the post reads
as a swipeable, viewer-paced carousel that Instagram labels as video.

Usage:
    python3 pipeline/make_video_slides.py posts/2026-11-19-caregiver
    python3 pipeline/make_video_slides.py posts/2026-11-19-caregiver --seconds 3

Output: posts/<folder>/video/slide-N.mp4 (one per slide-N.jpg, same order).
Public URL: https://raw.githubusercontent.com/brittanysandovalrn-dot/bwylde-social-assets/main/posts/<folder>/video/slide-N.mp4

Requires ffmpeg on PATH. Does not touch the source JPGs.
"""
import argparse
import glob
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="post folder holding slide-N.jpg files")
    ap.add_argument("--seconds", type=float, default=3.0,
                    help="duration per slide (default 3)")
    args = ap.parse_args()

    folder = args.folder.rstrip("/")
    slides = sorted(
        glob.glob(os.path.join(folder, "slide-*.jpg")),
        key=lambda p: int(os.path.basename(p).split("-")[1].split(".")[0]),
    )
    if not slides:
        sys.exit(f"No slide-*.jpg found in {folder}")

    out_dir = os.path.join(folder, "video")
    os.makedirs(out_dir, exist_ok=True)

    for src in slides:
        name = os.path.splitext(os.path.basename(src))[0]
        dst = os.path.join(out_dir, name + ".mp4")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-framerate", "30", "-i", src,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(args.seconds),
            # force the exact 4:5 frame; keeps Instagram from adding blank bars
            "-vf", "scale=1080:1350,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
            "-tune", "stillimage", "-r", "30",
            "-c:a", "aac", "-b:a", "64k",
            "-shortest", "-movflags", "+faststart",
            dst,
        ]
        subprocess.run(cmd, check=True)
        print(f"  {dst}")

    print(f"{len(slides)} video slides written to {out_dir}")


if __name__ == "__main__":
    main()
