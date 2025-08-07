from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from blockchain import Blockchain
from transaction import Transaction

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 創建全局區塊鏈實例
blockchain = Blockchain(difficulty=2, mining_reward=100.0)

@app.route('/')
def index():
    """
    API 首頁
    """
    return jsonify({
        "message": "歡迎使用私有區塊鏈 API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API 資訊",
            "GET /blockchain": "獲取完整區塊鏈",
            "GET /blockchain/validate": "驗證區塊鏈",
            "GET /balance/<address>": "獲取地址餘額",
            "GET /transactions/<address>": "獲取地址交易歷史",
            "POST /transaction": "創建新交易",
            "POST /mine": "挖掘待處理交易",
            "GET /pending": "獲取待處理交易"
        }
    })

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """
    獲取完整的區塊鏈
    """
    return jsonify({
        "blockchain": blockchain.to_dict(),
        "length": len(blockchain.chain),
        "valid": blockchain.is_chain_valid()
    })

@app.route('/blockchain/validate', methods=['GET'])
def validate_blockchain():
    """
    驗證區塊鏈是否有效
    """
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        "valid": is_valid,
        "message": "區塊鏈有效" if is_valid else "區塊鏈無效"
    })

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """
    獲取指定地址的餘額
    """
    balance = blockchain.get_balance(address)
    return jsonify({
        "address": address,
        "balance": balance
    })

@app.route('/transactions/<address>', methods=['GET'])
def get_transactions(address):
    """
    獲取指定地址的交易歷史
    """
    transactions = blockchain.get_transaction_history(address)
    return jsonify({
        "address": address,
        "transactions": transactions,
        "count": len(transactions)
    })

@app.route('/transaction', methods=['POST'])
def create_transaction():
    """
    創建新交易
    """
    try:
        data = request.get_json()
        
        # 驗證必要字段
        required_fields = ['from_address', 'to_address', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "message": f"缺少必要字段: {field}"
                }), 400
        
        # 創建交易
        transaction = Transaction(
            from_address=data['from_address'],
            to_address=data['to_address'],
            amount=float(data['amount'])
        )
        
        # 添加交易到區塊鏈
        success = blockchain.add_transaction(transaction)
        
        if success:
            return jsonify({
                "success": True,
                "message": "交易已成功添加到待處理列表",
                "transaction": transaction.to_dict()
            })
        else:
            return jsonify({
                "success": False,
                "message": "交易添加失敗"
            }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"錯誤: {str(e)}"
        }), 500

@app.route('/mine', methods=['POST'])
def mine_block():
    """
    挖掘待處理的交易
    """
    try:
        data = request.get_json()
        mining_reward_address = data.get('mining_reward_address', 'miner_default')
        
        success = blockchain.mine_pending_transactions(mining_reward_address)
        
        if success:
            latest_block = blockchain.get_latest_block()
            return jsonify({
                "success": True,
                "message": "區塊挖掘成功",
                "block": latest_block.to_dict()
            })
        else:
            return jsonify({
                "success": False,
                "message": "沒有待處理的交易可挖掘"
            }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"挖掘錯誤: {str(e)}"
        }), 500

@app.route('/pending', methods=['GET'])
def get_pending_transactions():
    """
    獲取待處理的交易
    """
    pending = [tx.to_dict() for tx in blockchain.pending_transactions]
    return jsonify({
        "pending_transactions": pending,
        "count": len(pending)
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """
    獲取區塊鏈統計信息
    """
    total_transactions = sum(len(block.transactions) for block in blockchain.chain)
    return jsonify({
        "total_blocks": len(blockchain.chain),
        "total_transactions": total_transactions,
        "pending_transactions": len(blockchain.pending_transactions),
        "difficulty": blockchain.difficulty,
        "mining_reward": blockchain.mining_reward,
        "is_valid": blockchain.is_chain_valid()
    })

@app.route('/save', methods=['POST'])
def save_blockchain():
    """
    保存區塊鏈到文件
    """
    try:
        data = request.get_json()
        filename = data.get('filename', 'blockchain.json')
        
        blockchain.save_to_file(filename)
        
        return jsonify({
            "success": True,
            "message": f"區塊鏈已保存到 {filename}"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"保存錯誤: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("啟動私有區塊鏈 API 服務器...")
    print("API 文檔: http://localhost:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)