
import hashlib
import uuid

def get_offline_uuid(player_name: str) -> str:
    # 1. 构造基础字符串
    base_string = f"OfflinePlayer:{player_name}"
    
    # 2. 计算MD5
    md5_bytes = hashlib.md5(base_string.encode('utf-8')).digest()
    
    # 3. 设置UUID版本和变体 (UUID v3)
    # 将第7个字节的高四位设置为 0x3
    md5_bytes = bytearray(md5_bytes)
    md5_bytes[6] = (md5_bytes[6] & 0x0F) | 0x30
    # 将第9个字节的高两位设置为 0x2
    md5_bytes[8] = (md5_bytes[8] & 0x3F) | 0x80
    
    # 4. 格式化为标准UUID字符串
    return str(uuid.UUID(bytes=bytes(md5_bytes)))

