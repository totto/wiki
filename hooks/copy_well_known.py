"""
MkDocs hook: copy .well-known directory to site output.

MkDocs 1.x excludes hidden directories (starting with '.') from the build.
This hook copies docs/.well-known/ to site/.well-known/ after every build,
making KCP signing key and other IANA-registered well-known resources
available at their standard URLs.
"""

import shutil
import os


def on_post_build(config, **kwargs):
    src = os.path.join(config["docs_dir"], ".well-known")
    dst = os.path.join(config["site_dir"], ".well-known")
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
