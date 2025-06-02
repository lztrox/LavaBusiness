from ..types.models import Invoice, InvoiceStatus, Payoff, PayoffStatus
from ..types.models import Balance, PayMethods, PayoffTariffs

class ResponseProcessor:
    @classmethod
    def process(cls, *args, **kwargs):
        return cls._process(*args, **kwargs)

    @classmethod
    def _process(cls, *args, **kwargs):
        order_id = kwargs.get('order_id')
        response = kwargs['response']
        response_type = kwargs['response_type']

        processor, model = cls._get_response_processors(response_type=response_type)
        response_data = processor(response=response)
        if order_id:
            model_data = model(order_id, **response_data)
        else:
            model_data = model(**response_data)

        return model_data

    @classmethod
    def _get_response_processors(cls, response_type: str):
        if response_type == 'invoice_created':
            return cls._process_invoice_response_data, Invoice
        elif response_type == 'invoice_status':
            return cls._process_invoice_status_response_data, InvoiceStatus
        elif response_type == 'payoff_created':
            return cls._process_payoff_response_data, Payoff
        elif response_type == 'payoff_status':
            return cls._process_payoff_status_response_data, PayoffStatus
        elif response_type == 'balance':
            return cls._process_balance_response_data, Balance
        elif response_type == 'pay_methods':
            return cls._process_pay_methods_response_data, PayMethods
        elif response_type == 'payoff_tariffs':
            return cls._process_payoff_tariffs_response_data, PayoffTariffs
        else:
            raise ValueError(f'Unknown response type: {response_type}')

    @staticmethod
    def _process_invoice_response_data(response: dict):
        response_data = response['data']
        data = {
            'invoice_id': response_data['id'],
            'amount': response_data['amount'],
            'expire_date': response_data['expired'],
            'url': response_data['url'],
            'comment': response_data['comment']
        }
        return data

    @staticmethod
    def _process_invoice_status_response_data(response: dict):
        response_data = response['data']
        data = {
            'order_id': response_data['order_id'],
            'invoice_id': response_data['id'],
            'status': response_data['status'],
            'amount': response_data['amount'],
            'expire_date': response_data['expired'],
            'full_response': response_data
        }
        return data
    
    @staticmethod
    def _process_payoff_response_data(response: dict):
        response_data = response['data']
        data = {
            'payoff_id': response_data['payoff_id']
        }
        return data

    @staticmethod
    def _process_payoff_status_response_data(response: dict):
        response_data = response['data']
        data = {
            'order_id': response_data['orderId'],
            'payoff_id': response_data['id'],
            'status': response_data['status'],
            'amount': response_data['amountPay'],
            'fee': response_data['commission'],
            'amount_recieve': response_data['amountReceive'],
            'service': response_data['service'],
            'wallet': response_data['wallet']
        }
        return data

    @staticmethod
    def _process_balance_response_data(response: dict):
        response_data = response['data']
        data = {
            'balance': response_data['balance'],
            'freeze_balance': response_data['freeze_balance']
        }
        return data

    @staticmethod
    def _process_pay_methods_response_data(response: dict):
        response_data = response['data']
        data = {
            'methods': response_data
        }
        return data

    @staticmethod
    def _process_payoff_tariffs_response_data(response: dict):
        response_data = response['data']
        data = {
            'tariffs': response_data['tariffs']
        }
        return data