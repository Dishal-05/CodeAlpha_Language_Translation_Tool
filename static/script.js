/* ============================================================
   script.js – Language Translator Front-End Logic
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  // ── DOM References ──────────────────────────────────────────
  const inputText    = document.getElementById("input-text");
  const outputText   = document.getElementById("output-text");
  const sourceLang   = document.getElementById("source-lang");
  const targetLang   = document.getElementById("target-lang");
  const translateBtn = document.getElementById("translate-btn");
  const swapBtn      = document.getElementById("swap-btn");
  const copyBtn      = document.getElementById("copy-btn");
  const clearBtn     = document.getElementById("clear-btn");
  const messageBar   = document.getElementById("message-bar");
  const loadingDiv   = document.getElementById("loading");
  const charCountEl  = document.getElementById("char-count");
  const serviceBadge = document.getElementById("service-badge");

  // ── UI Helper Functions ─────────────────────────────────────

  function showMessage(text, type = "error") {
    messageBar.textContent = text;
    messageBar.className = `message-bar ${type}`;
  }

  function hideMessage() {
    messageBar.className = "message-bar hidden";
  }

  function setLoading(isLoading) {
    if (isLoading) {
      loadingDiv.classList.remove("hidden");
      translateBtn.disabled = true;
      translateBtn.textContent = "Translating…";
      serviceBadge.classList.add("hidden");
    } else {
      loadingDiv.classList.add("hidden");
      translateBtn.disabled = false;
      translateBtn.textContent = "🔤 Translate";
    }
  }

  // ── 1. Translate Action ─────────────────────────────────────
  async function handleTranslate() {
    const text = inputText.value.trim();
    const source = sourceLang.value;
    const target = targetLang.value;

    hideMessage();

    // Client-side validation
    if (!text) {
      showMessage("⚠️ Please enter some text to translate.", "error");
      inputText.focus();
      return;
    }

    if (source === target && source !== "auto") {
      showMessage("⚠️ Source and target languages cannot be the same.", "error");
      return;
    }

    setLoading(true);
    outputText.value = "";
    copyBtn.disabled = true;

    try {
      const response = await fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          source_lang: source,
          target_lang: target
        })
      });

      const data = await response.json();

      if (response.ok && data.translated_text) {
        outputText.value = data.translated_text;
        copyBtn.disabled = false;
        hideMessage();

        // Display AI provider badge
        if (data.service) {
          serviceBadge.textContent = `Powered by ${data.service}`;
          serviceBadge.classList.remove("hidden");
        }
      } else {
        const errorText = data.error || "Translation request failed. Please try again.";
        showMessage(`❌ ${errorText}`, "error");
      }
    } catch (err) {
      showMessage("❌ Could not connect to translation server. Please ensure the Flask app is running.", "error");
      console.error("Translation request error:", err);
    } finally {
      setLoading(false);
    }
  }

  translateBtn.addEventListener("click", handleTranslate);

  // ── 2. Swap Languages ───────────────────────────────────────
  swapBtn.addEventListener("click", () => {
    hideMessage();

    // If source is "auto", swapping to target is not allowed
    if (sourceLang.value === "auto") {
      showMessage("⚠️ Please select a specific source language before swapping.", "error");
      return;
    }

    // Swap dropdown selections
    const prevSource = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = prevSource;

    // Swap textarea text
    const prevInputText = inputText.value;
    inputText.value = outputText.value;
    outputText.value = prevInputText;

    // Update counter and button states
    charCountEl.textContent = inputText.value.length;
    copyBtn.disabled = outputText.value.trim() === "";
    serviceBadge.classList.add("hidden");

    // Spin animation
    swapBtn.classList.add("spinning");
    swapBtn.addEventListener("animationend", () => {
      swapBtn.classList.remove("spinning");
    }, { once: true });
  });

  // ── 3. Copy Translation ─────────────────────────────────────
  copyBtn.addEventListener("click", async () => {
    const textToCopy = outputText.value.trim();
    if (!textToCopy) return;

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(textToCopy);
      } else {
        // Fallback for older browsers
        outputText.select();
        document.execCommand("copy");
      }

      showMessage("✅ Translation copied to clipboard!", "success");
      setTimeout(hideMessage, 2500);
    } catch (err) {
      console.error("Copy failed:", err);
      showMessage("❌ Failed to copy to clipboard.", "error");
    }
  });

  // ── 4. Clear Reset ──────────────────────────────────────────
  clearBtn.addEventListener("click", () => {
    inputText.value = "";
    outputText.value = "";
    charCountEl.textContent = "0";
    copyBtn.disabled = true;
    serviceBadge.classList.add("hidden");
    hideMessage();
    inputText.focus();
  });

  // ── 5. Live Character Counter ───────────────────────────────
  inputText.addEventListener("input", () => {
    charCountEl.textContent = inputText.value.length;
  });

  // ── 6. Keyboard Shortcut (Ctrl+Enter or Cmd+Enter) ──────────
  inputText.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleTranslate();
    }
  });
});
