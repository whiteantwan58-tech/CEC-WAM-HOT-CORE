# 🔐 Biometric Authentication Guide

## Overview

The CEC-WAM-HOT-CORE dashboard now features **real biometric authentication** using the WebAuthn API. This provides secure access using your device's built-in biometric sensors:

- 🖐️ **Fingerprint sensors** (laptop/desktop)
- 📱 **Face ID** (iPhone/iPad)
- 🔑 **Touch ID** (Mac)
- 🪟 **Windows Hello** (Windows devices)

## Features

- ✅ Industry-standard WebAuthn API
- ✅ Works with built-in device biometrics
- ✅ Secure credential storage (browser-managed)
- ✅ No passwords required
- ✅ Cross-device support
- ✅ Privacy-focused (biometric data never leaves your device)

## Setup Instructions

### First Time Setup

1. **Open the dashboard** in a modern browser (Chrome, Firefox, Safari, or Edge)
2. The lock screen will appear with "No biometric registered" message
3. Click **"REGISTER BIOMETRIC"** button
4. Your browser will prompt you to use your biometric sensor:
   - **Laptop/Desktop**: Touch your fingerprint sensor
   - **iPhone/iPad**: Use Face ID or Touch ID
   - **Mac**: Use Touch ID
   - **Windows**: Use Windows Hello (fingerprint or face)
5. Complete the biometric verification
6. Success! Your biometric is now registered

### Daily Use

1. Open the dashboard
2. The system will detect your registered biometric
3. Click **"AUTHENTICATE"** button (or wait 2 seconds for auto-authentication)
4. Use your biometric sensor to verify your identity
5. Access granted!

## Supported Devices & Browsers

### ✅ Fully Supported

| Device Type | Biometric Method | Browser Support |
|-------------|------------------|-----------------|
| iPhone/iPad | Face ID / Touch ID | Safari, Chrome, Firefox, Edge |
| Mac | Touch ID | Safari, Chrome, Firefox, Edge |
| Windows PC | Windows Hello | Chrome, Firefox, Edge |
| Android | Fingerprint | Chrome, Firefox, Edge |
| Laptop | Fingerprint Reader | Chrome, Firefox, Edge |

### ⚠️ Requirements

- Modern browser (released in last 2 years)
- Device with biometric hardware
- HTTPS connection (required for WebAuthn)
- JavaScript enabled

## Security Features

### How It Works

1. **Registration Phase**:
   - Browser creates a public/private key pair
   - Private key stored securely in device's secure enclave or platform authenticator
   - Public key managed by the browser's credential manager (not stored in localStorage)
   - A non-sensitive credential ID reference is stored in browser's localStorage (no cryptographic key material)
   - Your biometric data **never** leaves your device

2. **Authentication Phase**:
   - Browser presents a challenge
   - You verify with biometric sensor
   - Device signs challenge with private key
   - Browser verifies signature
   - Access granted if valid

### Security Benefits

- 🔒 **No passwords to remember or steal**
- 🔒 **Biometric data stays on your device**
- 🔒 **Phishing-resistant authentication**
- 🔒 **Hardware-backed security**
- 🔒 **Can't be shared or transferred**

## Console Commands

Access the EVE terminal and use these commands:

### Check Biometric Status
```
biometric
```
Shows:
- Registration status
- Credential ID (partial)
- Registration date
- Last authentication time

### Reset Biometric Credentials
```
biometric reset
```
Clears stored credentials. Reload page to register again.

## Troubleshooting

### "WebAuthn is not supported"
- **Solution**: Update your browser to the latest version
- **Alternative**: Use Chrome, Firefox, Safari, or Edge

### "No biometric hardware detected"
- **Solution**: Ensure your device has a fingerprint sensor or Face ID
- **Check**: Device settings to enable biometric features

### "Authentication failed"
- **Cause**: Sensor couldn't read biometric or wrong finger/face
- **Solution**: Try again with the registered biometric
- **Tip**: Clean your fingerprint sensor or ensure good lighting for Face ID

### "Registration failed"
- **Check**: Browser permissions for WebAuthn
- **Try**: Reload page and try again
- **Ensure**: Biometric is enrolled in device settings first

### Biometric Not Working
1. Verify biometric is set up in device settings
2. Test biometric with device unlock (phone lock, laptop login)
3. Clear credentials with `biometric reset` command
4. Reload page and register again

## Privacy & Data

### What Gets Stored

**In Browser (localStorage)**:
- Credential ID (public identifier)
- Registration timestamp
- Last authentication timestamp

**NOT Stored**:
- ❌ Your biometric data (fingerprint, face scan)
- ❌ Private cryptographic keys
- ❌ Personal information
- ❌ Authentication history beyond last login

### Data Location

- **Biometric Data**: Stays in device's secure hardware enclave
- **Private Keys**: Stored in browser's secure key storage
- **Public Data**: localStorage (credential ID only)

### Clearing Data

To completely remove biometric authentication:
1. Open EVE terminal
2. Type `biometric reset`
3. Or clear browser's localStorage for this site

## Technical Details

### WebAuthn Specification

- **Standard**: W3C Web Authentication API
- **Credential Type**: Platform authenticator (built-in)
- **Algorithms**: ES256 (ECDSA), RS256 (RSA)
- **User Verification**: Required
- **Attestation**: None (privacy-focused)

### Implementation

```javascript
// Registration uses PublicKeyCredential.create()
// Authentication uses PublicKeyCredential.get()
// Credentials stored locally in browser
// Relying Party: window.location.hostname
```

## Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 67+ | ✅ Full |
| Firefox | 60+ | ✅ Full |
| Safari | 13+ | ✅ Full |
| Edge | 18+ | ✅ Full |
| Opera | 54+ | ✅ Full |

## FAQ

**Q: Can I use this on multiple devices?**
A: Yes, but you need to register biometric on each device separately. Credentials are device-specific.

**Q: What if I lose access to my biometric?**
A: Use the `biometric reset` command to clear credentials and set up a new biometric.

**Q: Is this more secure than passwords?**
A: Yes! Biometric authentication is phishing-resistant and tied to your physical presence.

**Q: Can someone copy my biometric to access the dashboard?**
A: No. Your biometric data never leaves your device, and the private key is hardware-protected.

**Q: Does this work offline?**
A: Yes! Authentication happens locally on your device.

**Q: Will this work on my Chromebook?**
A: Yes, if your Chromebook has a fingerprint sensor or supports Android biometrics.

## Support

For issues or questions:
- Check this guide's Troubleshooting section
- Review browser console for detailed error messages
- Ensure device biometrics are working (test with device unlock)
- Try the `biometric reset` command and register again

---

**Built with ❤️ for the CEC-WAM Team**

🌌 *Secure access through the power of biometric technology* 🌌
