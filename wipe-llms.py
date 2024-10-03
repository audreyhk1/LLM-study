import os
from transformers import TRANSFORMERS_CACHE

cache_dir = TRANSFORMERS_CACHE
if os.path.exists(cache_dir):
    import shutil
    shutil.rmtree(cache_dir)
		