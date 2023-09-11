import mock
from blog.scripts.geocoderApi import Geocoder


@mock.patch("blog.scripts.geocoderApi.requests.get")
def test_geocoder_api_request_get(mock_requests_get):
    sut = Geocoder(query='')

    mock_requests_get.return_value = mock.Mock(name='mock response', **{'status_code': 200, 'json.return_value': {}})

    assert sut.geocoderApiRequest() == {}
    mock_requests_get.assert_called_once_with(
        'https://maps.googleapis.com/maps/api/geocode/json?address=&key=AIzaSyD1ckgetM8cnzdgwd1XpEetOhxghe5w82M'
        )


@mock.patch("blog.scripts.geocoderApi.requests.get")
def test_date_request(mock_requests_get):
    sut = Geocoder(query='')

    mock_requests_get.return_value = mock.Mock(
        name='mock response', **{"status_code": 200,
                                 "json.return_value": {
                                    "status": "OK",
                                    "results": [
                                        {
                                            "address_components": [
                                                {
                                                    "long_name": "Paris",
                                                    "short_name": "Paris",
                                                    "types": [
                                                        "locality",
                                                        "political"
                                                    ]
                                                },
                                                {
                                                    "long_name": "Paris",
                                                    "short_name": "Paris",
                                                    "types": [
                                                        "administrative_area_level_2",
                                                        "political"
                                                    ]
                                                },
                                                {
                                                    "long_name": "Île-de-France",
                                                    "short_name": "IDF",
                                                    "types": [
                                                        "administrative_area_level_1",
                                                        "political"
                                                    ]
                                                },
                                                {
                                                    "long_name": "France",
                                                    "short_name": "FR",
                                                    "types": [
                                                        "country",
                                                        "political"
                                                    ]
                                                }
                                            ],
                                            "formatted_address": "Paris, France",
                                            "geometry": {
                                                "bounds": {
                                                    "northeast": {
                                                        "lat": 48.9021475,
                                                        "lng": 2.4698509
                                                    },
                                                    "southwest": {
                                                        "lat": 48.8155622,
                                                        "lng": 2.2242191
                                                    }
                                                },
                                                "location": {
                                                    "lat": 48.856614,
                                                    "lng": 2.3522219
                                                },
                                                "location_type": "APPROXIMATE",
                                                "viewport": {
                                                    "northeast": {
                                                        "lat": 48.9021475,
                                                        "lng": 2.4698509
                                                    },
                                                    "southwest": {
                                                        "lat": 48.8155622,
                                                        "lng": 2.2242191
                                                    }
                                                }
                                            },
                                            "partial_match": "true",
                                            "place_id": "ChIJD7fiBh9u5kcRYJSMaMOCCwQ",
                                            "types": [
                                                "locality",
                                                "political"
                                                ]
                                        }
                                    ]
                                }
                            }
                        )
    assert sut.dataRequest() == {'longName': 'Paris',
                                            'status': 'OK', 'lat': 48.856614, 'lng': 2.3522219,
                                            'placeID': ['ChIJD7fiBh9u5kcRYJSMaMOCCwQ']}
