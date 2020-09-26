### DOCKER
# ¯¯¯¯¯¯¯¯


docker.build: ##
	docker build -t "kfirfer/kibana-index-pattern-updater:${version}" .

docker.push: ##
	docker push kfirfer/kibana-index-pattern-updater:${version}
