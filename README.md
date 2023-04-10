# Text2Video-Zero-sd-webui

- clone this repo to `/path/to/stable-diffusion-webui/extensions`
- get `annotator` and `__assets__` folders from this [link](https://huggingface.co/spaces/PAIR/Text2Video-Zero/tree/main) and put them in `/path/to/stable-diffusion-webui/extensions/Text2Video-Zero-sd-webui`
- relaunch your webui, the first launch may take a few minutes for caching video examples.
- may need to add `--disable-safe-unpickle` to `bash webui.sh` when launch

## Updates
- [4/10/2023] 
  - Updated to original repo `2e1b115`
  - Disabled example caching
  - Updated denpendences, after automatic installation, it should work on Linux environment. For example, issues such as "can't import decord" and no tab showing are due to erroneous dependency installation. 
