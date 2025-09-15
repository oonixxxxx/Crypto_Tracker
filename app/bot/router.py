from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession
from config import BACKEND_URL

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Hello, world!')

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Help!')

@router.message(Command('crypto'))
async def crypto_command(message: Message):
    async with ClientSession(base_url=BACKEND_URL) as session:
        async with session.get('/cryptocurrency') as resp:
            data = await resp.json()
    if isinstance(data, list) and data:
        first = data[0]
        name = first.get('name', 'Unknown')
        symbol = first.get('symbol', '')
        await message.answer(f"Top: {name} ({symbol})")
    else:
        await message.answer('No data')

@router.message(Command('crypto_id'))
async def crypto_id_command(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer('Usage: /crypto_id <id>')
        return
    currency_id = int(parts[1])
    async with ClientSession(base_url=BACKEND_URL) as session:
        async with session.get(f'/cryptocurrency/{currency_id}') as resp:
            data = await resp.json()
    name = data.get('name', 'Unknown')
    symbol = data.get('symbol', '')
    await message.answer(f"{name} ({symbol})")
    