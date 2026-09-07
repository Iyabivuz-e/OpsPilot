# I know this file could be separate based on the components, but we are just testing


class OpsService:
    def __init__(self):
        pass

    def get_orders(self, customer_id: str):
        pass

    def get_order(self, order_id: str):
        pass

    def cancel_order(self, order_id: str):
        pass

    def get_payments(self, customer_id: str):
        pass

    def get_payment(self, payment_id: str):
        pass

    def get_refunds(self, customer_id: str):
        pass

    def create_refunds(self):
        pass

    def get_refund(self, refund_id: str):
        pass

    def get_refund_eligibility(self):
        pass

    def get_returns(self, customer_id: str):
        pass

    def get_return(self, return_id: str):
        pass

    service = OpsService
