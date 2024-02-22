import asyncio
import runner


async def main():
    await runner.dp.start_polling(runner.bot)


if __name__ == '__main__':
    asyncio.run(main())
