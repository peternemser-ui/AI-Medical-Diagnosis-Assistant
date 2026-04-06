# Mobile App Publishing Guide

## Prerequisites
- Node.js 18+
- Capacitor CLI: `npm install -g @capacitor/cli`
- Android Studio (for Android)
- Xcode (for iOS, macOS only)

## Setup
```bash
cd frontend
npm install @capacitor/core @capacitor/cli
npx cap init "MedDiagnose AI" "ai.meddiagnose.app" --web-dir dist
npx cap add android
npx cap add ios
```

## Build & Deploy
```bash
# Build web app
npm run build

# Sync to native projects
npx cap sync

# Open in IDE
npx cap open android  # Opens Android Studio
npx cap open ios      # Opens Xcode
```

## App Store Submission
- Android: Build signed APK/AAB from Android Studio
- iOS: Archive and upload from Xcode

## Key Features for Mobile
- Camera access for photo analysis (already implemented)
- Push notifications for diagnosis results
- Offline mode via service worker (already implemented)
- Haptic feedback on interactions
