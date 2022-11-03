

## Update config
python ../templates/update_config.py

## Start db
cd db; docker-compose up 

## Start plantum-service 
cd plantuml-service; docker-compose up


## Start ui-api
cd ui-api; python server.py

## Start user interface
cd user-interface; start index.html 

