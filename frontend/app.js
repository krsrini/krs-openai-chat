const chatbox = document.getElementById("chatbox");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const clearBtn = document.getElementById("clear");
const logoutBtn = document.getElementById("logout");
const modelSelect = document.getElementById("model-select");
const thinking = document.getElementById("thinking");

function nowTimestamp() {
  const d = new Date();
  // Local time with seconds
  return d.toLocaleString();
}

function appendMessage({ who, text, html = null }) {
  const time = nowTimestamp();
  const wrapper = document.createElement("div");
  wrapper.className = `msg ${who}`;
  wrapper.innerHTML = `
    <div class="meta"><span class="who">${who === "user" ? "You" : "AI"}</span> · <span class="time">${time}</span></div>
    <div class="content">${html || escapeHtml(text)}</div>
  `;
  chatbox.appendChild(wrapper);
  chatbox.scrollTop = chatbox.scrollHeight;
  enhanceCodeBlocks();
  saveChat();
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// Syntax highlight + copy buttons
function enhanceCodeBlocks() {
  chatbox.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
    if (!block.parentNode.querySelector(".copy-btn")) {
      const button = document.createElement("button");
      button.textContent = "Copy";
      button.className = "copy-btn";
      button.onclick = () => {
        navigator.clipboard.writeText(block.innerText).then(() => {
          button.textContent = "Copied!";
          button.classList.add("copied");
          setTimeout(() => {
            button.textContent = "Copy";
            button.classList.remove("copied");
          }, 1500);
        });
      };
      block.parentNode.appendChild(button);
    }
  });
}

function storageKey() {
  // Per-user chat history
  const u = window.localStorage.getItem("krs_user") || "anonymous";
  return `krs_chat_${u}`;
}

function saveChat() {
  window.localStorage.setItem(storageKey(), chatbox.innerHTML);
}

function loadChat() {
  const saved = window.localStorage.getItem(storageKey());
  if (saved) {
    chatbox.innerHTML = saved;
    enhanceCodeBlocks();
  }
}

async function getMe() {
  const r = await fetch("/api/me", { credentials: "include" });
  return r.json();
}

async function postJSON(url, data) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data || {})
  });
  return r.json();
}

async function sendMessage() {
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage({ who: "user", text: userMessage });

  input.value = "";
  const model = modelSelect.value;

  // show thinking
  thinking.style.display = "block";

  try {
    const data = await postJSON("/api/chat", { message: userMessage, model });
    const assistantMessage = data.reply || `Error: ${data.error || "No response"}`;
    const html = marked.parse(assistantMessage);
    appendMessage({ who: "ai", text: assistantMessage, html });
  } catch (e) {
    appendMessage({ who: "ai", text: `Error: ${e.message}` });
  } finally {
    thinking.style.display = "none";
  }
}

async function main() {
  const me = await getMe();
  if (!me.username) {
    window.location.href = "/";
    return;
  }
  window.localStorage.setItem("krs_user", me.username);
  loadChat();

  sendBtn.onclick = sendMessage;
  input.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });
  clearBtn.onclick = () => {
    chatbox.innerHTML = "";
    saveChat();
  };
  logoutBtn.onclick = async () => {
    await postJSON("/api/logout");
    window.location.href = "/";
  };
}

window.addEventListener("DOMContentLoaded", main);
