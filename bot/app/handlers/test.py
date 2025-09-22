from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.photo)
async def get_photo_file_id(message: Message):
    # Берём самое большое фото (последний элемент)
    file_id = message.photo[-1].file_id  
    
    print(f"file_id этой картинки:\n<code>{file_id}</code>")
    
    # Если хочешь сразу сохранить куда-то:
    # product = await get_product(current_product_id)
    # product.image = file_id
    # await session.commit()
