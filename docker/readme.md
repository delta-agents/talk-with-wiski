# Docker

``` bash
cd /d "D:\my_projects\talk-with-wiski"
docker build -t talk-with-wiski/api:0.0.3 -f docker\Dockerfile .
docker run --name talk-with-wiski_0.0.3 -p 8000:8000 -t talk-with-wiski/api:0.0.3
```
