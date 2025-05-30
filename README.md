# CosmicMan Prime: Enhancing Activation Strategies for Improved Text-to-Image Synthesis
<img src="./assets/1.png" width="96%" height="96%">

[Gabriel Odai Afotey](mailto:gabrielafotey@gmail.com) <br>
**[[Video Demo]](https://www.youtube.com/watch?v=CsZKA27tQDA)** | | **[[Paper]](./Cosmic-Man-Prime.pdf)** | **[[Huggingface Gradio]](https://huggingface.co/spaces/cosmicman/CosmicMan-SDXL)**  

**Abstract:** I present CosmicMan Prime, a text-to-image foundation model designed to enhance image
generation quality through refined activation strategies. Unlike traditional models that struggle
with suboptimal image quality and text-image misalignment, CosmicMan Prime achieves im-
proved synthesis by optimizing activation functions, ensuring better alignment between textual
descriptions and generated images.
Central to CosmicMan Prime’s improvements are the modified activation strategies and data-
driven refinements: (1) I investigate the impact of activation functions on model performance,
proposing a shift from the standard SiLU activation to more robust alternatives. By testing
various activation functions, I demonstrate that carefully chosen activations can significantly en-
hance model convergence and output fidelity. This exploration provides a deeper understanding
of how activation functions influence the relationship between text and image data. (2) I argue
that a specialized text-to-image model must balance both architectural improvements and prac-
tical usability. To this end, we focus on optimizing CosmicMan Prime’s underlying structure
to enhance its ability to generate high-quality images from detailed textual descriptions. This
model integrates the improved activation function strategies into existing architectures, ensuring
scalability and effectiveness without requiring substantial changes to the foundational model.
Through these refinements, CosmicMan Prime’s delivers higher-quality, more realistic images,
while maintaining the flexibility to be used across various downstream tasks.. <br>

## Updates
- [18/06/2024] Training code is released!
- [14/06/2024] Pretrained models [CosmicMan-SDXL](https://huggingface.co/cosmicman/CosmicMan-SDXL), [CosmicMan-SD](https://huggingface.co/cosmicman/CosmicMan-SD) and inference scripts are released. [Online Huggingface Gradio Demo](https://huggingface.co/spaces/cosmicman/CosmicMan-SDXL) is also released.
- [29/04/2024] [CosmicManHQ-1.0 Dataset](https://huggingface.co/datasets/cosmicman/CosmicManHQ-1.0) is released!
- [05/04/2024] :fire::fire::fire:CosmicMan is selected as **Highlight Paper** (324 out of 11,532 submissions) at CVPR 2024!
- [02/04/2024] [Technical report](https://arxiv.org/abs/2404.01294) has been released.
- [01/03/2024] CosmicMan has been accepted by CVPR2024.


## Usage
Our CosmicMan-SDXL is based on [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) and UNet checkpoint for CosmicMan-SDXL can be download from huggingface page [cosmicman/CosmicMan-SDXL](https://huggingface.co/cosmicman/CosmicMan-SDXL). 
Our CosmicMan-SD is based on [runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5) and UNet checkpoint for CosmicMan-SD can be download from huggingface page [cosmicman/CosmicMan-SD](https://huggingface.co/cosmicman/CosmicMan-SD). 


### Requirements
```
conda create -n cosmicman python=3.10
source activate cosmicman
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install accelerate datasets transformers  invisible-watermark bitsandbytes deepspeed gradio==3.48.0
pip install -e ./diffusers
```

### Quick start with [Gradio](https://www.gradio.app/guides/quickstart)

To get started, first install the required dependencies, then run:

```
# CosmicMan-SDXL 
python demo_sdxl.py
```
Let's have a look at a simple example using the `http://your-server-ip:port`.


### Inference

You can directly use our model with Diffusers for CosmicMan-SDXL and CosmicMan-SD:

```
# CosmicMan-SDXL 
import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

base_path = "stabilityai/stable-diffusion-xl-base-1.0"
refiner_path = "stabilityai/stable-diffusion-xl-refiner-1.0"
unet_path = "cosmicman/CosmicMan-SDXL"

# Load model.
unet = UNet2DConditionModel.from_pretrained(unet_path, torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(base_path, unet=unet, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")
pipe.scheduler = EulerDiscreteScheduler.from_pretrained(base_path, subfolder="scheduler", torch_dtype=torch.float16)

refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(refiner_path, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda") # we found use base_path instead of refiner_path may get a better performance

# Generate image.
positive_prompt = "A fit Caucasian elderly woman, her wavy white hair above shoulders, wears a pink floral cotton long-sleeve shirt and a cotton hat against a natural landscape in an upper body shot"
negative_prompt = ""
image = pipe(positive_prompt, num_inference_steps=30, 
        guidance_scale=7.5, height=1024, 
        width=1024, negative_prompt=negative_prompt, output_type="latent").images[0]
image = refiner(positive_prompt, negative_prompt=negative_prompt, image=image[None, :]).images[0].save("output.png")
```

```
# CosmicMan-SD
import torch
from diffusers import StableDiffusionPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

base_path = "runwayml/stable-diffusion-v1-5"
unet_path = "cosmicman/CosmicMan-SD"

# Load model.
unet = UNet2DConditionModel.from_pretrained(unet_path, torch_dtype=torch.float16)
pipe = StableDiffusionPipeline.from_pretrained(base_path, unet=unet, torch_dtype=torch.float16, variant="fp16").to("cuda")
pipe.scheduler = EulerDiscreteScheduler.from_pretrained(base_path, subfolder="scheduler", torch_dtype=torch.float16)

# Generate image.
positive_prompt = "A closeup portrait shot against a white wall, a fit Caucasian adult female with wavy blonde hair falling above her chest wears a short sleeve silk floral dress and a floral silk normal short sleeve white blouse"
negative_prompt = ""
image = pipe(positive_prompt, num_inference_steps=30, 
        guidance_scale=7.5, height=1024, 
        width=1024, negative_prompt=negative_prompt, output_type="pil").images[0].save("output.png")
```

We also provide the inference scripts in this repository for CosmicMan-SDXL and CosmicMan-SD:

```
# CosmicMan-SDXL 
python infer_sdxl.py --H 1024 --W 1024 --outdir ./Output_sdxl  --steps 30 --use_refiner \
    --prompts "A fit Caucasian elderly woman, her wavy white hair above shoulders, wears a pink floral cotton long-sleeve shirt and a cotton hat against a natural landscape in an upper body shot"\

# CosmicMan-SD
python infer_sd.py --H 1024 --W 1024  --outdir ./Output_sd  --steps 30 \
    --prompts "A closeup portrait shot against a white wall, a fit Caucasian adult female with wavy blonde hair falling above her chest wears a short sleeve silk floral dress and a floral silk normal short sleeve white blouse" \
```

### Training
Download the CosmicManHQ-1.0 dataset from [Hugging face](https://huggingface.co/datasets/cosmicman/CosmicManHQ-1.0) and place it in the `data` directory. Then update the training script found in `train_sdxl.sh` and train! 
```
srun -p PARTITION --gres=gpu:1 --ntasks-per-node=1 --cpus-per-task=8 sh train_sdxl.sh
```


## TODOs
- [x] Release technical report.
- [x] Release data.
- [x] Release Inference code.
- [x] Release pretrained models.
- [x] Release training code.


## Related Work
* (ECCV 2022) **StyleGAN-Human: A Data-Centric Odyssey of Human Generation**, Jianglin Fu et al. [[Paper](https://arxiv.org/pdf/2204.11823.pdf)], [[Project Page](https://stylegan-human.github.io/)], [[Dataset](https://github.com/stylegan-human/StyleGAN-Human)]
* (ICCV 2023) **UnitedHuman: Harnessing Multi-Source Data for High-Resolution Human Generation**, Jianglin Fu et al. [[Paper](https://arxiv.org/abs/2309.14335)], [[Project Page](https://unitedhuman.github.io/)]

## Citation

If you find this work useful for your research, please consider citing our paper:

```bibtex
@inproceedings{cosmicman,
      title = {CosmicMan: A Text-to-Image Foundation Model for Humans},
      author = {Li, Shikai and Fu, Jianglin and Liu, Kaiyuan and Wang, Wentao and Lin, Kwan-Yee and Wu, Wayne},
      booktitle = {Computer Vision and Pattern Recognition (CVPR)},
      year = {2024}
}
```


