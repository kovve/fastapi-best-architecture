import asyncio
asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)
import aiomqtt


async def main():
    async with aiomqtt.Client(
        hostname="127.0.0.1",
        port=1883,
    ) as client:

        while True:

            await client.publish(
                "device/001/status",
                "hello world"
            )

            print("publish success")

            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())