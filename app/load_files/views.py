from datetime import datetime, timedelta
import pandas as pd
from flask import redirect, url_for, flash, request, render_template, make_response, jsonify
from sqlalchemy import create_engine
from werkzeug.datastructures import CombinedMultiDict
import instance.config as instance_config
import pandas as pd
from .. import db
from app import global_data
from . import load_files
from . import utils as load_files_utils
from .forms import UploadForm
import numpy as np
import codecs, json

engine = create_engine(instance_config.SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
select_propiedades = 'SELECT *, PROPIEDAD.idAgencia as agencia FROM innodb.PROPIEDAD  inner join innodb.CIUDADES on PROPIEDAD.idCiudad = CIUDADES.idCiudad  inner join innodb.AGENCIA on AGENCIA.idAgencia = PROPIEDAD.idAgencia where idPropiedad = %(id)s;'

@load_files.route('/<id>', methods=['GET'])
def rooms(id):

    propiedades = pd.read_sql(select_propiedades, con=db.engine, params={'id':id})
    fotos = pd.read_sql("FOTO", con=engine)
    servicios = pd.read_sql("SERVICIOS", con=engine)
    fotos_propiedades = fotos[fotos['idPropiedad'] == id]
    servicios_propiedades = servicios[servicios['idPropiedad'] == id]

    servicios_propiedades = servicios_propiedades.drop(['idPropiedad'], axis=1)
    json_servicios = servicios_propiedades.to_json(orient='values')

    #propiedad = propiedades.to_json(orient='split')
    propiedad = propiedades.iloc[0]

    fotos_propiedades = fotos_propiedades.drop(['idFoto', 'idPropiedad', 'tipo'], axis=1)
    json_fotos = fotos_propiedades.to_json(orient='records')

    print(propiedad)
    print('propiedad')

    r = make_response(jsonify(
        id=propiedad.idPropiedad,
        images=json_fotos,
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
        property_name=propiedad.propietario,
        rating=propiedad.ratingPropiedad,
        services=json_servicios
    ))


    return r


@load_files.route('/search', methods=['GET'])
def search():
    location = request.args.get('location')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')

    agencia = pd.read_sql("AGENCIA", con=engine)

    if(location == 'MDE'):
        r = make_response(jsonify(
            id="ID",
            thumbnail="URL",
            location={
                "name":"Medellin",
                "code":"MDE",
                "latitude":"",
                "longitude":""
            },
            price="",
            currency="COP",
            property_name="NAME",
            rating=0.0,
            agency={
                "name":"Nutibara",
                "id":"1234"
            }
        ))

        agencia = pd.read_sql("AGENCIA", con=engine)
        print('***************** agencia')
        print(agencia)

    else:
        r = make_response(jsonify())
    r.mimetype = 'application/json'
    return r

@load_files.route('/load_account_files', methods=['GET', 'POST'])
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


