import json
import inspect

def read_db(json_name:str) -> dict:
    """returns contents of db.json as dict else empty dict"""
    try:
        with open(f'db/{json_name}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Reading json error: {e}")
        # if bot and SUPERADMIN:
        #     asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        return {}
    
def write_grpups_dict(json_name:str, column_name:str, key: str, value:str) -> bool:
    """
    Writes to groups_dict file and returns True if successful else False

    groups_dict.json:

    "source_id": { "241511234": "Group name" },
    "destination_id": { "241511234": "Group name" },
    "groups_cache": { "-1001739925049": "[ANDIJON TOSHKENT TAKSI](https://t.me/tashkent_andijon1)" }

    """
    try:
        contents = read_db(json_name)
        if isinstance(contents[column_name], dict):
            contents[column_name][key] = value
            with open(f'db/{json_name}.json', 'w') as file:
                json.dump(contents, file, indent=4)
            return True
        else:
            print(f"This json doesn't include dict as value, it is {type(contents[column_name])}")
            return False
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)
        return False

def write_keywords_list(json_name:str, column_name:str, data: int) -> bool:
    """
    Writes to keywords.json file and returns True if successful else False

    keywords.json:

    "admins": [
        123456789,
        987654321
    ],

    "negatives": [
        "negative1",
        "negative2"
    ],

    "keywords": [
        "keyword1",
        "keyword2"
    ]
    """
    try: 
        contents = read_db(json_name)
        if isinstance(contents[column_name], list):
            contents[column_name].append(data)
            with open(f"db/{json_name}.json", 'w') as file:
                json.dump(contents, file, indent=4)
            return True
        else:
            print(f"This json doesn't include list as value, it is {type(contents[column_name])}")
            return False
    except Exception as e:
        print(f"Error at {inspect.currentframe().f_code.co_name}", e)

# print(write_grpups_dict('groups_dict', 'source_id', '-1002263265', 'Test group name'))
# print(write_keywords_list('keywords', 'admins', 25321432134))
