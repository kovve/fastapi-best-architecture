import asyncio
import aiomqtt


async def main():
    async with aiomqtt.Client(
        hostname="127.0.0.1",
        port=1883,
    ) as client:

        await client.subscribe("device/#")

        async for message in client.messages:

            print("topic:", message.topic)
            print("payload:", message.payload.decode())


if __name__ == "__main__":
    asyncio.run(main())