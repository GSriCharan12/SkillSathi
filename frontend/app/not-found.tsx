import Link from "next/link";
import { Compass } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center p-6 text-center">
      <div className="p-4 mb-4 rounded-3xl bg-[#E8F5F3] text-[#2A9D8F]">
        <Compass className="w-8 h-8" />
      </div>
      <h2 className="text-xl font-bold text-[#14213D]">
        Pathway Not Found (404)
      </h2>
      <p className="max-w-md text-sm text-[#64748B] mt-2 mb-6">
        The page or vocational pathway module you are trying to view is not accessible.
      </p>
      <Link href="/">
        <Button variant="primary">
          Return to SkillSathi Home
        </Button>
      </Link>
    </div>
  );
}
