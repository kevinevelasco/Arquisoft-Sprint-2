import redis

def test_redis_connection():
    try:
        # Conectar a Redis
        r = redis.StrictRedis(host='10.128.0.5', port=6379, db=0)

        # Probar almacenando un valor
        test_key = 'test_key'
        test_value = 'Hello, Redis!'
        r.set(test_key, test_value)

        # Intentar recuperar el valor almacenado
        retrieved_value = r.get(test_key)

        if retrieved_value:
            print(f"Connection to Redis successful! Stored value: {retrieved_value.decode('utf-8')}")
        else:
            print("Failed to store or retrieve data from Redis.")
    
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")

if __name__ == "__main__":
    test_redis_connection()
