import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ContributionGrid from "./ContributionGrid";
import type { CalendarDay } from "../../types";

function buildDays(totalDays: number, doneIndexes: number[] = []): CalendarDay[] {
  return Array.from({ length: totalDays }, (_, i) => ({
    date: `2026-04-${String(i + 1).padStart(2, "0")}`,
    done: doneIndexes.includes(i),
    count: doneIndexes.includes(i) ? 1 : 0,
  }));
}

describe("ContributionGrid", () => {
  it("should render correct number of day cells", () => {
    const days = buildDays(30);
    render(
      <ContributionGrid
        days={days}
        year={2026}
        month={4}
        selectedDate={null}
        onSelectDate={() => {}}
      />
    );

    const dayCells = screen.getAllByTestId(/^day-/);
    expect(dayCells).toHaveLength(30);
  });

  it("should render primary class for done days", () => {
    const days = buildDays(30, [0, 4]);
    render(
      <ContributionGrid
        days={days}
        year={2026}
        month={4}
        selectedDate={null}
        onSelectDate={() => {}}
      />
    );

    const day1 = screen.getByTestId("day-1");
    const day5 = screen.getByTestId("day-5");
    expect(day1.className).toMatch(/bg-primary/);
    expect(day5.className).toMatch(/bg-primary/);
  });

  it("should render surface class for not done days", () => {
    const days = buildDays(30, []);
    render(
      <ContributionGrid
        days={days}
        year={2026}
        month={4}
        selectedDate={null}
        onSelectDate={() => {}}
      />
    );

    const day2 = screen.getByTestId("day-2");
    expect(day2.className).toMatch(/bg-surface/);
  });
});
