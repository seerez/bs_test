import json
import os

from django.shortcuts import redirect, render
from dotenv import load_dotenv

from transactions.bcschain import BCSNet
from transactions.models import Transaction

load_dotenv()

bcsnet = BCSNet()


def index(request):
    """Представление страницы транзакций"""
    context = {
        'transactions': Transaction.objects.all()
    }
    return render(request, 'index.html', context)


def update(request):
    """Представление страницы update"""
    TX = os.getenv('TX')
    signed_tx = bcsnet.create_tx(
        TX,
        [(bcsnet.getnewaddress(), 1)]
    )

    # response 500
    answer = bcsnet.sendrawtransaction(signed_tx)

    decoded_tx = bcsnet.decoderawtransaction(signed_tx)

    Transaction(
        transaction_pk=decoded_tx['txid'],
        value=0.00000001,
        jsontext=json.dumps(decoded_tx)
    ).save()
    return redirect('blochain:index')


def tx(request, txid):
    """Представление tx/..."""
    txobject = Transaction.objects.get(transaction_pk=txid)
    context = {
        'txobject': txobject
    }
    return render(request, 'tx.html', context)
