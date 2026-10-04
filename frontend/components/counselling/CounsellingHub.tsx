"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Trade,
  CounsellingDialogueResponse,
  CounsellingMessageItem,
  EvidenceCitation,
  SuggestedStartersData,
} from "@/types";
import { apiClient } from "@/lib/api-client";
import { FamilyContextPanel } from "./FamilyContextPanel";
import { EvidenceDrawer } from "./EvidenceDrawer";
import { VoiceController, SpeakButton } from "./VoiceController";
import { HumanEscalationModal } from "./HumanEscalationModal";
import {
  Send,
  Sparkles,
  Bot,
  User,
  ShieldAlert,
  ArrowRight,
  Headphones,
  RotateCcw,
  Globe2,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
} from "lucide-react";

interface CounsellingHubProps {
  initialTradeId?: number;
  initialTrades?: Trade[];
}

export function CounsellingHub({
  initialTradeId,
  initialTrades = [],
}: CounsellingHubProps) {
  const [trades, setTrades] = useState<Trade[]>(initialTrades);
  const [selectedTrade, setSelectedTrade] = useState<Trade | null>(null);
  const [speakerRole, setSpeakerRole] = useState<"PARENT" | "LEARNER">("PARENT");
  const [language, setLanguage] = useState<"en" | "te" | "hi">("en");
  const [sessionId, setSessionId] = useState<string>("");
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [alignmentScore, setAlignmentScore] = useState(82);

  // Messages thread
  const [messages, setMessages] = useState<CounsellingMessageItem[]>([]);
  // Current active evidence drawer citations
  const [activeCitations, setActiveCitations] = useState<EvidenceCitation[]>([]);
  const [isEvidenceAvailable, setIsEvidenceAvailable] = useState<boolean>(true);

  // Suggested starter chips
  const [starters, setStarters] = useState<SuggestedStartersData | null>(null);

  // Human Escalation Modal
  const [isEscalationOpen, setIsEscalationOpen] = useState(false);
  const [escalationReason, setEscalationReason] = useState("");

  const chatEndRef = useRef<HTMLDivElement>(null);

  // Initialize trade list & session
  useEffect(() => {
    const init = async () => {
      let loadedTrades = initialTrades;
      if (!loadedTrades || loadedTrades.length === 0) {
        const res = await apiClient.getTrades();
        if (res.success && res.data) {
          loadedTrades = res.data;
          setTrades(loadedTrades);
        }
      }

      if (loadedTrades.length > 0) {
        const found = initialTradeId
          ? loadedTrades.find((t) => t.id === initialTradeId) || loadedTrades[0]
          : loadedTrades[0];
        setSelectedTrade(found);
      }
    };
    init();
  }, [initialTradeId, initialTrades]);

  // Load Starters & initial welcome message when trade or language changes
  useEffect(() => {
    if (!selectedTrade) return;

    const loadStarters = async () => {
      const res = await apiClient.getSuggestedStarters(selectedTrade.id);
      if (res.success && res.data) {
        setStarters(res.data);
      }
    };
    loadStarters();

    // Set introductory greeting if chat is empty
    if (messages.length === 0) {
      const greetingText =
        language === "te"
          ? `నమస్కారం! నేను స్కిల్‌సాథీ AI కౌన్సెలర్. ${selectedTrade.title} ట్రేడ్ సంబంధిత భవిష్యత్తు, జీతం, భద్రత మరియు పై చదువుల గురించి మీ కుటుంబానికి అధికారిక ప్రభుత్వ వివరాలను అందిస్తాను. మీ ప్రశ్నను అడగండి.`
          : `Namaste! I am SkillSathi AI Counsellor. I am here to help your family understand verified career outcomes, salary ranges, and higher education paths for ${selectedTrade.title}. How may I help you today?`;

      setMessages([
        {
          speaker: "COUNSELLOR",
          message: greetingText,
          language: language,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          suggested_chips: [
            language === "te" ? "ITI electrician ki future ela untundi?" : "What is the career growth and future?",
            language === "te" ? "Starting salary entha untundi?" : "What is the verified starting salary?",
            language === "te" ? "Higher studies ki chance unda?" : "Can my child study Diploma or Degree later?",
          ],
        },
      ]);
    }
  }, [selectedTrade, language]);

  // Scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = textToSend || inputMessage.trim();
    if (!query || isLoading) return;

    setInputMessage("");

    // Append user message immediately
    const userMsg: CounsellingMessageItem = {
      speaker: speakerRole,
      message: query,
      language: language,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await apiClient.sendCounsellingMessage({
        session_id: sessionId || undefined,
        message: query,
        speaker_role: speakerRole,
        language: language,
        trade_id: selectedTrade?.id,
      });

      if (res.success && res.data) {
        const d = res.data;
        if (!sessionId) setSessionId(d.session_id);

        if (d.family_alignment_score) {
          setAlignmentScore(d.family_alignment_score);
        }

        // Update evidence drawer
        if (d.evidence_citations && d.evidence_citations.length > 0) {
          setActiveCitations(d.evidence_citations);
        }
        setIsEvidenceAvailable(d.is_evidence_available);

        // Append Counsellor Response
        const counsellorMsg: CounsellingMessageItem = {
          speaker: "COUNSELLOR",
          message: d.response_text,
          language: d.detected_language || language,
          intent: d.detected_intent,
          concern: d.detected_concern,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          evidence_refs: d.evidence_citations,
          explanation_points: d.explanation_points,
          suggested_chips: d.suggested_question_chips,
          escalation_recommended: d.escalation_recommended,
        };

        setMessages((prev) => [...prev, counsellorMsg]);

        // If escalation recommended, prepare modal
        if (d.escalation_recommended) {
          setEscalationReason(
            d.escalation_reason || "Complex or unresolved family decision requires certified human mentor."
          );
        }
      } else {
        const errorMsg: CounsellingMessageItem = {
          speaker: "SYSTEM",
          message:
            res.message || "We encountered a temporary connection issue. Please try your question again.",
          language: "en",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        };
        setMessages((prev) => [...prev, errorMsg]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          speaker: "SYSTEM",
          message: "Failed to connect to counselling engine: " + err.message,
          language: "en",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetDialogue = () => {
    setMessages([]);
    setActiveCitations([]);
    setSessionId("");
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Top Banner / Mission Context */}
      <div className="bg-gradient-to-r from-teal-900 via-navy-900 to-teal-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/30 text-teal-300 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              AI-Enabled Family Career Counsellor
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-outfit">
              Evidence-Grounded Family Guidance
            </h1>
            <p className="text-stone-300 text-xs sm:text-sm leading-relaxed">
              Addressing parental concerns around income, job security, social prestige, and higher education using only verified NCVET & DGT government tracer data.
            </p>
          </div>

          {/* Quick Actions & Language Selector */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Reset Chat */}
            <button
              type="button"
              onClick={handleResetDialogue}
              title="Start New Dialogue Session"
              className="p-2.5 bg-white/10 hover:bg-white/20 rounded-xl border border-white/10 text-stone-300 hover:text-white transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            {/* Connect Human Counsellor */}
            <button
              type="button"
              onClick={() => {
                setEscalationReason("Family requested 1-on-1 human counsellor session");
                setIsEscalationOpen(true);
              }}
              className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-emerald-900/30 flex items-center gap-2"
            >
              <Headphones className="w-4 h-4" />
              <span>Talk to Human Counsellor</span>
            </button>
          </div>
        </div>
      </div>

      {/* THREE-REGION COUNSELLING INTERFACE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* REGION 1: Family Context Drawer (Left 3 cols) */}
        <div className="lg:col-span-3">
          <FamilyContextPanel
            activeTrade={selectedTrade}
            trades={trades}
            onSelectTrade={(t) => setSelectedTrade(t)}
            speakerRole={speakerRole}
            onToggleSpeaker={(role) => setSpeakerRole(role)}
            alignmentScore={alignmentScore}
          />
        </div>

        {/* REGION 2: Interactive Dialogue Hub (Center 6 cols) */}
        <div className="lg:col-span-6 bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col h-[740px] overflow-hidden">
          {/* Dialogue Header */}
          <div className="px-6 py-4 border-b border-stone-100 flex items-center justify-between bg-stone-50/50">
            <div className="flex items-center gap-2.5">
              <div className="w-3 h-3 rounded-full bg-emerald-500 animate-ping" />
              <div>
                <h3 className="font-bold text-stone-900 text-sm">
                  Active Dialogue: {selectedTrade?.title || "Trade Counselling"}
                </h3>
                <p className="text-[11px] text-stone-500">
                  Speaking as:{" "}
                  <span className="font-semibold text-teal-800">
                    {speakerRole === "PARENT" ? "Parent / Guardian" : "Learner (Student)"}
                  </span>
                </p>
              </div>
            </div>

            <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-teal-50 text-teal-800 border border-teal-200">
              NCVET Grounded
            </span>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {messages.map((msg, index) => {
              const isAI = msg.speaker === "COUNSELLOR";
              const isUser = msg.speaker === "PARENT" || msg.speaker === "LEARNER";

              return (
                <div
                  key={index}
                  className={`flex gap-3 ${
                    isUser ? "flex-row-reverse" : "flex-row"
                  } animate-fade-in`}
                >
                  {/* Avatar */}
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-bold ${
                      isAI
                        ? "bg-teal-700 text-white shadow-sm"
                        : msg.speaker === "PARENT"
                        ? "bg-amber-600 text-white shadow-sm"
                        : "bg-teal-600 text-white shadow-sm"
                    }`}
                  >
                    {isAI ? (
                      <Bot className="w-4 h-4" />
                    ) : (
                      <User className="w-4 h-4" />
                    )}
                  </div>

                  {/* Message Bubble */}
                  <div
                    className={`max-w-[85%] space-y-2.5 ${
                      isUser
                        ? "bg-stone-900 text-white rounded-2xl rounded-tr-xs p-4 shadow-sm"
                        : "bg-stone-50 text-stone-900 border border-stone-200 rounded-2xl rounded-tl-xs p-4 shadow-xs"
                    }`}
                  >
                    {/* Speaker Tag & Audio Button */}
                    <div className="flex items-center justify-between text-[11px] font-semibold opacity-75">
                      <span>
                        {isAI
                          ? "SkillSathi AI Counsellor"
                          : msg.speaker === "PARENT"
                          ? "Parent / Guardian"
                          : "Learner (Ramesh)"}
                      </span>
                      <div className="flex items-center gap-2">
                        <span>{msg.timestamp}</span>
                        {isAI && <SpeakButton text={msg.message} language={msg.language} />}
                      </div>
                    </div>

                    {/* Detected Intent / Concern Pill */}
                    {isAI && (msg.intent || msg.concern) && (
                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {msg.intent && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-100/70 text-teal-800 border border-teal-200">
                            Intent: {msg.intent.replace(/_/g, " ")}
                          </span>
                        )}
                        {msg.concern && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200">
                            Concern: {msg.concern.replace(/_/g, " ")}
                          </span>
                        )}
                      </div>
                    )}

                    {/* Text Body */}
                    <p className="text-xs sm:text-sm leading-relaxed whitespace-pre-line">
                      {msg.message}
                    </p>

                    {/* Explanation Bullet Points */}
                    {msg.explanation_points && msg.explanation_points.length > 0 && (
                      <div className="bg-white/80 rounded-xl p-3 border border-stone-200 text-xs space-y-1.5 text-stone-800 mt-2">
                        <div className="font-bold text-[11px] text-teal-900 uppercase tracking-wider">
                          Key Takeaways for Family:
                        </div>
                        <ul className="space-y-1 list-disc list-inside text-[11px]">
                          {msg.explanation_points.map((pt, i) => (
                            <li key={i}>{pt}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Escalation Button if Recommended */}
                    {msg.escalation_recommended && (
                      <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-900 text-xs space-y-2 mt-2">
                        <div className="flex items-center gap-1.5 font-bold">
                          <ShieldAlert className="w-4 h-4 text-amber-700" />
                          <span>Human Counsellor Recommended</span>
                        </div>
                        <p className="text-[11px] text-amber-800">
                          This specific family question or situation benefits from personal guidance with a certified vocational mentor.
                        </p>
                        <button
                          type="button"
                          onClick={() => {
                            setEscalationReason("Complex family query or missing verified tracer dataset");
                            setIsEscalationOpen(true);
                          }}
                          className="w-full py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-lg font-bold text-xs transition-colors flex items-center justify-center gap-1.5 shadow-xs"
                        >
                          <Headphones className="w-3.5 h-3.5" />
                          <span>Book Free 1-on-1 Counsellor Call</span>
                        </button>
                      </div>
                    )}

                    {/* Suggested Follow-up Question Chips */}
                    {msg.suggested_chips && msg.suggested_chips.length > 0 && (
                      <div className="pt-2 border-t border-stone-200/50 space-y-1.5">
                        <div className="text-[10px] font-bold uppercase tracking-wider text-stone-500">
                          Suggested follow-up questions:
                        </div>
                        <div className="flex flex-wrap gap-1.5">
                          {msg.suggested_chips.map((chip, ci) => (
                            <button
                              key={ci}
                              type="button"
                              onClick={() => handleSendMessage(chip)}
                              className="text-[11px] text-left px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 transition-colors font-medium flex items-center gap-1"
                            >
                              <span>{chip}</span>
                              <ArrowRight className="w-3 h-3 text-teal-600 shrink-0" />
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {isLoading && (
              <div className="flex items-center gap-3 p-4 bg-teal-50/50 rounded-2xl border border-teal-100 animate-pulse">
                <Bot className="w-5 h-5 text-teal-700 animate-bounce" />
                <span className="text-xs font-semibold text-teal-900">
                  Retrieving verified government evidence and analyzing family context...
                </span>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Suggested Starter Chips Footer */}
          {starters && (
            <div className="px-5 py-2.5 bg-stone-50 border-t border-stone-100 flex items-center gap-2 overflow-x-auto text-xs">
              <span className="text-[10px] font-bold text-stone-500 uppercase tracking-wider shrink-0">
                Quick Ask:
              </span>
              {(speakerRole === "PARENT"
                ? starters.parent_starters
                : starters.learner_starters
              )
                .slice(0, 3)
                .map((s, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSendMessage(s.text)}
                    className="whitespace-nowrap px-3 py-1 bg-white hover:bg-stone-100 border border-stone-200 rounded-full text-[11px] text-stone-700 font-medium transition-colors shadow-2xs shrink-0"
                  >
                    {s.label}
                  </button>
                ))}
            </div>
          )}

          {/* Dialogue Input Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="p-4 bg-white border-t border-stone-200 flex items-center gap-2"
          >
            {/* Voice STT Controller */}
            <VoiceController
              language={language}
              onTranscript={(transcript) => {
                setInputMessage(transcript);
                handleSendMessage(transcript);
              }}
              isListening={isListening}
              setIsListening={setIsListening}
            />

            {/* Text Input Bar */}
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={`Ask a question as ${
                speakerRole === "PARENT" ? "Parent" : "Student"
              } in English...`}
              className="flex-1 text-xs sm:text-sm px-4 py-3 bg-stone-50 border border-stone-200 rounded-2xl focus:ring-2 focus:ring-teal-500 focus:outline-none transition-all placeholder:text-stone-400 font-medium"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="p-3 bg-teal-700 hover:bg-teal-800 disabled:opacity-40 text-white rounded-2xl transition-all shadow-md shadow-teal-700/20 flex items-center justify-center shrink-0"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* REGION 3: Live Verified Evidence Drawer (Right 3 cols) */}
        <div className="lg:col-span-3">
          <EvidenceDrawer
            citations={activeCitations}
            isEvidenceAvailable={isEvidenceAvailable}
            activeTradeTitle={selectedTrade?.title}
          />
        </div>
      </div>

      {/* Human Counsellor Escalation Modal */}
      <HumanEscalationModal
        isOpen={isEscalationOpen}
        onClose={() => setIsEscalationOpen(false)}
        sessionId={sessionId}
        defaultReason={escalationReason}
        tradeTitle={selectedTrade?.title}
      />
    </div>
  );
}
