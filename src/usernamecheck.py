
import re

def check_username(username: str) -> tuple[bool, str]:
    """
    校验《我的世界》Java版玩家用户名是否合法
    
    Args:
        username (str): 输入的玩家游戏名称
        
    Returns:
        tuple[bool, str]: (是否合法, 提示信息)
    """
    # 1. 基础类型与边界检查
    if not username:
        return False, "用户名不能为空"
        
    if not isinstance(username, str):
        return False, "用户名必须是字符串"

    # 2. 长度检查（方便给用户精准的 UI 提示）
    if len(username) < 3:
        return False, "用户名太短了，至少需要 3 个字符"
    if len(username) > 16:
        return False, "用户名太长了，最多允许 16 个字符"

    # 3. 核心正则表达式校验
    # ^[a-zA-Z0-9_]{3,16}$
    # ^ 匹配开头，$ 匹配结尾，中间只允许字母、数字和下划线
    pattern = r"^[a-zA-Z0-9_]{3,16}$"
    
    if re.match(pattern, username):
        return True, "用户名合法"
    else:
        # 如果长度没问题但没匹配成功，说明包含了非法字符
        # 比如中文字符、空格、减号、标点符号等
        if " " in username:
            return False, "用户名中不能包含空格"
        return False, "用户名包含非法字符（只允许字母、数字和下划线）"

# ==================== 测试用例 ====================
if __name__ == "__main__":
    test_cases = [
        "Steve",          # 合法
        "Alex_666",       # 合法
        "notch",          # 合法
        "Ab",             # 太短
        "VeryLongUsernamePlayer", # 太长 (22位)
        "Steve Pro",      # 包含空格
        "Steve-Pro",      # 包含减号
        "史蒂夫",          # 包含中文
        "Alex!",          # 包含感叹号
    ]

    print("--- 启动器用户名校验测试 ---")
    for case in test_cases:
        is_valid, msg = check_username(case)
        status = "✅ 通过" if is_valid else "❌ 拒绝"
        print(f"输入: {case:<25} 结果: {status:<5} 原因: {msg}")