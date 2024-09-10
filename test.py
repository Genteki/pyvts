import pyvts
import asyncio

async def main():
    myvts = pyvts.vts()
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()  # use token
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    print(response_data)
    hotkey_list = []
    for hotkey in response_data['data']['availableHotkeys']:
        hotkey_list.append(hotkey['name'])
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[0])
    await myvts.request(send_hotkey_request) # send request to play 'My Animation 1'
    await myvts.close()

if __name__ == "__main__":
    asyncio.run(main())