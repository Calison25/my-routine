import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import WorkoutForm from "./WorkoutForm";

describe("WorkoutForm", () => {
  it("renders done toggle buttons", () => {
    render(<WorkoutForm onSubmit={() => {}} submitting={false} />);

    expect(screen.getByText("Fiz")).toBeInTheDocument();
    expect(screen.getByText("Não fiz")).toBeInTheDocument();
  });

  it("save button is disabled when no done selection", () => {
    render(<WorkoutForm onSubmit={() => {}} submitting={false} />);

    const saveButton = screen.getByRole("button", { name: "Registrar" });
    expect(saveButton).toBeDisabled();
  });

  it("save button is enabled after selecting done", async () => {
    const user = userEvent.setup();
    render(<WorkoutForm onSubmit={() => {}} submitting={false} />);

    await user.click(screen.getByText("Fiz"));

    const saveButton = screen.getByRole("button", { name: "Registrar" });
    expect(saveButton).toBeEnabled();
  });

  it("shows duration field only when done is true", async () => {
    const user = userEvent.setup();
    render(<WorkoutForm onSubmit={() => {}} submitting={false} />);

    expect(screen.queryByPlaceholderText("Opcional")).not.toBeInTheDocument();

    await user.click(screen.getByText("Fiz"));
    expect(screen.getByPlaceholderText("Opcional")).toBeInTheDocument();
  });

  it("hides duration field when not done", async () => {
    const user = userEvent.setup();
    render(<WorkoutForm onSubmit={() => {}} submitting={false} />);

    await user.click(screen.getByText("Não fiz"));
    expect(screen.queryByPlaceholderText("Opcional")).not.toBeInTheDocument();
  });

  it("calls onSubmit with form data", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<WorkoutForm onSubmit={onSubmit} submitting={false} />);

    await user.click(screen.getByText("Fiz"));
    await user.click(screen.getByRole("button", { name: "Registrar" }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        done: true,
        date: expect.any(String),
      })
    );
  });

  it("shows submitting state", () => {
    render(<WorkoutForm onSubmit={() => {}} submitting={true} />);

    expect(screen.getByText("Salvando...")).toBeInTheDocument();
  });
});
