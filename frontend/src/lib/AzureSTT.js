import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk";

export function startAzureMicRecognition(onFinal, onInterim) {
  const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(
    import.meta.env.VITE_AZURE_SPEECH_KEY,
    import.meta.env.VITE_AZURE_SPEECH_REGION
  );
  speechConfig.speechRecognitionLanguage = "en-US";

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
