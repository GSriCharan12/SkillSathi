"use client";

import React, { useState, useEffect, useRef } from "react";
import { Mic, MicOff, Volume2, VolumeX, AlertCircle } from "lucide-react";

interface VoiceControllerProps {
  language: "en" | "te" | "hi";
  onTranscript: (text: string) => void;
  isListening: boolean;
  setIsListening: (val: boolean) => void;
}

export function VoiceController({
  language,
  onTranscript,
  isListening,
  setIsListening,
}: VoiceControllerProps) {
  const [isSpeechSupported, setIsSpeechSupported] = useState(true);
  const [speechError, setSpeechError] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if Web Speech API is supported
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSpeechSupported(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;

      // Set language locale strictly to English
      recognition.lang = "en-IN";


      recognition.onstart = () => {
        setIsListening(true);
        setSpeechError(null);
      };

      recognition.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        if (event.results[current].isFinal) {
          onTranscript(transcript);
          setIsListening(false);
        }
      };

      recognition.onerror = (event: any) => {
        console.warn("Speech recognition error:", event.error);
        if (event.error === "not-allowed") {
          setSpeechError("Microphone access denied. Please type your message.");
        } else if (event.error !== "no-speech") {
          setSpeechError(`Voice error (${event.error}). Please type.`);
        }
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } catch (err) {
      console.warn("Error initializing speech recognition:", err);
      setIsSpeechSupported(false);
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch (e) {}
      }
    };
  }, [language, onTranscript, setIsListening]);

  const toggleListening = () => {
    if (!isSpeechSupported) {
      alert("Voice input is not supported in this browser. Please type your question.");
      return;
    }

    if (isListening) {
      try {
        recognitionRef.current?.stop();
      } catch (e) {}
      setIsListening(false);
    } else {
      setSpeechError(null);
      try {
        recognitionRef.current?.start();
      } catch (e) {
        console.warn("Could not start recognition:", e);
        setIsListening(false);
      }
    }
  };

  return (
    <div className="flex items-center gap-2">
      <button
        type="button"
        onClick={toggleListening}
        aria-label={isListening ? "Stop voice recording" : "Start voice recording"}
        title={
          isSpeechSupported
            ? isListening
              ? "Listening... Click to stop"
              : "Speak in English"
            : "Voice input unsupported"
        }
        className={`relative p-2.5 rounded-full transition-all duration-200 flex items-center justify-center ${
          isListening
            ? "bg-red-500 text-white animate-pulse shadow-lg shadow-red-500/30 scale-105"
            : isSpeechSupported
            ? "bg-stone-100 hover:bg-emerald-50 text-stone-600 hover:text-emerald-700 border border-stone-200"
            : "bg-stone-100 text-stone-300 cursor-not-allowed opacity-60"
        }`}
      >
        {isListening ? (
          <Mic className="w-5 h-5 animate-bounce" />
        ) : (
          <Mic className="w-5 h-5" />
        )}
      </button>

      {speechError && (
        <span className="text-xs text-amber-700 bg-amber-50 border border-amber-200 px-2 py-1 rounded flex items-center gap-1">
          <AlertCircle className="w-3 h-3" />
          {speechError}
        </span>
      )}
    </div>
  );
}

/**
 * Text-to-Speech Playback button for AI Responses
 */
export function SpeakButton({
  text,
  language = "en",
}: {
  text: string;
  language?: string;
}) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = () => {
    if (!("speechSynthesis" in window)) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    // Clean markdown/bullet points for cleaner speech
    const cleanText = text
      .replace(/[*_#`]/g, "")
      .replace(/•/g, "")
      .replace(/\n+/g, ". ");

    const utterance = new SpeechSynthesisUtterance(cleanText);

    // Map language
    if (language === "te" || /[\u0C00-\u0C7F]/.test(text)) {
      utterance.lang = "te-IN";
    } else if (language === "hi" || /[\u0900-\u097F]/.test(text)) {
      utterance.lang = "hi-IN";
    } else {
      utterance.lang = "en-IN";
    }

    utterance.rate = 0.95; // Slightly slower for family clarity
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.cancel(); // Stop any pending speech
    window.speechSynthesis.speak(utterance);
  };

  return (
    <button
      onClick={handleSpeak}
      type="button"
      title={isSpeaking ? "Stop speech" : "Read answer aloud"}
      className={`p-1.5 rounded-md text-xs font-medium transition-colors flex items-center gap-1 ${
        isSpeaking
          ? "bg-emerald-600 text-white shadow-sm"
          : "text-stone-500 hover:text-emerald-700 hover:bg-emerald-50"
      }`}
    >
      {isSpeaking ? (
        <>
          <VolumeX className="w-3.5 h-3.5 animate-pulse" />
          <span>Stop</span>
        </>
      ) : (
        <>
          <Volume2 className="w-3.5 h-3.5" />
          <span>Listen</span>
        </>
      )}
    </button>
  );
}
