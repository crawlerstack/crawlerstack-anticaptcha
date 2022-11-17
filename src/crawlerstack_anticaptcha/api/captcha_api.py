"""base"""
import logging

from fastapi import APIRouter, File, Form, UploadFile

from crawlerstack_anticaptcha.services.captcha import CaptchaService
from crawlerstack_anticaptcha.services.category import CategoryService
from crawlerstack_anticaptcha.services.storage import StorageService
from crawlerstack_anticaptcha.services.update_record import UpdateRecordService
from crawlerstack_anticaptcha.utils.schema import Message

logger = logging.getLogger(f'{__name__}  {__name__}')
router = APIRouter()


@router.post('/identify/')
async def anticaptcha(
        category: str = Form(description='验证码类型参数'),
        image: UploadFile = File(description='默认为背景图片或验证码只需一张图像的情况'),
        fore_image: UploadFile = File(default=None, description='前景图,例如滑块验证码中的滑块部分'),
        extra_content: str = Form(default=None, description='额外描述，例如点选文字中文字内容'),
        # user_agent: Union[str, None] = Header(default=None)
) -> Message:
    """
    Based on the request parameters,
    the corresponding captcha is identified and the result is returned
    """
    captcha_service = CaptchaService(
        bg_image=image, fore_image=fore_image, category=category, extra_content=extra_content
    )
    result_message = await captcha_service.check()
    return result_message


@router.put('/record/{record_id}')
async def record(
        record_id: str, success: bool = Form()
) -> Message:
    """
    The interface that counts whether the captcha is parsed successfully
    """
    update = UpdateRecordService(success, record_id)
    result = await update.update()
    return result


@router.post('/categories')
async def create_captcha_category(name: str = Form()) -> Message:
    """添加验证码分类"""
    category = CategoryService(name=name)
    return await category.create()


@router.patch('/categories/{category_id}')
async def update_captcha_category(
        category_id: int, name: str = Form()
) -> Message:
    """修改验证码类型"""
    category = CategoryService(category_id=category_id, name=name)
    return await category.update()


@router.get('/categories')
async def get_category() -> Message:
    """Query captcha category list"""
    category = CategoryService()
    return await category.get_all()


@router.post('/storages')
async def create_storage_config(
        name: str = Form(), uri: str = Form()
) -> Message:
    """添加存储配置"""
    storage = StorageService(name=name, uri=uri)
    return await storage.create()


@router.patch('/storages/{storage_id}')
async def update_storage(
        storage_id: int, default: bool = Form()
) -> Message:
    """修改默认存储位置"""
    storage = StorageService(storage_id=storage_id, default=default)
    return await storage.update()


@router.delete('/storages/{storage_id}', include_in_schema=False)  # 文档中不展示
async def delete_storage(storage_id: int) -> Message:
    """
    删除存储配置

    用户禁止调用
    :param storage_id:
    :return:
    """
    storage = StorageService(storage_id=storage_id)
    return await storage.delete_by_id()


@router.get('/storages/{storage_id}')
async def get_storage_by_id(storage_id: int) -> Message:
    """获取存储配置详情"""
    storage = StorageService(storage_id=storage_id)
    return await storage.get_by_id()


@router.get('/storages')
async def get_all_storages() -> Message:
    """查询所有存储配置"""
    storage = StorageService()
    return await storage.get_all()
