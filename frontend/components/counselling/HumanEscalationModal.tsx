"use client";

import React, { useState } from "react";
import {
  UserCheck,
  Phone,
  MessageSquare,
  Building,
  CheckCircle,
  X,
  AlertCircle,
  Calendar,
  Clock,
} from "lucide-react";
import { apiClient } from "@/lib/api-client";

interface HumanEscalationModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: string;
  defaultReason?: string;
  tradeTitle?: string;
}

export function HumanEscalationModal({
  isOpen,
  onClose,
  sessionId,
  defaultReason = "Family would like 1-on-1 personalized guidance with a certified vocational counsellor.",
  tradeTitle,
}: HumanEscalationModalProps) {
  const [reason, setReason] = useState(defaultReason);
  const [preferredMethod, setPreferredMethod] = useState("PHONE_CALL");
  const [contactDetails, setContactDetails] = useState("+91 98765 43210");
  const [urgency, setUrgency] = useState("NORMAL");
  const [submitting, setSubmitting] = useState(false);
  const [confirmedData, setConfirmedData] = useState<{
    escalation_id: string;
    estimated_callback_time: string;
  } | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await apiClient.escalateToHuman({
        session_id: sessionId,
        reason,
        preferred_contact_method: preferredMethod,
        contact_details: contactDetails,
        urgency,
      });

      if (res.success && res.data) {
        setConfirmedData({
          escalation_id: res.data.escalation_id,
          estimated_callback_time: res.data.estimated_callback_time,
        });
      } else {
        alert(res.message || "Failed to schedule counsellor session");
      }
    } catch (err: any) {
      alert("Error scheduling human counsellor: " + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-stone-200 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full hover:bg-stone-100 text-stone-400 hover:text-stone-700 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {confirmedData ? (
          /* Confirmation State */
          <div className="text-center py-6 space-y-4">
            <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto text-emerald-600 border border-emerald-200">
              <CheckCircle className="w-8 h-8" />
            </div>
            <div className="space-y-1">
              <h3 className="text-xl font-bold text-stone-900">
                Counsellor Request Confirmed
              </h3>
              <p className="text-xs text-stone-600">
                A certified NCVET/State Vocational Counsellor has been assigned.
              </p>
            </div>

            <div className="p-4 bg-stone-50 rounded-2xl border border-stone-200 text-left space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-stone-500">Ticket ID:</span>
                <span className="font-mono font-bold text-stone-800">
                  {confirmedData.escalation_id}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-stone-500">Estimated Callback:</span>
                <span className="font-semibold text-emerald-700">
                  {confirmedData.estimated_callback_time}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-stone-500">Topic:</span>
                <span className="font-medium text-stone-800">{tradeTitle || "Vocational Pathway"}</span>
              </div>
            </div>

            <button
              onClick={onClose}
              className="w-full py-3 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-xl text-sm transition-colors shadow-md shadow-teal-700/20"
            >
              Back to Counselling Dialogue
            </button>
          </div>
        ) : (
          /* Request Form */
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-teal-50 text-teal-700 rounded-2xl border border-teal-100">
                <UserCheck className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-stone-900">
                  Connect with Certified Counsellor
                </h3>
                <p className="text-xs text-stone-500">
                  Free 1-on-1 family guidance by accredited state vocational counsellors
                </p>
              </div>
            </div>

            <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <span>
                Our AI Counsellor assists with verified data, but complex family decisions or unusual circumstances benefit from a human mentor.
              </span>
            </div>

            {/* Reason */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-stone-700">
                What would you like to discuss?
              </label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows={2}
                required
                className="w-full text-xs p-3 bg-stone-50 border border-stone-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            {/* Preferred Contact Method */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-stone-700">
                Preferred Contact Method
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: "PHONE_CALL", label: "Phone Call", icon: Phone },
                  { id: "WHATSAPP", label: "WhatsApp", icon: MessageSquare },
                  { id: "IN_PERSON", label: "ITI Centre", icon: Building },
                ].map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => setPreferredMethod(item.id)}
                      className={`p-2.5 rounded-xl border text-xs font-medium flex flex-col items-center gap-1.5 transition-all ${
                        preferredMethod === item.id
                          ? "bg-teal-50 border-teal-500 text-teal-800 font-bold shadow-xs"
                          : "bg-stone-50 border-stone-200 text-stone-600 hover:bg-stone-100"
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Contact Details */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-stone-700">
                Phone Number / Contact Details
              </label>
              <input
                type="text"
                value={contactDetails}
                onChange={(e) => setContactDetails(e.target.value)}
                required
                placeholder="+91 Phone number"
                className="w-full text-xs px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2.5 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 py-2.5 text-xs font-semibold text-stone-600 hover:bg-stone-100 rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="flex-1 py-2.5 bg-teal-700 hover:bg-teal-800 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-teal-700/20 disabled:opacity-50"
              >
                {submitting ? "Booking..." : "Confirm Counsellor Callback"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
