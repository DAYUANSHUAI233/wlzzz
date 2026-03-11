#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json
import gzip
from io import BytesIO
from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

# 字段说明（仅用于原板块数据，新接口不强制使用）
FIELD_DESC = {
    "c": "代码",
    "n": "名称",
    "s": "热度",
    "p": "涨跌幅(%)",
    "pr": "价格",
    "t": "主力类型",
    "cn": "概念",
    "v": "成交量(元)",
    "sp": "涨速"
}

# 接口基础URL
PLATE_API = "https://apphq.longhuvip.com/w1/api/index.php"
STOCK_API = "https://apphwshhq.longhuvip.com/w1/api/index.php"

# 原有请求头
HEADERS_PLATE = {
    'Host': 'apphq.longhuvip.com',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; Redmi 9 Build/RP1A.200720.011)',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Encoding': 'identity',
    'Accept-Language': 'zh-cn',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1'
}

HEADERS_STOCK = {
    'Host': 'apphwshhq.longhuvip.com',
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ADA-AL00 Build/PQ3A.190705.001)',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-cn',
    'Cache-Control': 'no-cache'
}

# ---------- 新增接口请求头 ----------
HEADERS_WOGOO = {
    'X-White-List': 'wogoo',
    'Authorization': '',
    'Accept': '*/*',
    'X-System-Version': '16.7.10',
    'X-Device-NO': 'CE6DDC52-954A-4E71-9201-7A09C8DDA4D3',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'Accept-Language': 'zh-Hans-CN;q=1.0',
    'Content-Type': 'application/json',
    'X-Tracking-ID': '1a3b7c34c7e4aebfb2db837a5edc484a',
    'X-Device-Token': 'Tk9SSUQuMSNzaDExZTNhYTU1aHMxNTlhNjc5Y2FmZWUxYjZmZmUxNS1oLTE3Mjg2NjQzODUzOTEtNGQzZTNmMDA3YWM5NDkxOTk3OTdkMzc1NGU3MTc5ODAjRmcrK0J3NC9xTFM1ZlJvMTVnc2oraDgza2VzQjIza1Vrb2pCdDdrSHNRYVlwSFNTQlBaMmRTeGR5dG9wbHJwRGVya0toazlkKzd4TXFLUUhETVpuM3JhUU5zdCt5N1A3R0tMY1B4ZldIMFh0VDVhdzVNYkQ0bGVONC9zbnJUY0VjeFV2Q25zZWRDbTYzMkk4OGNkTFpMbEZCVnJ5QVNSS0g2M0RzV1FZVEQrRC93T0crZERUUWFUb0IzbjB4b25Rait3QnVWdS9qWldyYnVLTisxS2hKcmV4SGxhNjBDb3hxVDkwUDVRd2hyZmdhSjh5dCtkTnJVZjJxS1VnTFkvOHMzODg4b012dXlYUjFlZ2x1dHdYYjlnZjBnZ2REaVc2Qnc4ODMxT1NqSDlEMFlrbGlDOVNmK05mSnd0OEJjUGFvczVRSkMyZ0twTkx4RTIvRDkyVFpCM0hyaEVGZVVWenR2TlVFSGJPTldMbEI3OUNwZzc4R1pwSGN1Wi92T21WTWxyQyMxNw==',
    'X-System-Type': '2',
    'X-App-Version': '6.12.0',
    'User-Agent': '',
    'Connection': 'keep-alive',
    'X-Device-Type': 'iPad6,11'
}

# ---------- 为 longhuvip 接口添加的请求头 ----------
HEADERS_LONGHU = {
    'Host': 'apphq.longhuvip.com',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; Redmi 9 Build/RP1A.200720.011)',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn',
    'Cache-Control': 'no-cache'
}

# ---------- 原有函数（保持不变）----------
def get_plate_rank():
    """获取实时板块排名"""
    params = {
        'Order': 1,
        'a': 'RealRankingInfo',
        'st': 20,
        'apiv': 'w21',
        'Type': 1,
        'c': 'ZhiShuRanking',
        'PhoneOSNew': 1,
        'ZSType': 7
    }
    
    url = f"{PLATE_API}?{urllib.parse.urlencode(params)}"
    
    try:
        resp = requests.get(url, headers=HEADERS_PLATE, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('errcode') != '0' and data.get('errcode') != 0:
            return {'error': data.get('errmsg', '未知错误')}
        
        plates = []
        for item in data.get('list', []):
            plates.append({
                'c': item[0],
                'n': item[1],
                's': item[2],
                'p': item[3],
                'sp': item[4] if len(item) > 4 else 0,
            })
        return plates
    except Exception as e:
        return {'error': str(e)}

def get_stock_list(plate_id):
    """获取板块内全部股票"""
    post_data = {
        'Order': 1,
        'TSZB': 0,
        'a': 'ZhiShuStockList_W8',
        'st': 60,
        'c': 'ZhiShuRanking',
        'PhoneOSNew': 1,
        'RStart': '0925',
        'old': 1,
        'DeviceID': '5520d2b6-c643-35e1-af95-3b5d19cf52a6',
        'VerSion': '5.22.0.6',
        'IsZZ': 0,
        'Token': '454f66058f1b5f3e105aeebf0001420f',
        'Index': 0,
        'REnd': '1500',
        'apiv': 'w43',
        'Type': -4,
        'IsKZZType': 0,
        'UserID': 6907021,
        'PlateID': plate_id,
        'TSZB_Type': 0,
        'filterType': 0
    }
    
    encoded_data = urllib.parse.urlencode(post_data)
    
    try:
        resp = requests.post(
            STOCK_API,
            data=encoded_data,
            headers=HEADERS_STOCK,
            timeout=15
        )
        resp.raise_for_status()
        
        content = resp.content
        try:
            buf = BytesIO(content)
            with gzip.GzipFile(fileobj=buf) as f:
                content = f.read()
        except:
            pass
        
        data = json.loads(content.decode('utf-8', errors='ignore'))
        
        if data.get('errcode') != '0' and data.get('errcode') != 0:
            return {'error': data.get('errmsg', '未知错误')}
        
        stocks = []
        for item in data.get('list', []):
            stocks.append({
                'c': item[0],
                'n': item[1],
                't': item[2],
                'p': item[6],
                'pr': item[5],
                'cn': item[4],
                'v': item[7],
            })
        return stocks
    except Exception as e:
        return {'error': str(e)}

# ---------- 新增接口函数（字段名改为中文，增加请求头）----------

def get_updown_stats():
    """1. 上涨下跌家数统计 (longhuvip)"""
    url = "https://apphq.longhuvip.com/w1/api/index.php?a=ZhangFuDetail&apiv=w21&c=HomeDingPan"
    try:
        resp = requests.get(url, headers=HEADERS_LONGHU, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # 检查返回码
        if data.get('errcode') not in (0, '0', None):
            print(f"[updown] API error: {data.get('errmsg')}")
            return {'上涨家数': 0, '下跌家数': 0, '总家数': 0, '上涨占比': 0, '下跌占比': 0}
        info = data.get('info', {})
        szjs = info.get('SZJS', 0)
        xdjs = info.get('XDJS', 0)
        total = szjs + xdjs
        up_percent = round(szjs / total * 100, 2) if total else 0
        down_percent = round(xdjs / total * 100, 2) if total else 0
        return {
            '上涨家数': szjs,
            '下跌家数': xdjs,
            '总家数': total,
            '上涨占比': up_percent,
            '下跌占比': down_percent
        }
    except Exception as e:
        print(f"[updown] exception: {str(e)}")
        return {'上涨家数': 0, '下跌家数': 0, '总家数': 0, '上涨占比': 0, '下跌占比': 0}

def get_retrace_stats():
    """2. 大幅回撤与综合强度 (longhuvip)"""
    url = "https://apphq.longhuvip.com/w1/api/index.php?a=ChangeStatistics&apiv=w31&c=HomeDingPan"
    try:
        resp = requests.get(url, headers=HEADERS_LONGHU, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get('errcode') not in (0, '0', None):
            print(f"[retrace] API error: {data.get('errmsg')}")
            return {'大幅回撤数量': 0, '综合强度': 0}
        info = data.get('info', [{}])[0]
        return {
            '大幅回撤数量': info.get('df_num', 0),
            '综合强度': info.get('strong', 0)
        }
    except Exception as e:
        print(f"[retrace] exception: {str(e)}")
        return {'大幅回撤数量': 0, '综合强度': 0}

def get_volume_stats():
    """3. 量能数据 (longhuvip)"""
    url = "https://apphq.longhuvip.com/w1/api/index.php?a=MarketCapacity&apiv=w31&Type=0&c=HomeDingPan"
    try:
        resp = requests.get(url, headers=HEADERS_LONGHU, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get('errcode') not in (0, '0', None):
            print(f"[volume] API error: {data.get('errmsg')}")
            return {'最后总量': '0', '昨日总量': '0', '预测量能': ''}
        info = data.get('info', {})
        return {
            '最后总量': info.get('last', '0'),
            '昨日总量': info.get('s_zrtj', '0'),
            '预测量能': info.get('yclnstr', '')
        }
    except Exception as e:
        print(f"[volume] exception: {str(e)}")
        return {'最后总量': '0', '昨日总量': '0', '预测量能': ''}

def get_market_mood():
    """4. 市场情绪核心数据 (huanshoulv)"""
    url = ("https://goserver.huanshoulv.com/aimapp/surgeLimit/marketMood?"
           "is_filter=1&date=20500120&page=1&page_count=1&open_uuid=ZNhp8mjS/JcDAKiLflcMYcw7"
           "&ts=1705732424532&device_id=ZNhp8mjS/JcDAKiLflcMYcw7&sdk_int=22&appversion=2.0.0.6"
           "&width=720&device_token=0fa9f8ebdeeca354e6deedad7308a16f4f51&has_dep=false&channel=hsl-app&div=ANDH020006")
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        info_list = data.get('data', {}).get('infoList', [])
        if not info_list:
            return {'error': '无数据'}
        item = info_list[0]
        # item顺序: [date,?,firstBoard,secondBoard,thirdBoard,thirdPlusBoard,boardCount,
        #           limitDown,limitUp,highestBoard,code,?,name,?,brokenBoard,oneWordBoard,naturalLimitUp]
        result = {
            '日期': item[0],
            '首板': item[2],
            '二板': item[3],
            '三板': item[4],
            '三板以上': item[5],
            '连板家数': item[6],
            '跌停': item[7],
            '涨停': item[8],
            '最高板': item[9],
            '炸板数量': item[15],
          
        }
        # 计算炸板率
        limit_up = result['涨停']
        broken = result['炸板数量']
        result['炸板率'] = round(broken / (limit_up + broken) * 100, 2) if (limit_up + broken) else 0
        return result
    except Exception as e:
        return {'error': str(e)}

def get_loss_stats(market_date):
    """5. 大跌与回撤统计 (wogoo) - 需要日期 YYYYMMDD"""
    url = "https://user-stock.wogoo.com/board/market/loss"
    payload = {"marketDate": market_date}
    try:
        resp = requests.post(url, headers=HEADERS_WOGOO, json=payload, timeout=15)
        data = resp.json()
        if data.get('success'):
            loss = data['data']['lossItems']
            draw_back = data['data']['drawBackItems']
            pre_loss = data['data']['preLossItems']
            pre_draw_back = data['data']['preDrawBackItems']
            return {
                '主线大跌总数': len(loss),
                '主线大跌修复': sum(1 for x in loss if x.get('tag') == 1),
                '大幅回撤总数': len(draw_back),
                '大幅回撤修复': sum(1 for x in draw_back if x.get('tag') == 1),
                '昨日主线大跌总数': len(pre_loss),
                '昨日主线大跌修复': sum(1 for x in pre_loss if x.get('tag') == 1),
                '昨日大幅回撤总数': len(pre_draw_back),
                '昨日大幅回撤修复': sum(1 for x in pre_draw_back if x.get('tag') == 1),
            }
        else:
            return {'error': data.get('desc', '未知错误')}
    except Exception as e:
        return {'error': str(e)}

def get_fund_trend(market_date):
    """6. 资金趋势数据 (wogoo) - 需要日期 YYYYMMDD"""
    url = "https://user-stock.wogoo.com/board/market/mood"
    payload = {"needType": 0, "marketDate": market_date}
    try:
        resp = requests.post(url, headers=HEADERS_WOGOO, json=payload, timeout=15)
        data = resp.json()
        if data.get('success'):
            fund_stats = data['data']['fundStats']
            if not fund_stats:
                return {'error': '无资金数据'}
            last = fund_stats[-1]  # 取最后一个时间点
            today = last['fundStats']
            yesterday = last['preFundStats']
            def to_billion(val, dec):
                # 转换为亿元
                return round(val / (10 ** (dec + 8)), 2)
            return {
                '今日涨停排队资金(亿)': to_billion(today['lastQueueFund']['value'], today['lastQueueFund']['decimal']),
                '昨日涨停排队资金(亿)': to_billion(yesterday['lastQueueFund']['value'], yesterday['lastQueueFund']['decimal']),
                '今日涨停成交资金(亿)': to_billion(today['tradeFund']['value'], today['tradeFund']['decimal']),
                '昨日涨停成交资金(亿)': to_billion(yesterday['tradeFund']['value'], yesterday['tradeFund']['decimal']),
                '今日打板获利资金(亿)': to_billion(today['boardProfitFund']['value'], today['boardProfitFund']['decimal']),
                '昨日打板获利资金(亿)': to_billion(yesterday['boardProfitFund']['value'], yesterday['boardProfitFund']['decimal']),
            }
        else:
            return {'error': data.get('desc', '未知错误')}
    except Exception as e:
        return {'error': str(e)}

def get_default_trade_date():
    """7. 获取默认交易日 (zizizaizai)"""
    url = "http://api.zizizaizai.com/market/trade/days?days=1"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get('code') == 20000 and data.get('data'):
            return data['data'][0]  # 返回 'YYYY-MM-DD' 格式
        else:
            return datetime.now().strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

# ---------- 路由 ----------

def json_response(data):
    """返回JSON响应"""
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/')
def index():
    """返回所有数据（板块排名 + TOP3板块成分股）"""
    plates = get_plate_rank()
    if isinstance(plates, dict) and 'error' in plates:
        return json_response({
            't': datetime.now().strftime('%m-%d %H:%M'),
            'err': plates['error'],
            'desc': FIELD_DESC
        })
    
    # 获取TOP3板块的成分股
    for plate in plates[:3]:
        stocks = get_stock_list(plate['c'])
        if isinstance(stocks, dict) and 'error' in stocks:
            plate['st'] = []
        else:
            plate['st'] = stocks
    
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'desc': FIELD_DESC,
        'ps': plates
    })

@app.route('/plates')
def plates():
    """仅返回板块排名"""
    data = get_plate_rank()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'desc': FIELD_DESC,
        'ps': data
    })

@app.route('/stocks/<plate_id>')
def stocks(plate_id):
    """返回指定板块的成分股"""
    data = get_stock_list(plate_id)
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'pc': plate_id,
        'desc': FIELD_DESC,
        'st': data
    })

# ---------- 新增路由 ----------

@app.route('/market/updown')
def market_updown():
    """上涨下跌家数"""
    data = get_updown_stats()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'data': data
    })

@app.route('/market/retrace')
def market_retrace():
    """大幅回撤与综合强度"""
    data = get_retrace_stats()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'data': data
    })

@app.route('/market/volume')
def market_volume():
    """量能数据"""
    data = get_volume_stats()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'data': data
    })

@app.route('/market/mood')
def market_mood():
    """市场情绪核心"""
    data = get_market_mood()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'data': data
    })

@app.route('/market/loss/<market_date>')
def market_loss(market_date):
    """大跌与回撤统计 (日期格式: YYYYMMDD)"""
    data = get_loss_stats(int(market_date))
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'date': market_date,
        'data': data
    })

@app.route('/market/trend/<market_date>')
def market_trend(market_date):
    """资金趋势数据 (日期格式: YYYYMMDD)"""
    data = get_fund_trend(int(market_date))
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'date': market_date,
        'data': data
    })

@app.route('/market/days')
def market_days():
    """默认交易日"""
    date_str = get_default_trade_date()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'default_date': date_str
    })

@app.route('/all')
def all_data():
    """聚合所有市场情绪数据 + 题材前10名及成分股"""
    # 获取默认日期（用于需要日期的接口）
    default_date_str = get_default_trade_date()  # YYYY-MM-DD
    try:
        market_date_int = int(datetime.strptime(default_date_str, '%Y-%m-%d').strftime('%Y%m%d'))
    except:
        market_date_int = int(datetime.now().strftime('%Y%m%d'))

    # 获取题材前10名
    plates_data = get_plate_rank()
    top_themes = []
    if isinstance(plates_data, list):
        for plate in plates_data[:10]:  # 取前10
            # 获取该题材的成分股
            stocks = get_stock_list(plate['c'])
            stock_list = []
            if isinstance(stocks, list):
                for s in stocks:
                    stock_list.append({
                        '代码': s.get('c', ''),
                        '名称': s.get('n', ''),
                        '主力类型': s.get('t', ''),
                        '涨跌幅': s.get('p', 0),
                        '价格': s.get('pr', 0),
                        '概念': s.get('cn', ''),
                        '成交量': s.get('v', 0)
                    })
            # 构建题材信息（去掉代码字段）
            top_themes.append({
                '名称': plate.get('n', ''),
                '热度': plate.get('s', 0),
                '涨跌幅': plate.get('p', 0),
                '涨速': plate.get('sp', 0),
                '股票列表': stock_list
            })

    result = {
        'timestamp': datetime.now().isoformat(),
        'default_trade_date': default_date_str,
        'updown': get_updown_stats(),
        'retrace': get_retrace_stats(),
        'volume': get_volume_stats(),
        'mood': get_market_mood(),
        'loss': get_loss_stats(market_date_int),
        'fund_trend': get_fund_trend(market_date_int),
        'top_themes': top_themes   # 新增题材数据
    }
    return json_response(result)

if __name__ == "__main__":
    print("=" * 60)
    print("启动 Web 服务器...")
    print("=" * 60)
    print("")
    print("请打开浏览器访问:")
    print("  http://127.0.0.1:5000")
    print("  http://localhost:5000")
    print("")
    print("原接口:")
    print("  http://127.0.0.1:5000/plates       - 板块排名")
    print("  http://127.0.0.1:5000/stocks/<代码> - 成分股")
    print("")
    print("新增接口:")
    print("  http://127.0.0.1:5000/market/updown    - 上涨下跌家数")
    print("  http://127.0.0.1:5000/market/retrace   - 大幅回撤与强度")
    print("  http://127.0.0.1:5000/market/volume    - 量能数据")
    print("  http://127.0.0.1:5000/market/mood      - 市场情绪核心")
    print("  http://127.0.0.1:5000/market/loss/<日期> - 大跌回撤 (日期YYYYMMDD)")
    print("  http://127.0.0.1:5000/market/trend/<日期> - 资金趋势 (日期YYYYMMDD)")
    print("  http://127.0.0.1:5000/market/days      - 默认交易日")
    print("  http://127.0.0.1:5000/all              - 聚合所有数据（含题材前10名及成分股）")
    print("")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=False)