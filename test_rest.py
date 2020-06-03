import io
import os
import json
import unittest
from app import create_app


__author__ = 'Roberto Mucci (r.mucci@cineca.it)'


class TestDataObjects(unittest.TestCase):

    API_ROOMS = 'http://localhost:8000/rooms/1'
    API_USER = 'http://localhost:8000/rooms/booking/darlexx08@gmail.com'
    API_SEARCH = 'http://localhost:8000/rooms/search?location=MDE&checkin=2020-01-01&checkout=2020-01-01'
    API_RESERVE = 'http://localhost:8000/rooms/booking'
    API_MOCK = 'https://demo3205276.mockable.io/rooms/1'

    @classmethod
    def setUpClass(self):
        "set up test fixtures"
        print('### Setting up flask server ###')
        config_name = os.getenv('FLASK_ENV')
        app = create_app(config_name)
        # app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_01_get_verify(self):
        r = self.app.get(self.API_ROOMS)
        self.assertEqual(r.status_code, 200)

    def test_02_get_agency(self):
        r = self.app.get(self.API_ROOMS)
        self.assertEqual(r.status_code, 200)
        json_response = r.get_json()
        self.assertIsNotNone(json_response['agency'])

    def test_03_get_reserves(self):
        r = self.app.get(self.API_USER)
        self.assertEqual(r.status_code, 200)
        json_response = r.get_json()
        self.assertIsNotNone(json_response[0]['agency'])

    def test_04_search(self):
        r = self.app.get(self.API_SEARCH)
        self.assertEqual(r.status_code, 200)
        json_response = r.get_json()
        self.assertIsNotNone(json_response[0]['property_name'])
        self.assertEqual(json_response[0]['property_name'],  'Apartamento en El poblado')

    def test_05_post_reserve_error(self):
        r = self.app.post(self.API_RESERVE, data=dict(checkin="2020-02-06", checkout="2020-02-10", email="arlex.molina@udea.edu.co", name="Mauricio Molina", id_room="1" ))
        json_response = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(json_response)
        self.assertEqual(json_response, {'error': 'Ocurrio un fallo al ingresar la reserva'})

    def test_06_post_reserve_succes(self):
        r = self.app.post(self.API_RESERVE, data=json.dumps(dict(checkin="2020-02-06", checkout="2020-02-10", email="arlex.molina@udea.edu.co", name="Mauricio Molina", id_room=1 )), content_type='application/json')
        json_response = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(json_response['id_booking'])

    def test_07_mockable(self):
        r = self.app.get(self.API_ROOMS)
        rr = self.app.get(self.API_MOCK)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(rr.status_code, 200)
        json_response = r.get_json()
        json_response_mock = rr.get_json()
        self.assertIsNotNone(json_response)
        self.assertIsNotNone(json_response_mock)
        self.assertEqual(json_response, json_response_mock)
