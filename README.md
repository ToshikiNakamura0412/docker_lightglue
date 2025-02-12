# docker_lightglue

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Docker image for [LightGlue](https://github.com/cvg/LightGlue.git)

<p align="center">
  <img src="docs/demo.png" width="600"/>
</p>

## Installation
```bash
git clone https://github.com/ToshikiNakamura0412/docker_lightglue.git ~/docker_lightglue
cd ~/docker_lightglue
docker compose build
./download_images.sh
```

## Usage
### Start
```bash
docker compose up -d
```

### Demo (Easy)
```bash
docker compose exec demo python3 demo.py
```

### Demo (Difficult)
```bash
docker compose exec demo python3 demo.py difficult
```

### Stop
```bash
docker compose down
```
