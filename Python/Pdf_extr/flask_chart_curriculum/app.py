from quart import Quart, send_file
import asyncio
from cassandra.cluster import Cluster
from chart_generator import generate_work_skills_chart, generate_language_skills_chart

app = Quart(__name__)

async def get_skills_data():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('cv_skills')
    
    # Recupera work_skills
    work_skills = []
    future = session.execute_async("SELECT work_skills FROM candidates_skills")
    rows = future.result()  
    for row in rows:
        work_skills.extend(row.work_skills)

    # Recupera language_skills
    language_skills = []
    future = session.execute_async("SELECT language_skills FROM candidates_skills")
    rows = future.result()  
    for row in rows:
        language_skills.extend(row.language_skills)

    cluster.shutdown()
    return work_skills, language_skills

@app.route('/plot/work_skills')
async def plot_work_skills():
    work_skills, _ = await get_skills_data()
    img_buffer = generate_work_skills_chart(work_skills)
    img_buffer.seek(0)
    response = await send_file(img_buffer, mimetype='image/webp')
    response.headers['Cache-Control'] = 'no-store, no-cache'
    return response

@app.route('/plot/language_skills')
async def plot_language_skills():
    _, language_skills = await get_skills_data()
    img_buffer = generate_language_skills_chart(language_skills)
    img_buffer.seek(0)
    response = await send_file(img_buffer, mimetype='image/webp')
    response.headers['Cache-Control'] = 'no-store, no-cache'
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
