"use client";

import React, { useState, useEffect } from "react";
import {
  CounsellorCase,
  CounsellorDashboardSummary,
  CounsellorNote,
} from "@/types";
import { apiClient } from "@/lib/api-client";
import {
  Users,
  ShieldCheck,
  AlertCircle,
  Clock,
  CheckCircle2,
  Headphones,
  Search,
  Filter,
  ArrowRight,
  Plus,
  Send,
  Lock,
  Globe,
  Sparkles,
  Award,
  Building,
  Phone,
  MessageSquare,
  ChevronRight,
  Activity,
  Check,
} from "lucide-react";

export function CounsellorPortal() {
  const [summary, setSummary] = useState<CounsellorDashboardSummary | null>(null);
  const [cases, setCases] = useState<CounsellorCase[]>([]);
  const [selectedCase, setSelectedCase] = useState<CounsellorCase | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>("ALL");
  const [filterPriority, setFilterPriority] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Note form state
  const [noteText, setNoteText] = useState("");
  const [noteVisibility, setNoteVisibility] = useState<"COUNSELLOR_PRIVATE" | "FAMILY_SHARED">("COUNSELLOR_PRIVATE");
  const [isActionItem, setIsActionItem] = useState(false);
  const [isSubmittingNote, setIsSubmittingNote] = useState(false);

  // Live presence state
  const [presence, setPresence] = useState<{ is_connected: boolean; counsellor_online: boolean; family_online: boolean } | null>(null);

  // Resolution state
  const [resolutionSummary, setResolutionSummary] = useState("");

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [sumRes, casesRes] = await Promise.all([
        apiClient.getCounsellorDashboardSummary(),
        apiClient.getCounsellorCases(),
      ]);

      if (sumRes.success && sumRes.data) {
        setSummary(sumRes.data);
      }
      if (casesRes.success && casesRes.data) {
        setCases(casesRes.data);
        if (casesRes.data.length > 0 && !selectedCase) {
          setSelectedCase(casesRes.data[0]);
        }
      }
    } catch (err) {
      console.error("Error loading counsellor data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Poll presence for selected case
  useEffect(() => {
    if (!selectedCase) return;
    const fetchPresence = async () => {
      try {
        const res = await apiClient.getCasePresence(selectedCase.id);
        if (res.success && res.data) {
          setPresence(res.data);
        }
      } catch (e) {}
    };
    fetchPresence();
    const interval = setInterval(fetchPresence, 10000);
    return () => clearInterval(interval);
  }, [selectedCase]);

  const handleAssignToMe = async () => {
    if (!selectedCase) return;
    try {
      const res = await apiClient.assignCounsellorCase(selectedCase.id, 1);
      if (res.success && res.data) {
        setSelectedCase(res.data);
        loadData();
      }
    } catch (err) {
      alert("Error assigning case: " + err);
    }
  };

  const handleUpdateStatus = async (newStatus: string) => {
    if (!selectedCase) return;
    try {
      const res = await apiClient.updateCounsellorCaseStatus(selectedCase.id, {
        case_status: newStatus,
        resolution_summary: newStatus === "RESOLVED" ? resolutionSummary : undefined,
      });
      if (res.success && res.data) {
        setSelectedCase(res.data);
        loadData();
      }
    } catch (err) {
      alert("Error updating status: " + err);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCase || !noteText.trim() || isSubmittingNote) return;
    setIsSubmittingNote(true);
    try {
      const res = await apiClient.addCounsellorNote(selectedCase.id, {
        note_text: noteText.trim(),
        visibility: noteVisibility,
        is_action_item: isActionItem,
      });
      if (res.success) {
        setNoteText("");
        // Reload case detail
        const updated = await apiClient.getCounsellorCaseDetail(selectedCase.id);
        if (updated.success && updated.data) {
          setSelectedCase(updated.data);
        }
      }
    } catch (err) {
      alert("Failed to add note: " + err);
    } finally {
      setIsSubmittingNote(false);
    }
  };

  const filteredCases = cases.filter((c) => {
    if (filterStatus !== "ALL" && c.case_status !== filterStatus) return false;
    if (filterPriority !== "ALL" && c.priority !== filterPriority) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchFamily = c.family_code?.toLowerCase().includes(q) || c.family_name?.toLowerCase().includes(q);
      const matchTrade = c.trade_title?.toLowerCase().includes(q);
      const matchReason = c.escalation_reason?.toLowerCase().includes(q);
      if (!matchFamily && !matchTrade && !matchReason) return false;
    }
    return true;
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* 1. Header & KPI Metrics */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="relative z-10 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-semibold border border-teal-400/30">
                <ShieldCheck className="w-3.5 h-3.5" />
                Accredited Counsellor Workstation
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold font-outfit text-white">
                Vocational Guidance Case Dashboard
              </h1>
              <p className="text-xs sm:text-sm text-slate-300">
                Direct decision-support for families navigating vocational qualifications
              </p>
            </div>
          </div>

          {/* KPI Summary Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            {[
              { label: "New Escalations", val: summary?.new_cases ?? 0, color: "text-amber-400", bg: "bg-amber-500/10" },
              { label: "Active Sessions", val: summary?.active_cases ?? 0, color: "text-teal-400", bg: "bg-teal-500/10" },
              { label: "High Priority", val: summary?.priority_cases ?? 0, color: "text-rose-400", bg: "bg-rose-500/10" },
              { label: "Resolved Cases", val: summary?.resolved_cases ?? 0, color: "text-emerald-400", bg: "bg-emerald-500/10" },
            ].map((kpi, i) => (
              <div
                key={i}
                className={`p-4 rounded-2xl border border-white/10 ${kpi.bg} backdrop-blur-md space-y-1`}
              >
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  {kpi.label}
                </div>
                <div className={`text-2xl font-black ${kpi.color}`}>{kpi.val}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 2. MAIN SPLIT WORKSTATION: Case Queue (Left 4 cols) & Detail Dossier (Right 8 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT 4 COLS: CASE QUEUE */}
        <div className="lg:col-span-4 bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-stone-100">
            <h3 className="font-bold text-stone-900 text-sm flex items-center gap-2">
              <Users className="w-4 h-4 text-teal-700" />
              <span>Case Queue ({filteredCases.length})</span>
            </h3>
          </div>

          {/* Search & Filters */}
          <div className="space-y-2">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search family, trade, reason..."
                className="w-full text-xs pl-8 pr-3 py-2 bg-stone-50 border border-stone-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
              <Search className="w-3.5 h-3.5 text-stone-400 absolute left-2.5 top-2.5" />
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="bg-stone-50 border border-stone-200 rounded-xl px-2 py-1.5 text-xs text-stone-700"
              >
                <option value="ALL">All Statuses</option>
                <option value="OPEN">Open (New)</option>
                <option value="ASSIGNED">Assigned</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="RESOLVED">Resolved</option>
              </select>

              <select
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="bg-stone-50 border border-stone-200 rounded-xl px-2 py-1.5 text-xs text-stone-700"
              >
                <option value="ALL">All Priorities</option>
                <option value="URGENT">Urgent</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>
          </div>

          {/* Cases List */}
          <div className="space-y-2.5 max-h-[600px] overflow-y-auto pr-1">
            {filteredCases.length === 0 ? (
              <div className="p-6 text-center text-xs text-stone-400 bg-stone-50 rounded-2xl">
                No matching counsellor cases.
              </div>
            ) : (
              filteredCases.map((c) => {
                const isSelected = selectedCase?.id === c.id;
                return (
                  <button
                    key={c.id}
                    onClick={() => setSelectedCase(c)}
                    className={`w-full p-3.5 rounded-2xl text-left border transition-all space-y-1.5 ${
                      isSelected
                        ? "bg-teal-50/70 border-teal-500 shadow-xs"
                        : "bg-stone-50/50 hover:bg-stone-100/70 border-stone-200"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-white border border-stone-200 text-stone-800">
                        {c.family_code || `Case #${c.id}`}
                      </span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                          c.priority === "URGENT" || c.priority === "HIGH"
                            ? "bg-rose-100 text-rose-800"
                            : "bg-stone-100 text-stone-600"
                        }`}
                      >
                        {c.priority}
                      </span>
                    </div>

                    <div className="text-xs font-bold text-stone-900 truncate">
                      {c.trade_title || "Vocational Pathway"}
                    </div>

                    <div className="text-[11px] text-stone-500 line-clamp-2">
                      {c.escalation_reason}
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-stone-400 pt-1">
                      <span>Status: {c.case_status}</span>
                      <span>{new Date(c.created_at).toLocaleDateString()}</span>
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </div>

        {/* RIGHT 8 COLS: CASE DOSSIER & WORKBENCH */}
        <div className="lg:col-span-8 bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          {selectedCase ? (
            <>
              {/* Dossier Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-stone-100">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-teal-100 text-teal-900">
                      Case #{selectedCase.id}: {selectedCase.case_status}
                    </span>
                    <span className="text-xs text-stone-500">
                      Family: <strong>{selectedCase.family_code}</strong> ({selectedCase.location_label || "India"})
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-stone-900">
                    {selectedCase.trade_title || "Vocational Pathway Discussion"}
                  </h2>
                </div>

                {/* Status & Assignment Actions */}
                <div className="flex flex-wrap items-center gap-2">
                  {!selectedCase.assigned_counsellor_id ? (
                    <button
                      onClick={handleAssignToMe}
                      className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                    >
                      Assign to Me
                    </button>
                  ) : (
                    <div className="text-xs text-emerald-800 font-semibold bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
                      Assigned to {selectedCase.assigned_counsellor_name || "You"}
                    </div>
                  )}

                  <select
                    value={selectedCase.case_status}
                    onChange={(e) => handleUpdateStatus(e.target.value)}
                    className="bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs font-semibold text-stone-800"
                  >
                    <option value="OPEN">Mark OPEN</option>
                    <option value="ASSIGNED">Mark ASSIGNED</option>
                    <option value="IN_PROGRESS">Mark IN_PROGRESS</option>
                    <option value="FOLLOW_UP_NEEDED">Mark FOLLOW_UP</option>
                    <option value="RESOLVED">Mark RESOLVED</option>
                  </select>
                </div>
              </div>

              {/* Family Context & Reported Concerns */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-teal-50/50 rounded-2xl border border-teal-100 space-y-2 text-xs">
                  <div className="font-bold text-teal-900 text-[11px] uppercase tracking-wider">
                    Learner Profile & Aspiration
                  </div>
                  <div className="text-stone-700 space-y-1">
                    <div>
                      <strong>Learner:</strong> {selectedCase.learner_name || "Aarav (10th Passed)"}
                    </div>
                    <div>
                      <strong>Target Trade:</strong> {selectedCase.trade_title}
                    </div>
                    <div>
                      <strong>Contact:</strong> {selectedCase.preferred_contact_method} ({selectedCase.contact_details || "+91 Phone"})
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-amber-50/50 rounded-2xl border border-amber-200 space-y-2 text-xs">
                  <div className="font-bold text-amber-900 text-[11px] uppercase tracking-wider">
                    Reported Parent Concerns
                  </div>
                  <p className="text-stone-800 font-medium leading-relaxed">
                    "{selectedCase.escalation_reason}"
                  </p>
                  {selectedCase.parent_concerns && selectedCase.parent_concerns.length > 0 && (
                    <ul className="list-disc list-inside text-[11px] text-stone-700 space-y-0.5">
                      {selectedCase.parent_concerns.map((pc, i) => (
                        <li key={i}>{pc}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>

              {/* AI Counselling Summary */}
              {selectedCase.ai_summary && (
                <div className="p-4 bg-stone-50 rounded-2xl border border-stone-200 text-xs space-y-1.5">
                  <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                    <span>AI Pre-Counselling Evidence Synthesis</span>
                  </div>
                  <p className="text-stone-700 leading-relaxed">
                    {selectedCase.ai_summary}
                  </p>
                </div>
              )}

              {/* Counsellor Notes & Guidance Thread */}
              <div className="space-y-4 pt-4 border-t border-stone-100">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-stone-900 flex items-center gap-2">
                    <MessageSquare className="w-4 h-4 text-teal-700" />
                    <span>Counsellor Notes & Guidance Log ({selectedCase.notes?.length || 0})</span>
                  </h3>
                </div>

                {/* Notes List */}
                <div className="space-y-3">
                  {selectedCase.notes && selectedCase.notes.length > 0 ? (
                    selectedCase.notes.map((n) => (
                      <div
                        key={n.id}
                        className={`p-4 rounded-2xl border space-y-1.5 text-xs ${
                          n.visibility === "FAMILY_SHARED"
                            ? "bg-emerald-50/50 border-emerald-200"
                            : "bg-stone-50 border-stone-200"
                        }`}
                      >
                        <div className="flex items-center justify-between text-[11px] font-semibold">
                          <span className="flex items-center gap-1.5 text-stone-900">
                            {n.visibility === "FAMILY_SHARED" ? (
                              <Globe className="w-3.5 h-3.5 text-emerald-700" />
                            ) : (
                              <Lock className="w-3.5 h-3.5 text-stone-500" />
                            )}
                            {n.author_name || "Counsellor"} •{" "}
                            <span className="text-[10px] text-stone-500">
                              {n.visibility === "FAMILY_SHARED" ? "Shared with Family Room" : "Private Note"}
                            </span>
                          </span>
                          <span className="text-stone-400">{new Date(n.created_at).toLocaleString()}</span>
                        </div>
                        <p className="text-stone-800 leading-relaxed">{n.note_text}</p>
                      </div>
                    ))
                  ) : (
                    <div className="p-4 bg-stone-50 rounded-xl text-center text-xs text-stone-400">
                      No notes added yet.
                    </div>
                  )}
                </div>

                {/* Add Note Form */}
                <form onSubmit={handleAddNote} className="p-4 bg-stone-50 rounded-2xl border border-stone-200 space-y-3">
                  <label className="text-xs font-bold text-stone-800">
                    Add Counsellor Guidance Note:
                  </label>
                  <textarea
                    value={noteText}
                    onChange={(e) => setNoteText(e.target.value)}
                    rows={2}
                    placeholder="Enter clinical assessment or family action recommendation..."
                    required
                    className="w-full text-xs p-3 bg-white border border-stone-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  />

                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3 text-xs">
                      <label className="flex items-center gap-1.5 text-stone-700 cursor-pointer">
                        <input
                          type="radio"
                          name="visibility"
                          checked={noteVisibility === "COUNSELLOR_PRIVATE"}
                          onChange={() => setNoteVisibility("COUNSELLOR_PRIVATE")}
                        />
                        <span>Private Note (Counsellors only)</span>
                      </label>

                      <label className="flex items-center gap-1.5 text-emerald-800 font-semibold cursor-pointer">
                        <input
                          type="radio"
                          name="visibility"
                          checked={noteVisibility === "FAMILY_SHARED"}
                          onChange={() => setNoteVisibility("FAMILY_SHARED")}
                        />
                        <span>Share with Family Decision Room</span>
                      </label>
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmittingNote || !noteText.trim()}
                      className="px-4 py-2 bg-teal-700 hover:bg-teal-800 disabled:opacity-40 text-white rounded-xl text-xs font-bold transition-all shadow-xs flex items-center gap-1.5"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>Post Note</span>
                    </button>
                  </div>
                </form>
              </div>

              {/* Case Resolution Summary Box */}
              {selectedCase.case_status === "RESOLVED" && selectedCase.resolution_summary && (
                <div className="p-4 bg-emerald-50 rounded-2xl border border-emerald-200 text-xs space-y-1">
                  <div className="font-bold text-emerald-900 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                    <span>Agreed Resolution Roadmap</span>
                  </div>
                  <p className="text-emerald-800 leading-relaxed">
                    {selectedCase.resolution_summary}
                  </p>
                </div>
              )}
            </>
          ) : (
            <div className="p-12 text-center text-stone-400 space-y-2">
              <Headphones className="w-10 h-10 mx-auto text-stone-300" />
              <p className="text-sm font-bold text-stone-700">Select a case from the queue</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
