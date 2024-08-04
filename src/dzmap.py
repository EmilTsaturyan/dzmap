import asyncio
import pyfiglet

from parser import parser
from ports import PORTS_AND_SERVICES



async def check_port(ip: str, port: int):
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1)
        print(f'[+] Port: {port} | Protocol: {PORTS_AND_SERVICES[port]["protocol"]} | Service: {PORTS_AND_SERVICES[port]["service"]}')
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def check_ports(ip: str, start_port: int, end_port: int) -> None:
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(check_port(ip, port))
        if len(tasks) >= 2000:
            await asyncio.gather(*tasks)
            tasks = [] 
    if tasks:
        await asyncio.gather(*tasks)


def validate_port_range(port_range: str) -> tuple[int]:
    if port_range.count('-') == 1:
        start_port, end_port = port_range.split('-')
        try:
            start_port, end_port = int(start_port), int(end_port)
            if start_port >= 1 and end_port <= 65535 and start_port < end_port:
                return (start_port, end_port)
            else:
                return False
        except ValueError:
            return False
    else:
        return False

if __name__ == "__main__":
    Banner = pyfiglet.figlet_format('D Z M A P', font='standard')
    print(Banner)

    args = parser.parse_args()
    ports_range = validate_port_range(args.range)
    if ports_range:
        start_port, end_port = ports_range

        asyncio.run(check_ports(args.ip, start_port, end_port))
    else:
        print('Invalid arguments')