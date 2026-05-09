function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }
        async function sendMessage() {
            var input = document.getElementById('user-input');
            var text = input.value;
            if(!text) return;
            addMsg(text, 'user'); 
            input.value = ''; 
            var res = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            var data = await res.json();   
            addMsg(data.reply, 'bot'); 
            addToHistory(text, data.reply); 
        }
        function addMsg(txt, type) {
            var div = document.createElement('div');
            div.className = 'msg ' + type;
            div.innerText = txt;
            document.getElementById('chat-box').appendChild(div);
            document.getElementById('chat-box').scrollTop = 9999;
            return div;
        }
        function addToHistory(q, a) {
            var container = document.getElementById('history-container');
            var div = document.createElement('div');
            div.className = 'hist-item';
            
            div.innerHTML = `
                <span onclick="restoreChat(this)">${q.substring(0,15)}...</span>
                <div>
                    <button class="btn-icon" onclick="downloadFile(this)">💾</button>
                    <button class="btn-icon" onclick="this.parentElement.parentElement.remove()">🗑️</button>
                </div>
            `;
            div.setAttribute('data-q', q);
            div.setAttribute('data-a', a);
            container.prepend(div);
        }
        function restoreChat(element) {
            var parent = element.parentElement; 
            var q = parent.getAttribute('data-q');
            var a = parent.getAttribute('data-a');
            document.getElementById('chat-box').innerHTML = ''; 
            addMsg(q, 'user');
            addMsg(a, 'bot');
            toggleSidebar(); 
        }
        function downloadFile(element) {
            var parent = element.parentElement.parentElement;
            var q = parent.getAttribute('data-q');
            var a = parent.getAttribute('data-a');
            var text = "QUESTION: " + q + "\n\nREPONSE: " + a;
            var link = document.createElement('a');
            link.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(text);
            link.download = "exercice.txt";
            link.click();
        }
        function clearChat() {
            document.getElementById('chat-box').innerHTML = '<div class="msg bot">Écran effacé !</div>';
        }