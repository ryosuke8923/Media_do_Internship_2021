build:
	docker build -t team_c .

run-bash:
	docker run -it -e PORT=8888 -p 8888:8888 -v :/app team_c bash
