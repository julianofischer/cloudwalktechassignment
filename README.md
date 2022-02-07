# cloudwalktechassignment
 - workers
   - docker
 - fila
   - rabbitmq 
 sudo docker run -d --hostname rabbitmq --name rabbit-cloudwalk -e RABBITMQ_DEFAULT_USER=cloudwalk -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3
 docker start rabbit-cloudwalk
