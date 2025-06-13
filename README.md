# LavaBusiness
[![PyPi Package Version](https://img.shields.io/pypi/v/lavabusiness?style=flat-square)](https://pypi.python.org/pypi/lavabusiness)
[![Supported python versions](https://img.shields.io/pypi/pyversions/lavabusiness)](https://pypi.python.org/pypi/lavabusiness)
[![License](https://img.shields.io/github/license/lztrox/lavabusiness?style=flat-square)](https://opensource.org/licenses/MPL-2.0)
[![Downloads](https://img.shields.io/pypi/dm/lavabusiness?style=flat-square)](https://pypi.org/project/lavabusiness/)
[![Issues](https://img.shields.io/github/issues/lztrox/lavabusiness?style=flat-square)](https://github.com/lztrox/lavabusiness/issues)

Asynchronous client for Lava.ru Business-API

Асинхронный клиент для работы с Lava.ru Бизнес-API 

## Examples
### Creating invoice
```python
import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    invoice = await api.create_invoice(100)
    print(f'Payment url: {invoice.url}')
    print(f'Invoice ID: {invoice.invoice_id}')

asyncio.run(main())
```
  
### Checking invoice status
```python
import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    INVOICE_ID = ""
    invoice = await api.invoice_status(INVOICE_ID)

    if invoice.status == 'success':
        print('Invoice paid')
    elif invoice.status == 'expired':
        print('Invoice expired')
    else:
        print('Waiting for payment')
    
asyncio.run(main())
```

### More examples: [`examples/`](https://github.com/lztrox/LavaBusiness/tree/master/examples)
### Detailed docs: https://lavabusiness.readthedocs.io/en/latest/
