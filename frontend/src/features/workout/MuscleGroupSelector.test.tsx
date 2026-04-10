import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import MuscleGroupSelector from "./MuscleGroupSelector";
import type { MuscleGroup } from "../../types";

const groups: MuscleGroup[] = [
  { id: 1, name: "Peito", category_id: 1 },
  { id: 2, name: "Costas", category_id: 1 },
  { id: 3, name: "Pernas", category_id: 1 },
];

describe("MuscleGroupSelector", () => {
  it("renders muscle groups", () => {
    render(
      <MuscleGroupSelector
        groups={groups}
        selectedIds={[]}
        onToggle={() => {}}
        loading={false}
      />
    );

    expect(screen.getByText("Peito")).toBeInTheDocument();
    expect(screen.getByText("Costas")).toBeInTheDocument();
    expect(screen.getByText("Pernas")).toBeInTheDocument();
  });

  it("highlights selected groups", () => {
    render(
      <MuscleGroupSelector
        groups={groups}
        selectedIds={[2]}
        onToggle={() => {}}
        loading={false}
      />
    );

    const selected = screen.getByText("Costas").closest("button");
    expect(selected).toHaveClass("bg-primary");
  });

  it("calls onToggle when a group is clicked", async () => {
    const onToggle = vi.fn();
    const user = userEvent.setup();

    render(
      <MuscleGroupSelector
        groups={groups}
        selectedIds={[]}
        onToggle={onToggle}
        loading={false}
      />
    );

    await user.click(screen.getByText("Pernas"));
    expect(onToggle).toHaveBeenCalledWith(3);
  });
});
