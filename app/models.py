class ReservaModel(object):
    @staticmethod
    def get_reserva_model():
        return AccountingComment

class AccountingComment(ReservaModel):
    __tablename__ = 'RESERVA'

