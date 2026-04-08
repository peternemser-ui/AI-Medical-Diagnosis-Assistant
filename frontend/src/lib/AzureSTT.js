import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk";

/**
 * Start continuous Azure speech recognition.
 * @param {Function} onFinal - Callback for final recognized text
 * @param {Function} onInterim - Callback for interim/partial text
 * @param {string} [language='en-US'] - BCP-47 language code for recognition
 */
export function startAzureMicRecognition(onFinal, onInterim, language = 'en-US') {
  const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(
    import.meta.env.VITE_AZURE_SPEECH_KEY,
    import.meta.env.VITE_AZURE_SPEECH_REGION
  );
  speechConfig.speechRecognitionLanguage = language;

  const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
  const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);

  recognizer.recognizing = (s, e) => {
    if (onInterim) onInterim(e.result.text);
  };

  recognizer.recognized = (s, e) => {
    if (e.result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
      if (onFinal) onFinal(e.result.text);
    }
  };

  recognizer.startContinuousRecognitionAsync();

  return () => {
    recognizer.stopContinuousRecognitionAsync();
  };
}
