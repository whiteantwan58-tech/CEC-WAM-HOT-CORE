/**
 * encrypt.js — Local secret encryption utility (WebCrypto / AES-GCM)
 *
 * Provides helpers to encrypt and decrypt sensitive string values using the
 * browser's built-in WebCrypto API (no external dependencies).
 *
 * Algorithm: AES-GCM 256-bit
 *  - A fresh random key is derived from a passphrase + salt via PBKDF2.
 *  - A fresh random 12-byte IV is generated for every encrypt call.
 *  - The key is NEVER stored; the caller must supply the passphrase each time.
 *
 * ── Usage ───────────────────────────────────────────────────────────────────
 *
 *   // Encrypt:
 *   const { ciphertext, iv, salt } = await CecCrypto.encrypt('my-secret-value', 'my-passphrase');
 *   // Store ciphertext, iv, and salt (all base64 strings) – safe to persist locally.
 *
 *   // Decrypt:
 *   const plaintext = await CecCrypto.decrypt(ciphertext, iv, salt, 'my-passphrase');
 *
 * ── Security notes ──────────────────────────────────────────────────────────
 *  - NEVER commit actual secret values or passphrases to the repository.
 *  - NEVER commit the .env file (it is in .gitignore).
 *  - This utility is for *optional* local-at-rest protection of cached values
 *    in localStorage / IndexedDB, NOT a substitute for server-side secret stores.
 *  - Requires a secure context (HTTPS or localhost).
 *
 * ── WebCrypto availability ───────────────────────────────────────────────────
 *  - Available in all modern browsers (Chrome 37+, Firefox 34+, Safari 11+,
 *    Edge 12+) and Node.js ≥ 19 (globalThis.crypto.subtle).
 */

'use strict';

const CecCrypto = (() => {
  const ENC = new TextEncoder();
  const DEC = new TextDecoder();

  /** Convert an ArrayBuffer → base64 string. */
  function _bufToB64(buf) {
    return btoa(String.fromCharCode(...new Uint8Array(buf)));
  }

  /** Convert a base64 string → Uint8Array. */
  function _b64ToBuf(b64) {
    return Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  }

  /**
   * Derive an AES-GCM 256-bit CryptoKey from a passphrase + salt using PBKDF2.
   * @param {string} passphrase
   * @param {Uint8Array} salt
   * @returns {Promise<CryptoKey>}
   */
  async function _deriveKey(passphrase, salt) {
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      ENC.encode(passphrase),
      'PBKDF2',
      false,
      ['deriveKey']
    );
    return crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations: 600_000, hash: 'SHA-256' },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt']
    );
  }

  /**
   * Encrypt a plaintext string with a passphrase.
   * @param {string} plaintext   — value to protect
   * @param {string} passphrase  — user-supplied key material (NOT stored)
   * @returns {Promise<{ciphertext: string, iv: string, salt: string}>}
   *   All values are base64-encoded and safe to store in localStorage/IndexedDB.
   */
  async function encrypt(plaintext, passphrase) {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv   = crypto.getRandomValues(new Uint8Array(12));
    const key  = await _deriveKey(passphrase, salt);

    const cipherbuf = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      ENC.encode(plaintext)
    );

    return {
      ciphertext: _bufToB64(cipherbuf),
      iv:         _bufToB64(iv),
      salt:       _bufToB64(salt),
    };
  }

  /**
   * Decrypt a previously encrypted value.
   * @param {string} ciphertext  — base64 ciphertext from encrypt()
   * @param {string} iv          — base64 IV from encrypt()
   * @param {string} salt        — base64 salt from encrypt()
   * @param {string} passphrase  — same passphrase used during encrypt()
   * @returns {Promise<string>}  — original plaintext
   * @throws if the passphrase is wrong or the ciphertext is tampered with.
   */
  async function decrypt(ciphertext, iv, salt, passphrase) {
    const key = await _deriveKey(passphrase, _b64ToBuf(salt));

    const plainbuf = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: _b64ToBuf(iv) },
      key,
      _b64ToBuf(ciphertext)
    );

    return DEC.decode(plainbuf);
  }

  return { encrypt, decrypt };
})();

// Make available as an ES module export when bundled, and as a global otherwise.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CecCrypto;
}
