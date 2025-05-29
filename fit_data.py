from googleapiclient.discovery import build
import datetime

def get_health_data(credentials):
    service = build('fitness', 'v1', credentials=credentials)
    
    # Рассчет временных меток
    now = datetime.datetime.now()
    end = int(now.timestamp() * 1000)
    start = end - 86400000  # 24 часа назад
    
    # Запрос данных
    body = {
        "aggregateBy": [
            {"dataTypeName": "com.google.step_count.delta"},
            {"dataTypeName": "com.google.heart_rate.bpm"},
            {"dataTypeName": "com.google.sleep.segment"}
        ],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": start,
        "endTimeMillis": end
    }
    
    response = service.users().dataset().aggregate(
        userId="me", body=body
    ).execute()
    
    return parse_response(response)

def parse_response(response):
    # Парсинг ответа Google Fit
    result = {"steps": 0, "avg_heart_rate": 0, "sleep_duration": 0}
    
    for bucket in response.get("bucket", []):
        for dataset in bucket.get("dataset", []):
            data_type = dataset["dataSourceId"].split(":")[2]
            
            for point in dataset.get("point", []):
                if "com.google.step_count" in data_type:
                    result["steps"] += point["value"][0]["intVal"]
                
                elif "com.google.heart_rate" in data_type:
                    result["avg_heart_rate"] = point["value"][0]["fpVal"]
                
                elif "com.google.sleep" in data_type:
                    result["sleep_duration"] += point["endTimeNanos"] - point["startTimeNanos"]
    
    # Конвертация наносекунд в часы для сна
    if result["sleep_duration"] > 0:
        result["sleep_duration"] = round(result["sleep_duration"] / 3_600_000_000_000, 1)
    
    return result