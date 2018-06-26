# ElastiCup 

## Analyze 2018 FIFA World Cup with the ELK stack!

This project loads automatically information about world cup games into Elastcsearch.

It sets up elasticsearch and kibana docker containers which are ready for your analysis. 

When you deploy the stack, a python script downloads the current status (updates every minute!) and load it instently to elasticsearch!

## Getting Started

- Make sure you have docker swarm!

- Clone the project by running:

  ```git clone https://github.com/eeddaann/ElastiCup.git```

- build the image and deploy the docker stack:

  ``` docker build . -t elasticup-etl && docker stack deploy -c docker-compose.yml elasticup``` 

- Now open the browser and go to:

  ```http://127.0.0.1:5601``` 

