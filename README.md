# case_cats
docker run -d -p 27017:27017 -e AUTH=no --name mongo mongo
docker run -d -p 8888:8888 --name case_cats_api viniciusks/case_cats:1.0.0