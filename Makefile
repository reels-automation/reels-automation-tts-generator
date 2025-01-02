install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
build-container:
	docker build --no-cache -t reels-automation-tts-generator .
run-container:
		docker run --rm -it \
  --network reels-automation-docker-compose_local-kafka \
  --network reels-automation-docker-compose_minio-network \
  reels-automation-tts-generator