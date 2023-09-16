from telethon import TelegramClient, events

# bot_token = ''


def readFile(input_file):
    id_array, name_array, username_array = [], [], []
    for line in input_file:
        help_array = line.split('-')
        id_array.append(help_array[0])
        name_array.append(help_array[1])
        username_array.append(help_array[2].replace("\n", ""))

    return id_array, name_array, username_array


def sendMessage(client, username, message):
    async def main():
        await client.send_message(username, message)

    with client:
        client.loop.run_until_complete(main())


def sendFile(client, username, file_address):
    async def main():
        await client.send_file(username, file_address)

    with client:
        client.loop.run_until_complete(main())


api_id = ''
api_hash = ''
client = TelegramClient('anon', api_id, api_hash)

input_file = open("input.txt", "r")

id_array, name_array, username_array = readFile(input_file)

for i in range(len(username_array)):
    username = username_array[i]
    file_address = 'Files/' + name_array[i] + '.pdf'
    sendMessage(client, username, 'This is first test')
    sendFile(client, username, file_address)
