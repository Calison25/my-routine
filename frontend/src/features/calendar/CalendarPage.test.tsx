import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import CalendarPage from "./CalendarPage";

vi.mock("../../hooks/useWorkoutCalendar", () => ({
  useWorkoutCalendar: () => ({
    calendar: {
      days: Array.from({ length: 30 }, (_, i) => ({
        date: `2026-04-${String(i + 1).padStart(2, "0")}`,
        done: false,
        count: 0,
      })),
    },
    loading: false,
    error: null,
  }),
}));

describe("CalendarPage", () => {
  it("should render the current month name in Portuguese", () => {
    render(<CalendarPage />);

    expect(screen.getByText(/Abril/i)).toBeInTheDocument();
    expect(screen.getByText(/2026/)).toBeInTheDocument();
  });
});
