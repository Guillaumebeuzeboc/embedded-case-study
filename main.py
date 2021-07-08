import asyncio

from controllers.commander import Commander


async def main():
    Commander()


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
