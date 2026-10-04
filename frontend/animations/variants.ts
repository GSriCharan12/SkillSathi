/**
 * SkillSathi Motion Foundation - "FUTURE GARDEN"
 * High-craft, intentional Framer Motion variants respecting reduced-motion preferences.
 */
import { Variants, Transition } from "framer-motion";

// Check if user prefers reduced motion in browser
const isReducedMotion = () => {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
};

export const transitionSpring: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 24,
};

export const transitionSmooth: Transition = {
  duration: 0.45,
  ease: [0.22, 1, 0.36, 1],
};

// 1. Fade Up Variant
export const fadeUpVariant: Variants = {
  hidden: {
    opacity: 0,
    y: isReducedMotion() ? 0 : 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.45,
      ease: [0.22, 1, 0.36, 1],
    },
  },
};

// 2. Fade In Variant
export const fadeInVariant: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.35, ease: "easeOut" },
  },
};

// 3. Stagger Container Variant
export const staggerContainerVariant: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.05,
    },
  },
};

// 4. Scale Variant
export const scaleVariant: Variants = {
  hidden: {
    opacity: 0,
    scale: isReducedMotion() ? 1 : 0.94,
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24,
    },
  },
};

// 5. Card Hover Variant
export const cardHoverVariant: Variants = {
  initial: { y: 0, boxShadow: "0 4px 20px -2px rgba(20, 33, 61, 0.05)" },
  hover: {
    y: isReducedMotion() ? 0 : -4,
    boxShadow: "0 14px 30px -4px rgba(20, 33, 61, 0.12)",
    transition: { duration: 0.25, ease: "easeOut" },
  },
  tap: { scale: 0.98 },
};

// 6. Modal Variant
export const modalVariant: Variants = {
  hidden: {
    opacity: 0,
    scale: isReducedMotion() ? 1 : 0.95,
    y: isReducedMotion() ? 0 : 16,
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.96,
    y: 10,
    transition: { duration: 0.2 },
  },
};

// 7. Drawer Variant
export const drawerVariant: Variants = {
  hidden: { x: "100%", opacity: 0.5 },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24,
    },
  },
  exit: {
    x: "100%",
    opacity: 0,
    transition: { duration: 0.25, ease: "easeInOut" },
  },
};

// 8. Page Transition Variant
export const pageTransitionVariant: Variants = {
  initial: { opacity: 0, y: isReducedMotion() ? 0 : 8 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] },
  },
  exit: { opacity: 0, transition: { duration: 0.2 } },
};

// 9. Path Drawing Variant
export const pathDrawVariant: Variants = {
  hidden: { pathLength: 0, opacity: 0 },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: { duration: 1.2, ease: "easeInOut" },
  },
};
