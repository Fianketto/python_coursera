import asyncio
import concurrent.futures


data_base = []


def run_server(host, port):    # '127.0.0.1', 8181
    @asyncio.coroutine
    def handle_connection(reader, writer):
        while True:
            try:
                data = yield from reader.read(1024)
                if data:
                    process_data(data, writer)
                else:
                    break
            except concurrent.futures.TimeoutError:
                break
        writer.close()

    loop = asyncio.get_event_loop()
    server_gen = asyncio.start_server(handle_connection, host, port, loop=loop)
    server = loop.run_until_complete(server_gen)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()


def process_data(data, writer):
    message = data.decode("utf-8")
    params = message.split()
    if len(params) == 0:
        send_error_message(writer)
    elif params[0] == 'put':
        try:
            put(writer, *params[1:])
        except BaseException:
            send_error_message(writer)
    elif params[0] == 'get':
        if len(params) != 2:
            send_error_message(writer)
        else:
            try:
                list_to_send = get(params[1])
                encoded_str_to_send = encode_list(list_to_send)
                writer.write(encoded_str_to_send)
            except:
                send_error_message(writer)
    else:
        send_error_message(writer)


def put(writer, metric, val, timestamp):
    global data_base
    inserted = False
    # check types
    if correct_types(val, timestamp):
        for i in range(len(data_base)):  # check timestamp existence
            if data_base[i][0] == metric and data_base[i][2] == timestamp:
                data_base[i] = (metric, float(val), timestamp)
                inserted = True
        if not inserted:
            data_base.append((metric, float(val), timestamp))
        writer.write(b"ok\n\n")
    else:
        send_error_message(writer)


def get(metric) -> list:
    global data_base
    if metric == '*':
        return data_base
    needed_list = [x for x in data_base if x[0] == metric]
    return needed_list


def encode_list(list_to_send: list) -> bytes:
    str_to_send = "ok"
    for x in list_to_send:
        str_to_send += f"\n{x[0]} {x[1]} {x[2]}"
    str_to_send += "\n\n"
    return str_to_send.encode("utf-8")


def send_error_message(writer):
    writer.write(b"error\nwrong command\n\n")


def correct_types(val, timestamp):
    try:
        float(val)
    except ValueError:
        return False

    try:
        int(timestamp)
    except ValueError:
        return False

    return True


#run_server('127.0.0.1', 8181)
