install:
	pip install -r requirements.txt

lint:
	pylint src/*.py

run: lint
	cd src && streamlit run app.py --server.port 8080 --server.address 0.0.0.0  --server.headless true --logger.level debug

build:
	podman build -t pod-demo-image:latest . --platform linux/amd64

push:
	podman tag pod-demo-image:latest registry.home.glroland.com/ai/pod-demo:latest
	podman push registry.home.glroland.com/ai/pod-demo:latest --tls-verify=false

deploy:
	oc apply -f kubernetes/deploy.yaml

dev: lint
	odo dev
