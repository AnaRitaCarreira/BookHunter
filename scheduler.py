from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.tracker import check_all_tracked_books
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler():
    # Agenda para rodar todos os dias às 6h da manhã
    scheduler.add_job(check_all_tracked_books, 'cron', hour=6)
    scheduler.start()
