# Get Segments

Api for getting metrics from 'Яндекс Аудитории'.

## Run
1. Create config.ini in aps folder

    ```bash
       [scrap config]
       url = https://audience.yandex.ru/
       log_name = login
       passwd = password
       proxy_host = host
       proxy_port = port
    ```

2. build & run docker:
    ```bash
        docker build -t selenium_app .
        docker run -d selenium_app

    ```

3. Request:
    
    ```bash
        curl -i -H "Content-Type: application/json" -X POST \
                -d '{"segment_ids": [list of ids]}' \
                http://localhost:5000/api/
    ```
   
4. Response:
    ```json
        {
            "id": {
                "profile": false, 
                "result": {
                  "age": {
                    "age": <val>, 
                  }, 
                  "city": {
                    "city_name": <val>, 
                  }, 
                  "device": {
                    "number": <val>, 
                  }, 
                  "gender": {
                    "0": <val>, 
                    "1": <val>
                  }, 
                  "goals": [], 
                  "interests": {
                    "interest": <val>, 
                  }, 
                  "no_data": false, 
                  "segments": {
                    "segment": <val>, 
                  }, 
                  "self_similarity": <val>, 
                  "settings": {}, 
                  "totals": <val>
                }
              }
            }

    ```
 
3. 

