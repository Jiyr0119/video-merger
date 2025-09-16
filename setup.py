from setuptools import setup, find_packages

setup(
    name="myproject",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "ffmpeg-python",
        "vosk",
        "srt"
    ],
    author="Jonathan",
    author_email="jonathan@example.com",
    description="视频合并工具",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/video-merger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)