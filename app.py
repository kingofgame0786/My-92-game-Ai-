<!DOCTYPE html>
<html lang="ur">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>92Jeeto Game Assistant</title>
    <style>
        :root { --primary: #00f2fe; --accent: #e94560; --bg: #10101a; }
        body { font-family: sans-serif; background: transparent; margin: 0; padding: 10px; }
        
        /* Floating Container */
        .app-card { 
            background: rgba(16, 21, 30, 0.95); 
            border: 2px solid var(--primary);
            border-radius: 15px; 
            padding: 15px;
            box-shadow: 0 0 20px rgba(0,242,254,0.3);
            position: relative;
        }

        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; pb: 5px; mb: 10px; }
        h3 { color: var(--primary); margin: 0; font-size: 16px; }

        /* Prediction Highlight */
        .prediction-zone {
            background: #1a1a2e;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid var(--accent);
            margin-bottom: 15px;
        }
        .bet-now { font-size: 20px; font-weight: bold; color: #fff; text-transform: uppercase; }

        /* Quick Input Grid */
        .input-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px; }
        select, input, button { 
            background: #252a41; color: white; border: 1px solid #444; 
            padding: 8px; border-radius: 5px; font-size: 14px;
        }
        button { background: var(--accent); border: none; font-weight: bold; cursor: pointer; }

        /* History Dots */
        .history-dots { display: flex; gap: 5px; overflow-x: auto; padding: 5px 0; }
        .dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
        .red-dot { background: #ff4d4d; }
        .green-dot { background: #2ecc71; }
        .violet-dot { background: #9b59b6; }
    </style>
</head>
<body>

<div class="app-card" id="mainApp">
    <div class="header">
        <h3>92Jeeto Formula 🚀</h3>
        <span style="font-size: 10px; color: #aaa;">Status: Active</span>
    </div>

    <div class="prediction-zone" id="predBox">
        <div style="font-size: 12px; color: #00f2fe;">اگلی چال (Predicted):</div>
        <div class="bet-now" id="nextBet">WAIT...</div>
        <div id="logicReason" style="font-size: 10px; color: #f8f8f8; margin-top: 5px;">3 نتائج درج کریں</div>
    </div>

    <div class="input-grid">
        <input type="number" id="num" placeholder="No." min="0" max="9">
        <select id="size">
            <option value="Big">Big</option>
            <option value="Small">Small</option>
        </select>
        <select id="color">
            <option value="Red">Red</option>
            <option value="Green">Green</option>
            <option value="Violet">Violet</option>
        </select>
    </div>
    <button style="width: 100%;" onclick="processData()">اگلا رزلٹ شامل کریں</button>

    <div style="margin-top: 10px; font-size: 11px;">تاریخچہ (Recent):</div>
    <div class="history-dots" id="dotList">
        <!-- Dots will appear here -->
    </div>
</div>

<script>
    let history = [];

    function processData() {
        const n = document.getElementById('num').value;
        const s = document.getElementById('size').value;
        const c = document.getElementById('color').value;

        if(n==="") return alert("نمبر لکھیں");

        // Add to history
        history.unshift({ n: parseInt(n), s: s, c: c });
        if(history.length > 20) history.pop();

        updateUI();
        run92Formula();
        document.getElementById('num').value = "";
    }

    function updateUI() {
        const list = document.getElementById('dotList');
        list.innerHTML = history.map(h => `
            <div class="dot ${h.c === 'Red' ? 'red-dot' : h.c === 'Green' ? 'green-dot' : 'violet-dot'}" 
                 title="${h.s} ${h.n}"></div>
        `).join('');
    }

    function run92Formula() {
        if(history.length < 3) return;

        const last = history[0];
        const sizes = history.map(x => x.s);
        const colors = history.map(x => x.c);
        
        let pSize = "";
        let pColor = "";
        let reason = "";

        // 1. Dragon Check
        let dCount = 1;
        for(let i=0; i<sizes.length-1; i++) {
            if(sizes[i] === sizes[i+1]) dCount++; else break;
        }

        if(dCount >= 4) {
            pSize = last.s;
            reason = `ڈریگن ٹرینڈ (${dCount} بار ${last.s})`;
        } 
        // 2. Jump Check
        else if (sizes[0] !== sizes[1] && sizes[1] !== sizes[2]) {
            pSize = last.s === "Big" ? "Small" : "Big";
            reason = "جمپ پیٹرن (B-S-B-S) جاری ہے";
        }
        else {
            pSize = last.s;
            reason = "ٹرینڈ فالو کریں";
        }

        // Color Logic
        let cCount = 1;
        for(let i=0; i<colors.length-1; i++) {
            if(colors[i] === colors[i+1]) cCount++; else break;
        }
        pColor = (cCount >= 4) ? (last.c === "Red" ? "Green" : "Red") : last.c;

        document.getElementById('nextBet').innerText = `${pSize} + ${pColor}`;
        document.getElementById('logicReason').innerText = reason;
        
        // Violet Alert
        if(last.n === 0 || last.n === 5) {
            document.getElementById('logicReason').innerText += " | ⚠️ وائلٹ: خطرہ!";
        }
    }
</script>
</body>
</html>
