"use client";

import { useEffect } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Next.js App Error:", error);
  }, [error]);

  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center p-6 text-center">
      <div className="p-4 mb-4 rounded-3xl bg-[#FDF0F0] text-[#F28482]">
        <AlertCircle className="w-8 h-8" />
      </div>
      <h2 className="text-xl font-bold text-[#14213D]">
        We encountered a display hurdle
      </h2>
      <p className="max-w-md text-sm text-[#64748B] mt-2 mb-6">
        {error.message || "An unexpected error occurred while rendering the page."}
      </p>
      <Button
        variant="primary"
        leftIcon={<RefreshCw className="w-4 h-4" />}
        onClick={() => reset()}
      >
        Reload View
      </Button>
    </div>
  );
}
