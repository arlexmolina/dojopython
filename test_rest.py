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
    TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0Mzg3ZGUyMDUxMWNkNDgzYTIwZDIyOGQ5OTI4ZTU0YjNlZTBlMDgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcmVudHJvb21zLTIwMTkyIiwiYXVkIjoicmVudHJvb21zLTIwMTkyIiwiYXV0aF90aW1lIjoxNTkxMjQwNTE4LCJ1c2VyX2lkIjoiQ1JkZzdjVnpYN2JZTjRJTlVTa3FXTVNxN1BwMiIsInN1YiI6IkNSZGc3Y1Z6WDdiWU40SU5VU2txV01TcTdQcDIiLCJpYXQiOjE1OTEyNDA1MTgsImV4cCI6MTU5MTI0NDExOCwiZW1haWwiOiJhcnJlbmRhbWllbnRvc25qc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYXJyZW5kYW1pZW50b3NuanNAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.Q4dBmm9YQeUSHwf6jAwvpm7KzEuRZwenIEuTlXNyfP-Ov3r5b-1XMvxp8qp4qimPUMduUlqpeWEd8F1uFS1s9TwO5pEuNoSJKCOsOqc1twDp0XZQUY2L2RO7jptDOr0PKtKUMbGGSJ7mXJUrGtTuq1nD14aBSQywVpq1_NXShxDIOaZOzDmD9sH0JHpwFEK3z7HdSMdBeF6I6D0kr3w2cKPr1ectacc4L5IgftdGyWtGG7w5mB7EFLh2KD-Fc3W-iEossXuX3C0I1HCbxWYALoxEGYoH9mkm8CbWV2okRwEnV6JCbMs6f6xl3Ou92S47ODIq-jzHa_VZcECqYNrF3Q'

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
        headers={'authtoken': self.TOKEN}
        r = self.app.get(self.API_USER, headers=headers)
        self.assertEqual(r.status_code, 200)
        json_response = r.get_json()
        self.assertIsNotNone(json_response[0]['agency'])

    def test_04_search(self):
        r = self.app.get(self.API_SEARCH)
        self.assertEqual(r.status_code, 200)
        json_response = r.get_json()
        self.assertIsNotNone(json_response[0]['property_name'])
        self.assertEqual(json_response[0]['property_name'],  'Apartamento en El poblado')

    def test_05_post_reserve_error_token(self):
        r = self.app.post(self.API_RESERVE, data=dict(checkin="2020-02-06", checkout="2020-02-10", email="arlex.molina@udea.edu.co", name="Mauricio Molina", id_room="1" ))
        json_response = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(json_response)
        self.assertEqual(json_response, {'error': 'authorization required'})

    def test_06_post_reserve_error(self):
        r = self.app.post(self.API_RESERVE, data=json.dumps(dict(checkout="2020-02-10",
                email="arlex.molina@udea.edu.co", name="Mauricio Molina", id_room=1 )),
                          content_type='application/json',
                          headers={'authtoken': self.TOKEN})
        json_response = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(json_response)
        self.assertEqual(json_response, {'error': 'Ocurrio un fallo al ingresar la reserva'})

    def test_07_post_reserve_succes(self):
        r = self.app.post(self.API_RESERVE, data=json.dumps(dict(checkin="2020-02-06", checkout="2020-02-10",
                email="arlex.molina@udea.edu.co", name="Mauricio Molina", id_room=1 )),
                          content_type='application/json',
                          headers={'authtoken': self.TOKEN})
        json_response = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(json_response['id_booking'])

    def test_08_mockable(self):
        r = self.app.get(self.API_ROOMS)
        rr = self.app.get(self.API_MOCK)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(rr.status_code, 200)
        json_response = r.get_json()
        json_response_mock = rr.get_json()
        self.assertIsNotNone(json_response)
        self.assertIsNotNone(json_response_mock)
        self.assertEqual(json_response, json_response_mock)
