import csv
import os
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
from io import BytesIO
import requests

# pip3 install playwright pillow
# playwright install

async def get_twitter_profile_image(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()  # シークレットモードを使用
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3000)  # sleep

        try:
            img_tag = await page.query_selector('img[alt="Image"]')
            profile_image_url = await img_tag.get_attribute('src') if img_tag else None
        except Exception as e:
            profile_image_url = None
        finally:
            await browser.close()

    return profile_image_url

def normalize_twitter_id(twitter_id):
    if twitter_id.startswith('https://x.com/'):
        return twitter_id.split('/')[-1]
    elif twitter_id.startswith('@'):
        return twitter_id[1:]
    else:
        return twitter_id

def download_and_save_image(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path)

async def main():
    # 出力ディレクトリを作成
    os.makedirs('out', exist_ok=True)

    with open('dat.tsv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            twitter_id = row['twitter ID']
            if twitter_id:
                normalized_id = normalize_twitter_id(twitter_id)
                profile_image_url = await get_twitter_profile_image(f'https://x.com/{normalized_id}/photo')
                if profile_image_url:
                    file_extension = profile_image_url.split('.')[-1].split('?')[0]  # クエリパラメータを除去
                    file_path = f"out/{row['通し番号']}.{file_extension}"
                    if not os.path.exists(file_path):
                        download_and_save_image(profile_image_url, file_path)
                        print(f"Saved image for {normalized_id} to {file_path}")
                    else:
                        print(f"Skipped image download for {normalized_id} because file already exists at {file_path}")
                else:
                    print(f"Failed to get profile image for {normalized_id}")
            else:
                print(f"No Twitter ID for 通し番号 {row['通し番号']}")

# 非同期関数を実行
asyncio.run(main())
