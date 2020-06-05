from datetime import datetime, timedelta

import pandas as pd
from flask import redirect, url_for, flash, request, render_template, make_response, jsonify
from flask_cors import cross_origin
from flask_mail import Message
from sqlalchemy import create_engine
from sqlalchemy import text
from werkzeug.datastructures import CombinedMultiDict

import instance.config as instance_config
from app import global_data
from app import mail
from . import reserve
from .. import db
from .. import email_utils
import json
from firebase_admin import auth

engine = create_engine(instance_config.SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
select_propiedad = 'SELECT *, PROPIEDAD.idAgencia as agencia FROM innodb.PROPIEDAD  inner join innodb.CIUDADES on ' \
                    'PROPIEDAD.idCiudad = CIUDADES.idCiudad  inner join innodb.AGENCIA on AGENCIA.idAgencia = PROPIEDAD.idAgencia ' \
                    'where idPropiedad = %(id)s;'
select_propiedades = 'SELECT *, PROPIEDAD.idAgencia as agencia FROM innodb.PROPIEDAD  inner join innodb.CIUDADES on ' \
                    'PROPIEDAD.idCiudad = CIUDADES.idCiudad  inner join innodb.AGENCIA on AGENCIA.idAgencia = PROPIEDAD.idAgencia ' \
                    'where idPropiedad NOT IN (SELECT distinct idPropiedad FROM innodb.RESERVA where (fechaInicio between %(date1)s and %(date2)s) ' \
                    'or (fechaFinal between %(date3)s and %(date4)s)) ' \
                    'and codigoCiudad = %(codigo)s; '

select_reservas = 'SELECT *, PROPIEDAD.idAgencia as agencia, RESERVA.idPropiedad as idBooking FROM innodb.RESERVA inner join innodb.PROPIEDAD on PROPIEDAD.idPropiedad = RESERVA.idPropiedad inner join innodb.CIUDADES on ' \
                    'PROPIEDAD.idCiudad = CIUDADES.idCiudad  inner join innodb.AGENCIA on AGENCIA.idAgencia = PROPIEDAD.idAgencia ' \
                    'where email = %(email)s; '

select_id = 'SELECT max(idReserva) + 1 as id FROM innodb.RESERVA;'
insert_exp = text('INSERT INTO RESERVA (idReserva, idPropiedad, fechaInicio, fechaFinal, estado, nombreComprador, email) ' \
                  'VALUES (:idReserva, :idPropiedad, :fechaInicio, :fechaFinal, 1, :nombreComprador, :email)')

numeros = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
valor_romano=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']

# nuevo metodo
@reserve.route('test/<numero>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def test(numero):
    numero = int(numero)
    pendiente = numero
    resultado = ''

    for i in range(len(numeros)):
        pendiente_aux = pendiente
        resultado_aux = resultado
        while pendiente_aux >= numeros[i]:
            resultado_aux = resultado_aux + valor_romano[i]
            pendiente_aux = pendiente_aux - numeros[i]
        pendiente = pendiente_aux
        resultado = resultado_aux

    r = make_response(jsonify(resultado))

    return r

# nuevo metodo
@reserve.route('/<id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def rooms(id):
    propiedades = pd.read_sql(select_propiedad, con=db.engine, params={'id':id})
    fotos = pd.read_sql("FOTO", con=engine)
    servicios = pd.read_sql("SERVICIOS", con=engine)
    fotos_propiedades = fotos[fotos['idPropiedad'] == id]
    servicios_propiedades = servicios[servicios['idPropiedad'] == id]

    servicios_propiedades = servicios_propiedades.drop(['idPropiedad'], axis=1)
    json_servicios = servicios_propiedades.reset_index().to_dict(orient='list')
    xjsdon = json_servicios['nombreServicio']

    propiedad = propiedades.iloc[0]

    fotos_propiedades = fotos_propiedades.drop(['idFoto', 'idPropiedad'], axis=1)
    json_fotos = fotos_propiedades.to_json(orient='records')
    yjsdon = json.loads(json_fotos)

    r = make_response(jsonify(
        id=propiedad.idPropiedad,
        images=yjsdon,
        location={
            "name":propiedad.nombreCiudad,
            "code":propiedad.codigoCiudad,
            "latitude":propiedad.latitute,
            "longitude":propiedad.longitute
        },
        price=propiedad.precioNoche,
        currency=propiedad.currency,
        agency={
            "id":propiedad.agencia,
            "name":propiedad.nombreAgencia,
            "logo_url":propiedad.logo
        },
        property_name=propiedad.nombrePropiedad,
        rating=propiedad.ratingPropiedad,
        services=xjsdon
    ))

    return r

@reserve.route('/booking/<user_id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def reserves(user_id):
    try:
        try:
            token = request.headers['authtoken']
        except Exception as e:
            token = request.headers['Authtoken']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
    except Exception as e:
        print('********************* error')
        print(e)
        r = make_response(jsonify(error="authorization required"))
        return r
    propiedades = pd.read_sql(select_reservas, con=db.engine, params={'email':user_id})
    filtro = []
    now = datetime.now()
    try:
        for index, propiedad in propiedades.iterrows():
            data = {
                "id_room":propiedad.idBooking,
                "thumbnail":propiedad.urlMiniatura,
                "location":{
                    "name":propiedad.nombreCiudad,
                    "code":propiedad.codigoCiudad,
                    "latitude":propiedad.latitute,
                    "longitude":propiedad.longitute
                },
                "price":propiedad.precioNoche,
                "currency":propiedad.currency,
                "agency":{
                    "id":propiedad.agencia,
                    "name":propiedad.nombreAgencia
                },
                "property_name":propiedad.nombrePropiedad,
                "id_booking":str(propiedad.idReserva),
                "checkin":propiedad.fechaInicio.strftime("%Y-%m-%d"),
                "checkout":propiedad.fechaFinal.strftime("%Y-%m-%d")
            }
            filtro.append(data)
        r = make_response(jsonify(filtro))
    except Exception as e:
        print('********************* error')
        print(e)

    r = make_response(jsonify(filtro))
    r.mimetype = 'application/json'
    return r

@reserve.route('/booking', methods=['POST'])
@cross_origin() # allow all origins all methods.
def booking():
    try:
        try:
            token = request.headers['authtoken']
        except Exception as e:
            token = request.headers['Authtoken']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
    except Exception as e:
        print('********************* error')
        print(e)
        r = make_response(jsonify(error="authorization required"))
        return r
    try:
        content = request.json
        checkin = content['checkin']
        checkout = content['checkout']
        email = content['email']
        name = content['name']
        id_room = content['id_room']

        if checkin is None or checkout is None or email is None or name is None or id_room is None:
            r = make_response(jsonify(error="Todos los campos son obligatrios"))
            return r

        ids = pd.read_sql(select_id, con=db.engine, params={})
        id = ids = ids.iloc[0]
        idReserva = int(ids.id)

        engine.execute(insert_exp, idPropiedad=id_room,
                              fechaInicio=checkin,
                              fechaFinal=checkout,
                              nombreComprador=name,
                              email=email,
                              estado=1,
                              idReserva=idReserva)

        r = make_response(jsonify(
            id_booking=idReserva,
            checkin=checkin,
            checkout=checkout,
            email=email,
            name=name,
            id_room=id_room
        ))
        msg_dicts = []
        message_dict = email_utils.message_to_dict(to=[email],
                                                   subject="Conformación de reserva",
                                                   template='alerts_generated')
        msg_dicts.append(message_dict)
        email_utils.send_async_emails(msg_dicts)

    except Exception as e:
        r = make_response(jsonify(error="Ocurrio un fallo al ingresar la reserva"))

    return r

def send_async_emails(msg_dicts):
    with mail.connect() as conn:
        for msg_dict in msg_dicts:
            msg = Message()
            msg.__dict__.update(msg_dict)
            conn.send(msg)

@reserve.route('/search', methods=['GET'])
@cross_origin() # allow all origins all methods.
def search():
    location = request.args.get('location')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')

    propiedades = pd.read_sql(select_propiedades, con=db.engine, params={'date1':checkin, 'date2':checkout, 'date3':checkin, 'date4':checkout, 'codigo':location})
    filtro = []
    try:
        for index, propiedad in propiedades.iterrows():
            data = {
                "id":propiedad.idPropiedad,
                "thumbnail":propiedad.urlMiniatura,
                "location":{
                    "name":propiedad.nombreCiudad,
                    "code":propiedad.codigoCiudad,
                    "latitude":propiedad.latitute,
                    "longitude":propiedad.longitute
                },
                "price":propiedad.precioNoche,
                "currency":propiedad.currency,
                "agency":{
                    "id":propiedad.agencia,
                    "name":propiedad.nombreAgencia
                },
                "property_name":propiedad.nombrePropiedad,
                "rating":propiedad.ratingPropiedad
            }
            filtro.append(data)
    except Exception as e:
        print('********************* error')
        print(e)
    r = make_response(jsonify(filtro))

    r.mimetype = 'application/json'
    return r

@reserve.route('/load_account_files', methods=['GET', 'POST'])
def load_account_files():
    accounts_data_load_form = UploadForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST':
        event_metadata = {}
        if accounts_data_load_form.validate_on_submit():
            upload_type = request.form.get('upload_type')
            f = accounts_data_load_form.upload.data

            balances_df = load_files_utils.process_balances_file(f, upload_type)

            global_data.load_accounts_data('accounting', balances_df)
            return redirect(url_for('dashboard.homepage'))

        else:
            result_message = "El archivo no es válido. Debe ser un archivo de texto separado por algún caracter " \
                             "o un archivo de Excel"
            flash(result_message)

        event_metadata['result_message'] = result_message

    show_loading = False
    current_date = datetime.now()
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = current_date - timedelta(days=1)
    return render_template('load_files/load_account_files.html',
                           title="Dojo Python Panda",
                           active_page='daily_load',
                           daily_load_form=accounts_data_load_form,
                           show_loading=show_loading,
                           current_date=datetime.strftime(current_date, '%d/%m/%Y'))


@reserve.route('/user', methods=['POST'])
@cross_origin() # allow all origins all methods.
def user():
    content = request.json
    if content is None:
        content = request.form['_Response']

    content = json.loads(content)
    transactionId = content['TransactionId']
    redirectURL = "http://valemastest.s3-website-us-east-1.amazonaws.com/user?id="+transactionId
    return redirect(redirectURL)
