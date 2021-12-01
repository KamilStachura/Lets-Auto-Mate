import asyncio
from scrapli.driver.core import AsyncIOSXEDriver
from device_list import DEVICES
from rich import print as rprint


async def gather_version(device):

    conn = AsyncIOSXEDriver(**device)
    await conn.open()
    prompt_result = await conn.get_prompt()
    version_result = await conn.send_command("show version")
    structured_result = version_result.genie_parse_output()["version"]["version_short"]
    await conn.close()
    return prompt_result, structured_result


async def main():
    coroutines = [gather_version(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        rprint(f"[green]DEVICE: {result[0]}[/green]")
        rprint(f"Version: {result[1]}")



asyncio.run(main())