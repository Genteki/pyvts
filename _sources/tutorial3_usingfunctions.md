# Using functions

You could use different functions to do different tings.

Note it would be better to use `await vts.close()` at the end of every function. And use `await vts.connect(); await vts.request_authenticate()` at the beginning of every function.

```python
import pyvts
import asyncio

async def connect_auth(myvts):
    ''' functions to get authenticated '''
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()
    await myvts.close()

async def trigger(myvts):
    ''' function to trigger hotkey '''
    await myvts.connect()
    await myvts.request_authenticate()
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    print(response_data)
    hotkey_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["name"])
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[0])
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()

if __name__ == "__main__":
    ''' using different functions '''
    myvts = pyvts.vts()
    asyncio.run(connect_auth(myvts))
    asyncio.run(trigger(myvts))
```
