import asyncio
import json
from rubpy import Client

SESSION = "moslm2"
PROGRESS_FILE = "/storage/emulated/0/Download/moslm2_progress.json"
DELAY = 0.5

async def main():
    app = Client(SESSION)
    channels = {}
    seen_pages = set()

    try:
        async with app:
            await app.start()

            me = await app.get_me()
            data_me = me.to_dict
            print("ورود موفق!")

            start_id = None
            page = 0

            while True:
                result = await app.get_chats(start_id=start_id)
                data = result.to_dict
                chats = data.get("chats", []) or []
                page += 1

                for chat in chats:
                    guid = chat.get("object_guid", "")

                    if guid.startswith("c0"):
                        obj = chat.get("abs_object") or {}
                        title = obj.get("title", "بدون نام")
                        channels[guid] = title

                print("صفحه:", page)
                print("تعداد کانال:", len(channels))

                next_id = data.get("next_start_id")
                has_more = data.get("has_continue", False)

                if not has_more or not next_id:
                    break

                if next_id in seen_pages:
                    break

                seen_pages.add(next_id)
                start_id = next_id

            if not channels:
                print("کانالی پیدا نشد.")
                return

            print("\nفهرست کانال‌ها:")
            for i, (guid, title) in enumerate(channels.items(), 1):
                print(i, title)

            confirm = input(
                "\nبرای ترک کانال‌ها بنویس بله: "
            ).strip()

            if confirm != "بله":
                print("عملیات لغو شد.")
                return

            results = []

            for i, (guid, title) in enumerate(channels.items(), 1):
                try:
                    response = await app.builder(
                        name="joinChannelAction",
                        input={
                            "channel_guid": guid,
                            "action": "Leave"
                        },
                        dict=True
                    )

                    update = {}
                    if isinstance(response, dict):
                        update = response.get("chat_update", {})

                    if (
                        update.get("object_guid") == guid
                        and update.get("action") == "Delete"
                    ):
                        status = "موفق"
                    else:
                        status = "نامشخص"

                    print(i, title, status)

                    results.append({
                        "guid": guid,
                        "title": title,
                        "status": status
                    })

                except Exception as e:
                    print(i, title, "خطا:", str(e))
                    results.append({
                        "guid": guid,
                        "title": title,
                        "status": "خطا",
                        "error": str(e)
                    })

                with open(
                    PROGRESS_FILE,
                    "w",
                    encoding="utf-8"
                ) as f:
                    json.dump(
                        results,
                        f,
                        ensure_ascii=False,
                        indent=2
                    )

                await asyncio.sleep(DELAY)

            print("\nعملیات تمام شد.")
            print("تعداد کانال‌ها:", len(channels))
            print("گزارش:", PROGRESS_FILE)

    except Exception as e:
        print("خطا:", type(e).__name__, str(e))


asyncio.run(main())