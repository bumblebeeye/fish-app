from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# 设置数据库路径（确保路径正确）
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'fish.db')

# ✅ API 1: 筛选鱼类列表
@app.route('/api/fish', methods=['GET'])
def filter_fish():
    water = request.args.get('water')  # 示例：?water=淡水
    size = request.args.get('size')    # 示例：?size=5

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = "SELECT id, 常见名, 学名, 水域类型, 成体体长_cm, 性情 FROM fish WHERE 1=1"
    params = []
    if water:
        query += " AND 水域类型 = ?"
        params.append(water)
    if size:
        query += " AND 成体体长_cm <= ?"
        params.append(float(size))
    cur.execute(query, params)
    rows = cur.fetchall()
    result = [dict(zip([col[0] for col in cur.description], row)) for row in rows]
    conn.close()
    return jsonify(result)

# ✅ API 2: 获取鱼类详情
@app.route('/api/fish/<int:fish_id>', methods=['GET'])
def fish_detail(fish_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM fish WHERE id=?", (fish_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    result = dict(zip([col[0] for col in cur.description], row))
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
