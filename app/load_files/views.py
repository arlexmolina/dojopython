from datetime import datetime, timedelta

from flask import redirect, url_for, flash, request, render_template, make_response, jsonify
from werkzeug.datastructures import CombinedMultiDict

from app import global_data
from . import load_files
from . import utils as load_files_utils
from .forms import UploadForm


@load_files.route('/search', methods=['GET'])
def search():
    location = request.args.get('location')
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


