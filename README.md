# Unsupervised-Image-to-Image-Translation
This repository contains multiple util functions for the Unsupervised Image to Image Translation project.

## Organisation
- `dataset` contains all the files related to the different dataset we use for the different iterations
- `quantitative` contains all the code to generate images for every model and compute their LPIPS score and Inception score as well as the actual generated images.
- `testing` contains as script to generate the commands for quick images translations
- `conda_env.yml` is the conda environment that we set up in order to run our ode

### On the cluster
Please find the deliverables too big to be uploaded here on the cluster `iccluster139.iccluster.epfl.ch`:

- `/ivrldata1/students/2021-spring-cs413-team3/HANDIN/INIT_dataset`:
  - contains the dataset for our project:
    - `cloudy`, `sunny`, `night` and `rainy` contain what we kept from the dataset of INIT.
    - `ssd` contains all the classes (and images) created using RetinaNet
    - `miscelaneous_and_scripts` contains some scripts and intermediate `txt` files used during splitting.
- `/ivrldata1/students/2021-spring-cs413-team3/HANDIN/models`:
  - contains all the models trained that are presented in the `Results` part of our report as well as the baseline (FUNIT pretrained model that we fine-tuned)
