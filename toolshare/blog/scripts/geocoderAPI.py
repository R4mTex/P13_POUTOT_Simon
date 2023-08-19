import requests

# Put Your API Key Google Maps here (between quotes)
gmk = "AIzaSyD1ckgetM8cnzdgwd1XpEetOhxghe5w82M"


class Geocoder:
    def __init__(self, query):
        self.query = query

    def geocoderApiRequest(self):
        request = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={self.query}&key={gmk}")
        return request.json()

    def dataRequest(self):
        dataJson = self.geocoderApiRequest()

        if dataJson['status'] == 'OK':
            dataResults = []
            dataResults.extend(dataJson.get('results'))

            longName = [
                x.get('address_components', "None") for x in dataResults
            ]

            placeID = [
                x.get('place_id', "None") for x in dataResults
            ]

            geometry = [
                x.get('geometry', "None") for x in dataResults
            ]

            location = [
                x.get('location', 'None') for x in geometry
            ]

            lat = location[0]['lat']
            lng = location[0]['lng']
            return {
                'longName': longName[0][0]['long_name'],
                'status': dataJson['status'],
                'lat': lat,
                'lng': lng,
                'placeID': placeID
                }
        else:
            return {
                'status': dataJson['status'],
                }
