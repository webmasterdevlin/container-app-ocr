# OCR mock service
- This is a container for an azure container apps

## How to build and push a docker image
- start docker
- login to the azure container registry
```zsh
az acr login --name centauricr
```
- build the container
```zsh
docker build --platform linux/amd64 -t centauricr.azurecr.io/centauri-ocr:latest .
```
- push the image
```zsh
docker push centauricr.azurecr.io/centauri-ocr:latest
```
