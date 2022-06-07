from drf_yasg import openapi


def creators_filter_params():
    distance = openapi.Parameter('distance', openapi.IN_QUERY,
                                 description="Enter  distance",
                                 type=openapi.TYPE_INTEGER)
    longitude = openapi.Parameter('lon', openapi.IN_QUERY,
                                  description="Longitude",
                                  type=openapi.TYPE_NUMBER)
    latitude = openapi.Parameter('lat', openapi.IN_QUERY,
                                 description="Longitude",
                                 type=openapi.TYPE_NUMBER)
    return [distance, longitude, latitude]


def get_query():
    query = openapi.Parameter('query', openapi.IN_QUERY, description="enter query",
                              type=openapi.TYPE_STRING)
    return [query]
