
from flask import Flask, jsonify, request
from flask import send_from_directory
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.route("/api/encrypt-demo", methods=["POST"])
def encrypt_demo():
    data = request.get_json(silent=True) or {}
    candidate = data.get("candidate", "")

    if candidate not in {
        "Candidate A", "Candidate B", "Candidate C"
    }:
        return jsonify({"error": "Choose a valid demo candidate."}), 400

    # Generate a temporary 256-bit AES key
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)

    # Encrypt the selected demo text
    nonce = os.urandom(12)
    plaintext = candidate.encode("utf-8")
    ciphertext = aes.encrypt(nonce, plaintext, None)

    # Decrypt it to demonstrate recovery
    decrypted = aes.decrypt(
        nonce, ciphertext, None
    ).decode("utf-8")

    # Change one ciphertext byte to test tamper detection
    modified = bytearray(ciphertext)
    modified[0] ^= 1

    try:
        aes.decrypt(nonce, bytes(modified), None)
        tamper_result = "Unexpected success"
    except Exception:
        tamper_result = "Tampering detected: decryption rejected"

    return jsonify({
        "algorithm": "AES-256-GCM",
        "original_text": candidate,
        "ciphertext_base64": base64.b64encode(
            ciphertext
        ).decode("utf-8"),
        "decrypted_text": decrypted,
        "tamper_test": tamper_result,
        "demo_only": True,
        "note": "This is an encryption demonstration, not a recorded vote."
    })


if __name__ == "__main__":
    app.run(debug=True)
