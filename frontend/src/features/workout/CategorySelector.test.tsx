import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import CategorySelector from "./CategorySelector";
import type { TrainingCategory } from "../../types";

const categories: TrainingCategory[] = [
  { id: 1, name: "Musculação" },
  { id: 2, name: "Cardio" },
  { id: 3, name: "Pilates" },
];

describe("CategorySelector", () => {
  it("renders categories", () => {
    render(
      <CategorySelector
        categories={categories}
        selectedId={null}
        onSelect={() => {}}
        loading={false}
      />
    );

    expect(screen.getByText("Musculação")).toBeInTheDocument();
    expect(screen.getByText("Cardio")).toBeInTheDocument();
    expect(screen.getByText("Pilates")).toBeInTheDocument();
  });

  it("highlights selected category", () => {
    render(
      <CategorySelector
        categories={categories}
        selectedId={1}
        onSelect={() => {}}
        loading={false}
      />
    );

    const selected = screen.getByText("Musculação").closest("button");
    expect(selected).toHaveClass("bg-primary-container");
  });

  it("calls onSelect when a category is clicked", async () => {
    const onSelect = vi.fn();
    const user = userEvent.setup();

    render(
      <CategorySelector
        categories={categories}
        selectedId={null}
        onSelect={onSelect}
        loading={false}
      />
    );

    await user.click(screen.getByText("Cardio"));
    expect(onSelect).toHaveBeenCalledWith(2);
  });

  it("renders skeleton cards when loading", () => {
    const { container } = render(
      <CategorySelector
        categories={[]}
        selectedId={null}
        onSelect={() => {}}
        loading={true}
      />
    );

    const skeletons = container.querySelectorAll(".animate-pulse");
    expect(skeletons.length).toBeGreaterThan(0);
  });
});
