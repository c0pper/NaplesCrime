import geocoder

def convert_name_to_coords(name):
    g = geocoder.bing(f'{name}, 80133, Napoli, NA', key='Am9esTEL99oaLdr4dmuYtSJ5GJEoWSRaMpqZVsPmOZC5gyfjiASyAaCoAqYBvVBh')
    results = g.json
    if results:
        print(results['lat'], results['lng'])
        return {"lat": results['lat'], "lon": results['lng']}