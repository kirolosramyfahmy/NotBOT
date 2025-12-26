import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from playwright.async_api import async_playwright
from app.models.mission import Mission, MissionStatus

EVIDENCE_DIR = "/app/evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

class CrawlerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_mission(self, mission_id: int):
        mission = await self.db.get(Mission, mission_id)
        if not mission:
            return

        mission.status = MissionStatus.PROCESSING
        await self.db.commit()

        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()

            try:
                await page.goto(mission.target_url, timeout=30000, wait_until="domcontentloaded")
                brand = mission.brand_name
                js_script = """
                (brand) => {
                    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    let found = false;
                    const nodesToProcess = [];
                    while (node = walker.nextNode()) {
                        if (node.nodeValue.toLowerCase().includes(brand.toLowerCase())) {
                            found = true;
                            nodesToProcess.push(node);
                        }
                    }
                    for (const textNode of nodesToProcess) {
                        try {
                            const parent = textNode.parentNode;
                            if (parent && !['SCRIPT', 'STYLE', 'TEXTAREA'].includes(parent.tagName)) {
                                const span = document.createElement('span');
                                span.style.border = '3px solid red';
                                span.style.backgroundColor = 'yellow';
                                span.style.color = 'black';
                                span.style.fontWeight = 'bold';
                                const range = document.createRange();
                                range.selectNodeContents(textNode);
                                range.surroundContents(span);
                            }
                        } catch (e) {}
                    }
                    return found;
                }
                """
                is_detected = await page.evaluate(js_script, brand)
                if is_detected:
                    filename = f"mission_{mission.id}_{int(datetime.now().timestamp())}.png"
                    filepath = os.path.join(EVIDENCE_DIR, filename)
                    try:
                        await page.screenshot(path=filepath, full_page=True, timeout=20000)
                    except:
                        await page.screenshot(path=filepath, full_page=False)
                    mission.status = MissionStatus.DETECTED
                    mission.evidence_path = filename
                else:
                    mission.status = MissionStatus.CLEAN
            except Exception as e:
                mission.status = MissionStatus.ERROR
            finally:
                mission.processed_at = datetime.now()
                await self.db.commit()
                await browser.close()

async def run_crawler_task(mission_id: int):
    try:
        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            service = CrawlerService(db)
            await service.process_mission(mission_id)
    except:
        pass
